from gardenweb.db import get_db
import gardenweb.bed
import svgwrite
import datetime

pixels_per_foot = 50
filename = "garden_plan.svg"
image_width = 2000
image_height = 2000

x_padding = 20
y_padding = 20

def feet_to_pixels(feet):
    return round(feet*pixels_per_foot)

def pixels_to_feet(pixels):
    return pixels/pixels_per_foot



def make_bed_svg():
    dwg = svgwrite.Drawing("gardenweb/static/crap.svg", (2000, 2000))
    dwg.add(dwg.rect(insert=(10,10),
                     size=(200,400),
                     fill="black"))
    dwg.save()
    
