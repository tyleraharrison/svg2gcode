
"""Z position when tool is touching surface in mm"""
z_touching = 0.0

"""Z position where tool should travel in mm"""
z_travel = 10.0

"""Distance between pen and Y=0.0 in mm"""
y_offset = 60.0

"""Distance between pen and X=0.0 in mm"""
x_offset = 10.0

"""Print bed width in mm"""
bed_max_x = 221

"""Print bed height in mm"""
bed_max_y = 221

"""X/Y speed in mm/minute"""
xy_speed = 2400

"""Wait time between phases in milliseconds"""
wait_time = 1000

"""G-code emitted at the start of processing the SVG file"""
preamble = "G28; Home the machine\n; LAYER: 1\nG1 Z" + str(z_travel) + "; Raise printhead\nG1 F" + str(xy_speed) + "; Set X/Y speed in mm/min"

"""G-code emitted at the end of processing the SVG file"""
postamble = "G1 Z" + str(z_travel) + "; Raise tool\nG1 X0.0 Y220.0; Display printbed"

"""G-code emitted before processing a SVG shape"""
shape_preamble = "; ------\n; Draw shapes"

"""G-code emitted after processing a SVG shape"""
shape_postamble = "; ------\n; Shape completed"

""" 
Used to control the smoothness/sharpness of the curves.
Smaller the value greater the sharpness. Make sure the
value is greater than 0.1
"""
smoothness = 0.2


