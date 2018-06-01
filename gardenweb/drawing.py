from gardenweb.db import get_beds, get_plantings
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
    bed_group = svg_handle.g(class_ = "bed")
    bed_rect = svg_handle.rect(insert = (x_padding+feet_to_pixels((0 if zero_top_left else bed['top_left_x'])),
                                         y_padding+feet_to_pixels((0 if zero_top_left else bed['top_left_y']))),
                               size = (feet_to_pixels(bed['x_length']),
                                       feet_to_pixels(bed['y_length'])),
                               class_="bed")
    bed_group.add(bed_rect)
    svg_handle.add(bed_group)
    return None

def draw_bed_plantings(bed, svg_handle, x_padding = 0, y_padding = 0, zero_top_left = False):
    plantings = get_plantings(bed['id'])
    for planting in plantings:
        draw_planting(bed, planting, svg_handle, x_padding, y_padding, zero_top_left)
    return None

def draw_planting(bed, planting, svg_handle, x_padding = 0, y_padding = 0, zero_top_left = False):
    if zero_top_left:
        top_left_x = planting['top_left_x']
        top_left_y = planting['top_left_y']
    else:
        top_left_x = bed['top_left_x'] + planting['top_left_x']
        top_left_y = bed['top_left_y'] + planting['top_left_y']
        
    planting_group = svg_handle.g(class_="planting")
    planting_rect = svg_handle.rect(insert = (x_padding+feet_to_pixels(top_left_x),
                                              y_padding+feet_to_pixels(top_left_y)),
                                    size = (feet_to_pixels(planting['x_length']),
                                            feet_to_pixels(planting['y_length'])),
                                    class_="planting")
    text_handle = svg_handle.text(planting['plant_type'],
                                  insert = (x_padding + feet_to_pixels(top_left_x + planting['x_length']/2),
                                            y_padding + feet_to_pixels(top_left_y + planting['y_length']/2)),
                                  class_="planting")
    planting_group.add(planting_rect)
    planting_group.add(text_handle)
    svg_handle.add(planting_group)
    return None



def make_beds_svg():
    beds = get_beds()
    dwg = svgwrite.Drawing(filename = beds_filename,
                           size = calculate_beds_size(beds)+(x_padding, y_padding))
    dwg.add_stylesheet("beds.css","beds")
    for bed in beds:
        draw_bed(bed, dwg, x_padding = x_padding, y_padding = y_padding, zero_top_left = False)
    for bed in beds:
        draw_bed_plantings(bed, dwg, x_padding, y_padding, zero_top_left=False)
    dwg.save()
    return None

def make_bed_svg(bed):
    dwg = svgwrite.Drawing(filename = bed_filename,
                           size = calculate_beds_size([bed], zero_top_left = True)+ (x_padding, y_padding))
    dwg.add_stylesheet("beds.css", "beds")
    draw_bed(bed, dwg, x_padding = x_padding, y_padding = y_padding, zero_top_left = True)
    draw_bed_plantings(bed, dwg, x_padding, y_padding, zero_top_left=True)
    dwg.save()
    return None
    
