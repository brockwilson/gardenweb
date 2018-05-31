from gardenweb.db import get_db
import gardenweb.bed
import svgwrite
import datetime

pixels_per_foot = 50
beds_filename = "gardenweb/static/beds.svg"
bed_filename = "gardenweb/static/bed.svg"
image_width = 2000
image_height = 2000

x_padding = 20
y_padding = 20

def feet_to_pixels(feet):
    return round(feet*pixels_per_foot)

def pixels_to_feet(pixels):
    return pixels/pixels_per_foot

def calculate_beds_size(beds, zero_top_left = False):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for bed in beds:
        max_x = max(max_x, (0 if zero_top_left else bed['top_left_x']) + bed['x_length'])
        max_y = max(max_y, (0 if zero_top_left else bed['top_left_y']) + bed['y_length'])
    return (feet_to_pixels(max_x-min_x) + 2*x_padding,
            feet_to_pixels(max_y-min_y) + 2*y_padding)

def draw_bed(bed, svg_handle, x_padding = 0, y_padding = 0, zero_top_left = False):
    bed_rect = svg_handle.rect(insert = (x_padding+feet_to_pixels((0 if zero_top_left else bed['top_left_x'])),
                                         y_padding+feet_to_pixels((0 if zero_top_left else bed['top_left_y']))),
                               size = (feet_to_pixels(bed['x_length']),
                                       feet_to_pixels(bed['y_length'])),
                               class_="bed")
    # get the plantings
    # draw the plantings
    svg_handle.add(bed_rect)



def make_beds_svg():
    beds = gardenweb.bed.get_beds()
    dwg = svgwrite.Drawing(filename = beds_filename,
                           size = calculate_beds_size(beds)+(x_padding, y_padding))
    dwg.add_stylesheet("beds.css","beds")
    for bed in beds:
        draw_bed(bed, dwg, x_padding = x_padding, y_padding = y_padding)
    dwg.save()

def make_bed_svg(bed):
    dwg = svgwrite.Drawing(filename = bed_filename,
                           size = calculate_beds_size([bed], zero_top_left = True)+ (x_padding, y_padding))
    dwg.add_stylesheet("beds.css", "beds")
    draw_bed(bed, dwg, x_padding = x_padding, y_padding = y_padding, zero_top_left = True)
    dwg.save()
    
