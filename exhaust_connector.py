import cadquery as cq
from ocp_vscode import show_object
import math

# User's Parameters
lowerPipeInnerDiameter = 20     # mm
upperPipeInnerDiameter =10   # mm
adapterTickness = 2 # mm
adapterHeight = 20 # mm
tapperLower = 2 #degrees
tapperUpper = -2 #degrees
insideTube = True # if true, add the inside tube to the exhaust connector

# Function to create the exhaust connector
def create_exhaust_connector():
    # Create the lower pipe
    global insideTube
    socketHeight = max(adapterHeight/3, 20.0)  # Ensure a minimum height for the socket

    # Lower pipe
    lowerPipeOuterRadius = lowerPipeInnerDiameter / 2 + adapterTickness
    lowerPipe = cq.Workplane("XY").circle(lowerPipeOuterRadius).extrude(socketHeight, taper=tapperLower)

    # Upper pipe
    upperPipeOuterRadius = upperPipeInnerDiameter / 2
    upperPipe = cq.Workplane("XY").circle(upperPipeOuterRadius).extrude(-socketHeight, taper=tapperUpper).translate((0, 0, 2 * socketHeight + adapterHeight))

    # Adapter radii at both ends, accounting for tapers
    lowerAdapterRadius = lowerPipeOuterRadius - socketHeight * math.tan(math.radians(tapperLower))
    print(f"Lower Adapter Radius: {lowerAdapterRadius} mm")
    upperAdapterRadius = upperPipeOuterRadius - socketHeight * math.tan(math.radians(tapperUpper))
    print(f"Upper Adapter Radius: {upperAdapterRadius} mm")

    #ensure that the taper angle is not too large
    if (math.degrees(math.atan((lowerAdapterRadius - upperAdapterRadius) / adapterHeight)) > 30):
        raise ValueError("Increase the socket height to ensure printability.")
    # Create the adapter as a loft between two circles
    adapter = (
        cq.Workplane("XY")
        .workplane(offset=socketHeight)
        .circle(lowerAdapterRadius)
        .workplane(offset=adapterHeight)
        .circle(upperAdapterRadius)
        .loft()
    )

    # Combine the parts
    exhaust_connector = lowerPipe.union(adapter).union(upperPipe).faces("|Z").shell(-adapterTickness)

    #add the inside tube
    if insideTube:
        insideTube = (
            cq.Workplane("XY")
            .circle(upperAdapterRadius)
            .extrude(2*socketHeight + adapterHeight)
            .translate((0, 0, -socketHeight))
            .faces("|Z")
            .shell(-adapterTickness)
        )

        exhaust_connector = exhaust_connector.union(insideTube)

    return exhaust_connector

if __name__ == "__main__":
    # Create the exhaust connector
    exhaust_connector = create_exhaust_connector()

    # Show the result in the OCP VSCode viewer
    show_object(exhaust_connector, name="Exhaust Connector")

    # Export the result to STL
    cq.exporters.export(exhaust_connector, "exhaust_connector.stl")