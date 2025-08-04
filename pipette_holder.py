import cadquery as cq
from ocp_vscode import show_object
import os

#make the linke through the given coordinates and then extrude it as face and thicken to given thickness
def make_holder(list_points, width, thickness):
    if len(list_points) < 2:
        raise ValueError("At least two points are required to create a holder.")
    
    # Create a wire from the list of points
    wire = cq.Workplane("XY").spline(list_points)
    
    # Create a face from the wire and thicken it to the specified thickness
    # Use sweep to create a solid along the wire path
    # Create a rectangular cross-section for the sweep
    profile = cq.Workplane("YZ").rect(thickness, width)
    
    # Sweep the profile along the wire to create the solid
    solid = profile.sweep(wire).edges().chamfer(thickness/3)

    return solid

holder = make_holder(
    [(0, 0), (10, 0), (20, 5), (50, 0), (30, 40), (15, 80), (20, 80)],
    width=50,
    thickness=2
)
show_object(holder)