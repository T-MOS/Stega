# Stega
This is a silly and unnecessary tool I made to steganographically embed or extract/print the description text from NASA's APOD posts into the images collected via my APOD Picker wallpaper setter tool.

# "Modes"
1) Stegappend -> add row(s) of pixels after original image data that contain the encoded text 
2) Stega Prime -> distribute the encoded text bytes throughout the 2 least significant bits; per pixel per color channel
