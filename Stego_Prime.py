import sys
import numpy as np
from PIL import Image

if __name__ == "__main__":
  if len(sys.argv) != 3:
      sys.exit(1)

def image_accessor(image_path = sys.argv[1]):
  openInitial = Image.open(image_path)
  image_array = np.array(openInitial)
  return image_array

def text_to_binary(text_file = sys.argv[2]):
  with open(text_file, 'r') as t:
    # binary_str = ''.join(format(byte,'08b') for byte in bytearray(t, 'utf-8'))
    decimalized = [byte for byte in bytearray(t, 'utf-8')]
  # return binary_str
  return decimalized

def binary_decode(binString):
  # string_out = ''.join(chr(int(bytes[i:i+8],2)) for i in range(0,len(bytes),8))
  toBytes = bytes([int(binString)])
  return string_out

iArr = image_accessor.reshape
d
#flatten,add,unflatten
iArr.reshape(-1,3)


# for i in range(len(flat_stacked)-41,len(flat_stacked)-41+len(decArr)):
#   flat_stacked[i] = decArr[i % len(decArr)]

# embedded = embedded.astype(np.uint8)