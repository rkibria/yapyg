from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

tile_size = 128
part_size = tile_size / 3

# 678
# 345
# 012
part_xy_table = (
    (0,2), # 0
    (1,2), # 1
    (2,2), # 2
    (0,1), # 3
    (1,1), # 4
    (2,1), # 5
    (0,0), # 6
    (1,0), # 7
    (2,0), # 8
    )
def remove_part(draw, part):
    x, y = part_xy_table[part]
    draw.rectangle((x * part_size,
                    y * part_size,
                    (x + 1) * part_size + 1,
                    (y + 1) * part_size + 1),
                   (0, 0, 0, 0),
                   (0, 0, 0, 0))

wall_remove_table = (
    (0,1,2, 3,5, 6,7,8), # 0
    (0,1,2, 3,5, 6,8), # 1
    (0,1,2, 3, 6,7,8), # 2
    (0,2, 3,5, 6,7,8), # 3
    (0,1,2, 5, 6,7,8), # 4
    (0,1,2, 3, 6,8), # 5
    (0,2, 3, 6,7,8), # 6
    (0,2, 5, 6,7,8), # 7
    (0,1,2, 5, 6,8), # 8
    (0,2, 3,5, 6,8), # 9
    (0,1,2, 6,7,8), # a
    (0,2, 6,7,8), # b
    (0,2, 5, 6,8), # c
    (0,1,2, 6,8), # d
    (0,2, 3, 6,8), # e
    (0,2, 6,8), # f
    )

output_positions = (
    (0,3), # 0
    (1,3), # 1
    (2,3), # 2
    (3,3), # 3
    (0,2), # 4
    (1,2), # 5
    (2,2), # 6
    (3,2), # 7
    (0,1), # 8
    (1,1), # 9
    (2,1), # a
    (3,1), # b
    (0,0), # c
    (1,0), # d
    (2,0), # e
    (3,0), # f
    )

full_image_name = "bricks"

def smooth_edges(tile_image, x1, y1, x2, y2):
    box = (x1, y1, x2, y2)
    ic = tile_image.crop(box)
    ic = ic.filter(ImageFilter.SMOOTH)
    tile_image.paste(ic, box)

offset = 4
    
def smooth_left(tile_image):
    smooth_edges(tile_image, -50, -50, part_size + offset, tile_size + 50)

def smooth_right(tile_image):
    smooth_edges(tile_image, 2 * part_size - offset, -50, tile_size + 50, tile_size + 50)

def smooth_top(tile_image):
    smooth_edges(tile_image, -50, 0, tile_size + 50, part_size + offset)
    
def smooth_bottom(tile_image):
    smooth_edges(tile_image, -50, 2 * part_size - offset, tile_size + 50, tile_size)

def smooth_topright(tile_image):
    smooth_edges(tile_image, 2 * part_size - offset, -50, tile_size + 50, part_size + offset)

def smooth_topleft(tile_image):
    smooth_edges(tile_image, -50, -50, part_size + offset, part_size + offset)
    
def smooth_bottomright(tile_image):
    smooth_edges(tile_image, 2 * part_size - offset, 2 * part_size - offset, tile_size + 50, tile_size + 50)

def smooth_bottomleft(tile_image):
    smooth_edges(tile_image, -50, 2 * part_size - offset, part_size + offset, tile_size + 50)
        
output_image = Image.new("RGBA", (tile_size * 4, tile_size * 4), (0,0,0,0))
index = 0
for remove_list in wall_remove_table:
    tile_image = Image.open(full_image_name + ".png")
    tile_image.load()
    draw = ImageDraw.Draw(tile_image)

    for part in remove_list:
        remove_part(draw, part)

    cut_image = Image.new("RGBA", (tile_size * 3, tile_size * 3), (0,0,0,0))
    cut_image.paste(tile_image, (tile_size, tile_size))
    
    if index == 0:
        smooth_left(tile_image)
        smooth_right(tile_image)
        smooth_top(tile_image)
        smooth_bottom(tile_image)
    elif index == 1:
        smooth_left(tile_image)
        smooth_right(tile_image)
        smooth_bottom(tile_image)
    elif index == 2:
        smooth_left(tile_image)
        smooth_top(tile_image)
        smooth_bottom(tile_image)
    elif index == 3:
        smooth_left(tile_image)
        smooth_right(tile_image)
        smooth_top(tile_image)
    elif index == 4:
        smooth_right(tile_image)
        smooth_top(tile_image)
        smooth_bottom(tile_image)
    elif index == 5:
        smooth_left(tile_image)
        smooth_bottom(tile_image)
        smooth_topright(tile_image)
    elif index == 6:
        smooth_left(tile_image)
        smooth_top(tile_image)
        smooth_bottomright(tile_image)
    elif index == 7:
        smooth_top(tile_image)
        smooth_right(tile_image)
        smooth_bottomleft(tile_image)
    elif index == 8:
        smooth_bottom(tile_image)
        smooth_right(tile_image)
        smooth_topleft(tile_image)
    elif index == 9:
        smooth_left(tile_image)
        smooth_right(tile_image)
    elif index == 10:
        smooth_top(tile_image)
        smooth_bottom(tile_image)
    elif index == 11:
        smooth_top(tile_image)
        smooth_bottomleft(tile_image)
        smooth_bottomright(tile_image)
    elif index == 12:
        smooth_right(tile_image)
        smooth_topleft(tile_image)
        smooth_bottomleft(tile_image)
    elif index == 13:
        smooth_bottom(tile_image)
        smooth_topleft(tile_image)
        smooth_topright(tile_image)
    elif index == 14:
        smooth_left(tile_image)
        smooth_topright(tile_image)
        smooth_bottomright(tile_image)
    elif index == 15:
        smooth_topright(tile_image)
        smooth_bottomright(tile_image)
        smooth_topleft(tile_image)
        smooth_bottomleft(tile_image)
    del draw

    for i in xrange(10):
        cut_image = cut_image.filter(ImageFilter.BLUR)
        cut_image = cut_image.filter(ImageFilter.SMOOTH)
        cut_image = cut_image.filter(ImageFilter.SMOOTH_MORE)
    cut_image = cut_image.crop((tile_size, tile_size, 2 * tile_size, 2 * tile_size))
    cut_image.paste(tile_image, (0, 0), tile_image)
    
    x = output_positions[index][0] * tile_size
    y = output_positions[index][1] * tile_size
    output_image.paste(cut_image, (x, y))

    index += 1

output_image.save(full_image_name + "_walls.png")
print "done"
