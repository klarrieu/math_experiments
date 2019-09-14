from PIL import Image, ImageOps

img_path = 'input5.jpg'
img = Image.open(img_path)
img = ImageOps.expand(img, border=100, fill=(255, 185, 87))
width, height = img.size
print(width, height)
left = 320
top_cut = 50
img = img.crop(box=(left, top_cut, left + (height - top_cut)//(1.8), height))
img.save("input_border_crop.jpg")
img.show()
