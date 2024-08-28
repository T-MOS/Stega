import sys, os
import numpy as np
from PIL import Image

# if __name__ == "__main__":
#   if len(sys.argv) != 3:
#     sys.exit(1)

def image_accessor(image):
  if isinstance(image, Image.Image):
    image_array = np.array(image)
  else:
    openInitial = Image.open(image)
    image_array = np.array(openInitial)
  return image_array

def text_to_binary(text):
  if os.path.exists(text):
    with open(text, 'r') as t:
      binary_str = ''.join(format(chr(char),'08b') for char in bytearray(t, 'utf-8'))
  else:
    binary_str = ''.join(format(chr(char),'08b') for char in bytearray(text, 'utf-8'))
  return binary_str

def pad_and_reshape_text_decimals(decimal_array):
  fit = len(decimal_array) % 3
  rightPad = 0

  if fit != 0:
    rightPad = 3-fit

  padded = np.pad(decimal_array,(0,rightPad), mode = "constant").reshape(-1,3)
  return padded

def binary_decode(binString):
  # string_out = ''.join(chr(int(bytes[i:i+8],2)) for i in range(0,len(bytes),8))
  toBytes = bytes([int(binString)])
  return toBytes + "11111110"

# image_array = image_accessor()
# decimal_shaped = text_to_dec(image_array)
# text_embedded = array_operations(decimal_shaped)

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
          new_pixel.append((channel & ~1) | int(binary_string[embed_index]))
          embed_index += 1
        else:
          new_pixel.append(channel)
      new_image_pixels.append(tuple(new_pixel)) # add full new pixel to new_image  

    else: # no more text bytes, add og pixel vals
      new_image_pixels.append(pixel)

def extractor(image_path):
  image = Image.open(image_path)
  pixels = list(image.getdata())

  binary_out = '' # LSB holder
  for pixel in pixels:
    for channel in pixel:
      binary_out += str(channel & 1)

  description = ''
  for i in range(0, len(binary_out), 8):
    byte = binary_out[i:i+8]
    if byte == '11111110':  # End of message delimiter
        break
    description += chr(int(byte, 2))
  return description