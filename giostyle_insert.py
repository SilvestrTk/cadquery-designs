import cadquery as cq
from ocp_vscode import show_object

# This is the insulation insert for gio style vaccine carrier

#dimensions need to be adjusted based on the actual size and considering the types of ice packs used

#outside dimensions
iwidth = 160  # total width of the insert
iheight = 80  # total height of the insert
ilength = 120  # total length of the insert

#thickness
ithickness = 6  # thickness of the insulation material

#corner radius
corner_radius = ithickness + 2  # corner radius for the insert

# Create the insulation insert
insulation_insert = (
    cq.Workplane("XY")
    .box(iwidth, iheight, ilength)
    .edges("|Z")
    .fillet(corner_radius)
    .edges("<Z")
    .chamfer(2)
    .faces(">Z")
    .shell(-ithickness)
)



show_object(insulation_insert)