import sys
import numpy as np
from PIL import Image

r""" python .\Stegappend.py "test\iapetus3_cassini_slim.jpg" "test\text.txt """

# run conditions
# CLI


# Module
# if __name__ == "Stegappend":
#   # 3) Encode "Stegappend" -> 2 params:
#   # 4) Decode "Stegappend" -> 1 arg

def image_accessor(image = sys.argv[1]):
  openInitial = Image.open(image)
  image_array = np.array(openInitial)
  return image_array


# ENCODE
def text_to_dec(text = sys.argv[2]):
  with open(text, 'r') as t:
    text = t.read()
    decimalized = np.array([byte for byte in bytearray(text, 'utf-8')])
    decimalShaped = pad_and_reshape_text_decimals(decimalized)
  return decimalShaped

def pad_and_reshape_text_decimals(decimal_array):
  fit = len(decimal_array) % 3
  rightPad = 0

  if fit != 0:
    rightPad = 3-fit

  padded = np.pad(decimal_array,(0,rightPad), mode = "constant").reshape(-1,3)
  return padded

def array_operations(shaped_array):
  row_count = (len(shaped_array)//len(image_array))+1
  cols = image_array.shape[1]
  zerows = np.zeros((row_count,cols,3))
  
  # flatten,add,rebuild
  flat_stacked = np.vstack((image_array,zerows)).reshape(-1,3)
  added_start = len(flat_stacked)-(row_count*cols)
  insert_stop = added_start+len(shaped_array)
  for i in range(added_start,insert_stop):
    flat_stacked[i] = shaped_array[i % len(shaped_array)]
  rebuilt = flat_stacked.reshape(-1,cols,3).astype(np.uint8)
  
  text_embedded_image = Image.fromarray(rebuilt)
  return text_embedded_image


# DECODE 
def binary_decode(binString):
  # string_out = ''.join(chr(int(bytes[i:i+8],2)) for i in range(0,len(bytes),8))
  toBytes = bytes([int(binString)])
  return toBytes

if __name__ == "__main__":
  image_array = image_accessor() # argv 1

  # 1) Encode
  if len(sys.argv) == 3:
    decimal_shaped = text_to_dec() # argv 2
    text_embedded = array_operations(decimal_shaped)
    text_embedded.save("test/embedded_iapetus.bmp")
    text_embedded.show()
  # 2) Decode
  if len(sys.argv) == 2:
    decoded = binary_decode(image_array)
  else:
    print(sys.exit(1))
    # sys.exit(1)
