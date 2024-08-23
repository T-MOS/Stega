import sys
import numpy as np
from PIL import Image

# python .\Stegappend.py "test\iapetus3_cassini_slim.jpg" "test\text.txt

def image_accessor(image = sys.argv[1]):
  openInitial = Image.open(image)
  image_array = np.array(openInitial)
  return image_array

# ENCODE
def text_to_dec(text = sys.argv[2]):
  with open(text, 'r') as t:
    te = t.read()
    decimalized = np.array([byte for byte in bytearray(te, 'utf-8')])
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


# DECODE 
def decimal_accessor(image_array):
  # grab/flatten
  data_row = np.array(image_array[-1,...]).flatten
  # trim padding
  trimmed = [num for num in data_row if num > 0]
  # characterize
  decoded_row = bytes(data_row).decode('utf-8')

def decimal_decode(binString):
  # string_out = ''.join(chr(int(bytes[i:i+8],2)) for i in range(0,len(bytes),8))
  toBytes = bytes([int(binString)])
  return toBytes


# Run Conditions
if __name__ == "__main__":
  image_array = image_accessor() # argv 1
  # 1) Encoding
  if len(sys.argv) == 3:
    decimal_shaped = text_to_dec() # argv 2
    text_embedded = array_operations(decimal_shaped)
    text_embedded.save("test/embedded_iapetus.bmp")
    text_embedded.show()
  # 2) Decoding
  if len(sys.argv) == 2:
    decoded = decimal_decode(image_array)
  else:
    sys.exit(1)
