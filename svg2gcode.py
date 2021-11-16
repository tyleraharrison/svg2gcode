#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

def generate_gcode():
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    
    width = root.get('width')
    height = root.get('height')
    if width == None or height == None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()                

    if width == None or height == None:
        print("Unable to get width and height for the svg")
        sys.exit(1)

    width = float(width.split("mm")[0])
    height = float(height.split("mm")[0])
    # Must keep the ratio of the svg, so offset will be largest between x/y
    offset = max(x_offset, y_offset)
    corrected_bed_max_x = bed_max_x - offset
    corrected_bed_max_y = bed_max_y - offset
    scale_x = corrected_bed_max_x / max(width, height)
    scale_y = corrected_bed_max_y / max(width, height)

    print(preamble)
    # Iterator to lower printhead at first point
    num_points = 0 
    
    for elem in root.iter():
        
        try:
            _, tag_suffix = elem.tag.split('}')
        except ValueError:
            continue

        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()

            if d:
                print(shape_preamble) 
                p = point_generator(d, m, smoothness)
                for x,y in p:
                    if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:  
                        print("G1 X%0.01f Y%0.01f" % ((scale_x*x)+x_offset, (scale_y*y)+y_offset))
                        num_points += 1
                        if num_points == 1:
                            print("G1 Z" + str(z_touching) + "; Lower tool")
                    else:
                        print("\n; Coordinates out of range:", "G1 X%0.01f Y%0.01f" % ((scale_x*x)+x_offset, (scale_y*y)+y_offset))
                        print("; Raw:", str(x), str(y), "\nScaled:", str(scale_x*x), str(scale_y*y), "\nScale Factors:", scale_x, scale_y, "\n")
                print("G1 Z" + str(z_travel) + "; Raise tool")
                num_points = 0
                print(shape_postamble)

    print(postamble) 
    print("; Generated", num_points, "points")

if __name__ == "__main__":
    generate_gcode()



