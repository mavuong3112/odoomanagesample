# Tạo icon.png đơn giản
from PIL import Image, ImageDraw

# Tạo hình ảnh 128x128 với nền màu xanh
img = Image.new('RGB', (128, 128), color=(41, 128, 185))
draw = ImageDraw.Draw(img)

# Vẽ một số hình cơ bản lên icon
draw.rectangle((20, 20, 108, 108), fill=(255, 255, 255), outline=(52, 152, 219))
draw.ellipse((35, 35, 93, 93), fill=(41, 128, 185), outline=(52, 152, 219))
draw.polygon([(64, 25), (100, 75), (28, 75)], fill=(52, 152, 219))

# Lưu file
img.save('icon.png') 