from gardenweb.db import get_db
import gardenweb.bed
import svgwrite
import datetime

pixels_per_foot = 50
filename = "gardenweb/static/crap.svg"
image_width = 2000
image_height = 2000

x_padding = 20
y_padding = 20

def feet_to_pixels(feet):
    return round(feet*pixels_per_foot)

def pixels_to_feet(pixels):
    return pixels/pixels_per_foot

def calculate_bed_size():
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    beds = gardenweb.bed.get_beds()
    for bed in beds:
        max_x = max(max_x, bed['top_left_x'] + bed['x_length'])
        max_y = max(max_y, bed['top_left_y'] + bed['y_length'])
    return (feet_to_pixels(max_x-min_x) + 2*x_padding,
            feet_to_pixels(max_y-min_y) + 2*y_padding)

def draw_bed(bed, svg_handle, x_padding = 0, y_padding = 0):
    bed_rect = svg_handle.rect(insert = (x_padding+feet_to_pixels(bed['top_left_x']),
                                         y_padding+feet_to_pixels(bed['top_left_y'])),
                               size = (feet_to_pixels(bed['x_length']),
                                       feet_to_pixels(bed['y_length'])),
                               class_="bed")
    svg_handle.add(bed_rect)

def make_bed_svg():
    dwg = svgwrite.Drawing(filename = filename,
                       size = calculate_bed_size()+(x_padding, y_padding))
    beds = gardenweb.bed.get_beds()
    for bed in beds:
        draw_bed(bed, dwg, x_padding = x_padding, y_padding = y_padding)
    dwg.save()
    
