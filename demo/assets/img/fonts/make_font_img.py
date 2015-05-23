from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

fontname = "DroidSansMonoDotted"
font = ImageFont.truetype(fontname + ".ttf", 14)

ch_w = 10
ch_h = 16
img_w = 12 * ch_w
img_h = 8 * ch_h

img = Image.new("RGBA", (img_w, img_h), (0,0,0,0))

for code in xrange(32, 128):
    digit = chr(code)
    draw = ImageDraw.Draw(img)

    x = (code - 32) % 12
    y = (code - 32) / 12
    draw.text((x * ch_w, y * ch_h), digit, (255,255,255), font=font)

img.save(fontname + ".png")
