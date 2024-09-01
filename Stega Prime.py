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


def per_pixel_channel(image_path,binary_string):
  image = Image.open(image_path)
  pixels = list(image.getdata())
  
  embed_index = 0
  new_image_pixels = []
  for pixel in pixels:
    if embed_index < len(binary_string):
      new_pixel = []
      for channel in pixel:
        if embed_index < len(binary_string):
          new_pixel.append((channel & ~3) | int(binary_string[embed_index:embed_index+2]))
          embed_index += 2
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

  binary_out = '' # LSB holder
  for pixel in pixels:
    for channel in pixel:
      binary_out += str(channel & 3)
  
  byte_array = bytearray()
  for i in range(0, len(binary_out), 8):
    byte = binary_out[i:i+8]
    if byte == '11111110':  # End of message delimiter
      break
    byte_array.append(int(byte,2))
  # description = ''

  decoded = byte_array.decode('utf-8')
  return decoded

if __name__ == "__main__":
  if len(sys.argv) == 3:
    per_pixel_channel(sys.argv[1],text_to_binary(sys.argv[2]))
  elif len(sys.argv) == 2:
    text_output = extractor(sys.argv[1])
    print(text_output)
  else:
    sys.exit(1)