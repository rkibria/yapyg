from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

tile_size = 128
parts = 4
part_size = tile_size / parts

def remove_part(draw, x, y):
    draw.rectangle((x * part_size,
                    y * part_size,
                    (x + 1) * part_size + 1,
                    (y + 1) * part_size + 1),
                   (0, 0, 0, 0),
                   (0, 0, 0, 0))

full_image_name = "bricks"

def smooth_edges(tile_image, x1, y1, x2, y2):
    box = (x1, y1, x2, y2)
    ic = tile_image.crop(box)
    ic = ic.filter(ImageFilter.SMOOTH)
    tile_image.paste(ic, box)

offset = 4

def smooth_top(tile_image):
    smooth_edges(tile_image, -50, -50, tile_size + 50, (parts - 1) * part_size + offset)

def smooth_right(tile_image):
    smooth_edges(tile_image, 1 * part_size - offset, -50, tile_size + 50, tile_size + 50)

def smooth_bottom(tile_image):
    smooth_edges(tile_image, -50, 1 * part_size - offset, tile_size + 50, tile_size)

def smooth_left(tile_image):
    smooth_edges(tile_image, -50, -50, (parts - 1) * part_size + offset, tile_size + 50)


def smooth_topright(tile_image):
    smooth_edges(tile_image, 1 * part_size - offset, -50, tile_size + 50, (parts - 1) * part_size + offset)

def smooth_bottomright(tile_image):
    smooth_edges(tile_image, 1 * part_size - offset, 1 * part_size - offset, tile_size + 50, tile_size + 50)

def smooth_bottomleft(tile_image):
    smooth_edges(tile_image, -50, 1 * part_size - offset, (parts - 1) * part_size + offset, tile_size + 50)

def smooth_topleft(tile_image):
    smooth_edges(tile_image, -50, -50, (parts - 1) * part_size + offset, (parts - 1) * part_size + offset)

tiles_table = (
    (
        ('....',
         '....',
         '....',
         '####',),
        [smooth_top],
    ),

    (
        ('#...',
         '#...',
         '#...',
         '#...',),
        [smooth_right],
    ),

    (
        ('####',
         '....',
         '....',
         '....',),
        [smooth_bottom],
    ),

    (
        ('...#',
         '...#',
         '...#',
         '...#',),
        [smooth_left],
    ),

    (
        ('#...',
         '#...',
         '#...',
         '####',),
        [smooth_topright],
    ),

    (
        ('####',
         '#...',
         '#...',
         '#...',),
        [smooth_bottomright],
    ),

    (
        ('####',
         '...#',
         '...#',
         '...#',),
        [smooth_bottomleft],
    ),

    (
        ('...#',
         '...#',
         '...#',
         '####',),
        [smooth_topleft],
    ),

    (
        ('....',
         '....',
         '....',
         '#...',),
        [smooth_top, smooth_right],
    ),

    (
        ('#...',
         '....',
         '....',
         '....',),
        [smooth_bottom, smooth_right],
    ),

    (
        ('...#',
         '....',
         '....',
         '....',),
        [smooth_bottom, smooth_left],
    ),

    (
        ('....',
         '....',
         '....',
         '...#',),
        [smooth_top, smooth_left],
    ),

)

output_image_h = tile_size * 4
output_image = Image.new("RGBA", (tile_size * 4, output_image_h), (0,0,0,0))
index = 0
col = 0
row = 0
for tile_lines, smooth_functions in tiles_table:
    tile_image = Image.open(full_image_name + ".png")
    tile_image.load()
    draw = ImageDraw.Draw(tile_image)

    print "%d:" % index
    y = 0
    for tile_line in tile_lines:
        x = 0
        for character in tile_line:
            if character != "#":
                remove_part(draw, x, y)
            x += 1
        y += 1
        print tile_line
    print ""

    # make working image extra large to avoid effect artefacts at the edges
    cut_image = Image.new("RGBA", (tile_size * 3, tile_size * 3), (0,0,0,0))
    cut_image.paste(tile_image, (tile_size, tile_size))

    for smooth_function in smooth_functions:
        (smooth_function)(tile_image)

    del draw

    cut_image = cut_image.convert('LA')
    cut_image = cut_image.filter(ImageFilter.GaussianBlur(25))
    cut_image = cut_image.convert('RGBA')
    cut_image = cut_image.crop((tile_size, tile_size, 2 * tile_size, 2 * tile_size))
    cut_image.paste(tile_image, (0, 0), tile_image)

    col = index % 4
    row = index / 4
    output_image.paste(cut_image, (col * tile_size, output_image_h - tile_size - row * tile_size))

    index += 1

output_image.save(full_image_name + "_walls.png")
print "done"
