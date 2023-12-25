from PIL import Image, ImageFilter, ImageOps
from matplotlib import pyplot as plt
# Opening the image
im = Image.open("img.jpg")
# For viewing the image
im.show()
# To apply guassian blur using ImageFilter module
im1 = im.filter(ImageFilter.GaussianBlur(7))
im1.show()
# To find edges using ImageFilter module
im2 = im.filter(ImageFilter.FIND_EDGES)
im2.show()
# To convert rgb image to grayscale image using ImageOps module
im3 = ImageOps.grayscale(im)
im3.show()
# To rotate image 75 degrees anticlockwise
im5 = im.rotate(75)
im5.show()
# To resize the image to 300 pixels x 300 pixels
im4 = im.resize((300, 300))
im4.show()
# To split the image into rgb format
r, g, b = im.split()
print("The histogram of red")
# Plotting histogram of red
rh = r.histogram()
p = plt.hist(rh, 100)
# Plotting histogram of blue
bh = b.histogram()
plt.hist(bh, 100)
# Plotting histogram of green
gh = g.histogram()
plt.hist(gh, 100)
plt.show()
