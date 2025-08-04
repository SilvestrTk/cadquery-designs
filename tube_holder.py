import cadquery as cq
from ocp_vscode import show_object

#this is the simple tube holder

bwidth = 160 #total width of the holder
bheight = 80 #total height of the holder

#safe values 8 - 60
diameter = 16 #diameter of the holes (keep in mind tolerance, usually miniaml 0.6-1.0mm from the tube diameter)
row = int(bwidth/(diameter+10)) #number of rows

corner_radius = diameter/2+4

hole = cq.Workplane("XY").circle(diameter / 2).extrude(bheight - 3).edges("<Z").chamfer(2)

box = cq.Workplane("XY").box(bwidth, bwidth, bheight).edges("|Z").fillet(corner_radius).edges("<Z").chamfer(2)

def add_holes(wp):
    for i in range(row):
        for j in range(row):
            x = (j - (row - 1) / 2) * (bwidth/row)
            y = (i - (row - 1) / 2) * (bwidth/row)
            wp = wp.cut(hole.translate((x, y, 0)))
    return wp

box = add_holes(box).edges(">Z").chamfer(1)
show_object(box)