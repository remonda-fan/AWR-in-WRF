from images2gif import writeGif
from PIL import Image
import os,sys

os.chdir(sys.path[0])

file_names = sorted((fn for fn in os.listdir('.') if fn.endswith('.png')))
print file_names
#['animationframa.png', 'animationframb.png', ...] "

images = [Image.open(fn) for fn in file_names]

filename = "my_gif.GIF"

writeGif(filename, images, duration=0.1)