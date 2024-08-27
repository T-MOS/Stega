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

# def text_to_binary(text_file = sys.argv[2]):
#   with open(text_file, 'r') as t:
#     binary_str = ''.join(format(byte,'08b') for byte in bytearray(t, 'utf-8'))
#   return binary_str

def text_to_dec(text):
  if os.path.exists(text):
    with open(text, 'r',encoding="utf-8") as t:
      te = t.read()
      decimalized = np.array(bytearray(te, 'utf-8'))
      decimalShaped = pad_and_reshape_text_decimals(decimalized)
  else:
    decimalized = np.array(bytearray(text, 'utf-8'))
    decimalShaped = pad_and_reshape_text_decimals(decimalized)
  return decimalShaped

def pad_and_reshape_text_decimals(decimal_array):
  fit = len(decimal_array) % 3
  rightPad = 0

  if fit != 0:
    rightPad = 3-fit

  padded = np.pad(decimal_array,(0,rightPad), mode = "constant").reshape(-1,3)
  return padded

def array_operations(padded_array):
  row_count = (len(padded_array)//len(image_array))+1
  cols = image_array.shape[1]
  zerows = np.zeros((row_count,cols,3))
  
  # flatten,add,rebuild
  flat_stacked = np.vstack((image_array,zerows)).reshape(-1,3)
  added_start = len(flat_stacked)-(row_count*cols)
  insert_stop = added_start+len(padded_array)
  for i in range(added_start,insert_stop):
    flat_stacked[i] = padded_array[i % len(padded_array)]
  rebuilt = flat_stacked.reshape(-1,cols,3).astype(np.uint8)
  
  text_embedded_image = Image.fromarray(rebuilt)
  return text_embedded_image

def binary_decode(binString):
  # string_out = ''.join(chr(int(bytes[i:i+8],2)) for i in range(0,len(bytes),8))
  toBytes = bytes([int(binString)])
  return toBytes

# image_array = image_accessor()
# decimal_shaped = text_to_dec(image_array)
# text_embedded = array_operations(decimal_shaped)

embed_index = 0
new_image_pixels = []
for pixel in i_array_byte:
  if embed_index < len(initials_binary):
    new_pixel = []
    for channel in pixel:
      if embed_index < len(initials_binary)
        new_pixel.append((channel & ~1) | int(initials_binary[embed_index]))
        embed_index += 1
      else:
        new_pixel.append(channel)
      new_image_pixels.append(tuple(new_pixel)) # add full new pixel to new image  

    else: # no more message, add og pixel vals
      new_image_pixels.append(pixel)