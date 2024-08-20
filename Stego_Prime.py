import sys
import numpy as np
from PIL import Image

if len(sys.argv) != 3:
    sys.exit(1)

def image_accessor(image_path = sys.argv[1],text_file = sys.argv[2]):
  openInitial = Image.open(image_path)
  arrayed = np.array(openInitial)