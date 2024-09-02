import sys, os, re 
from PIL import Image

def sanitize_filename(string):
  pattern = r'([^\\/]+)\.[^.]+$' #read: "after last '/' before last '.'"
  rinsed = re.search(pattern, string)
  return rinsed.group(1)

def text_to_binary(text):
  if os.path.exists(text):
    with open(text, 'r', encoding='utf-8') as t:
      content = t.read()
      binary_str = ''.join(format(char,'08b') for char in content.encode('utf-8'))
  else:
    binary_str = ''.join(format(ord(char),'08b') for char in text)
  return binary_str + "11111110"

def two_per_channel(image_path, binary_string):
  image = Image.open(image_path)
  pixels = image.load()
  
  if len(binary_string) > image.width*image.height * 3 * 2:
    raise ValueError("Binary string is too long for dual LSB embed")

  bits = [int(bit) for bit in binary_string]
  bit_index = 0
  for y in range(image.height):
    for x in range(image.width):
      if bit_index >= len(binary_string):
        break

      r,g,b = pixels[x,y]

      if bit_index < len(binary_string):
        # embed 2 bits in red
        r = (r & ~3) | (bits[bit_index] << 1) | bits[bit_index +1]
        bit_index += 2
      if bit_index < len(binary_string):
        # in green
        g = (g & ~3) | (bits[bit_index] << 1) | bits[bit_index +1]
        bit_index += 2
      if bit_index < len(binary_string):
        # in blue
        b = (b & ~3) | (bits[bit_index] << 1) | bits[bit_index +1]
        bit_index += 2
        
      pixels[x,y] = (r,g,b)

  return image

def one_per_channel(image_path,binary_string):
  image = Image.open(image_path)
  pixels = list(image.getdata())
  if len(binary_string) > image.width * image.height * 3:
    raise ValueError("Binary string is too long to be embedded in LSB.")
  
  bit_index = 0
  new_image_pixels = []
  for pixel in pixels:
    if bit_index < len(binary_string):
      new_pixel = []
      for channel in pixel:
        if bit_index < len(binary_string):
          cleared_channel = channel & ~3
          embedded_bits = int(binary_string[bit_index:bit_index+2])
          new_channel = cleared_channel | embedded_bits
          new_pixel.append((channel & ~1) | int(binary_string[bit_index]))
          bit_index += 1
        else:
          new_pixel.append(channel)
      new_image_pixels.append(tuple(new_pixel)) # add full new pixel to new_image  

    else: # no more text bytes, add og pixel vals
      new_image_pixels.append(pixel)

  new_image = Image.new(image.mode, image.size)
  new_image.putdata(new_image_pixels)
  new_image.save(sanitize_filename(sys.argv[1]) + '_stegged.png')
  return new_image

def extractor(image_path):
  image = Image.open(image_path)
  pixels = list(image.getdata())

  # LSB
  try:  
    binary_out = '' # LSB holder
    for pixel in pixels:
      for channel in pixel:
        binary_out += str(channel & 1)
    
    byte_array = bytearray()
    for i in range(0, len(binary_out), 8):
      byte = binary_out[i:i+8]
      if byte == '11111110':  # End of message delimiter
        break
      byte_array.append(int(byte,2))

    decoded = byte_array.decode('utf-8')
    return decoded
  except:
    print("Non-LSB image")

  # Double LSB
  try:
    binary_out = ""
    for pixel in pixels:
      for channel in pixel:
        binary_out += format(channel & 3, "02b")

    byte_array = bytearray()
    for i in range(0, len(binary_out), 8):
      byte = binary_out[i:i+8]
      if byte == '11111110':  # End of message delimiter
        break
      byte_array.append(int(byte,2))

    decoded = byte_array.decode('utf-8')
    return decoded
  except Exception as e:
    print(f"Invalid: \n {e}")

if __name__ == "__main__":
  if len(sys.argv) == 3:
    one_per_channel(sys.argv[1],text_to_binary(sys.argv[2]))
  elif len(sys.argv) == 2:
    text_output = extractor(sys.argv[1])
    print(text_output)
  else:
    sys.exit(1)