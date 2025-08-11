import cadquery as cq
from ocp_vscode import show_object
import math

#user parameters

diameter = 20  # mm
height = 20    # mm
axleDiameter = 6  # mm
tappered = True  # if true, the knob is tapered
axleStopper = True  # if true, add a stopper to the axle
axleBolt = True  # if true, add a bolt to the axle
wings = True  # if true, add wings to the knob
boltSize = 3  # mm, size of the bolt if axleBolt is True
axleNut = True  # if true, add a nut to the axle
turnPlusSideOptions = ["Left", "Right", "None"]  # side of the knob that turns, can be "left" or "right"
turnPlusSide = turnPlusSideOptions[1]  # side of the knob that turns, can be "left" or "right"


# Function to create the knob
def create_knob():
    tapperAngle = 2 if tappered else 0  # degrees, angle of the taper if tappered
    knob = (
        cq.Workplane("XY")
        .circle(diameter / 2)
        .extrude(height, taper=tapperAngle)
    )
        # add wings
    if wings:
        wingRadius = diameter / 12
        wingHeight = height
        num_wings = 16
        angle_step = 360 / num_wings
        for i in range(num_wings):
            angle = math.radians(i * angle_step)
            x = (diameter / 2 - 1) * math.cos(angle)
            y = (diameter / 2 - 1) * math.sin(angle)
            wing = (
                cq.Workplane("XY")
                .circle(wingRadius)
                .extrude(wingHeight, taper=tapperAngle)
                .translate((x, y, 0))
            )
            knob = knob.union(wing)
    # add axle
    axleRadius = axleDiameter / 2
    axle = (
        cq.Workplane("XY")
        .circle(axleRadius)
        .extrude(height - 2)
        )
    if axleStopper:
        stopper = (
            cq.Workplane("XY")
            .rect(axleDiameter, axleDiameter)
            .extrude(height - 2)
            .translate((axleRadius+axleRadius/2, 0,0))
        )
        axle = axle.cut(stopper)
    knob = knob.cut(axle)
    # add bolt
    if axleBolt:
        bolt = (
            cq.Workplane("YZ")
            .circle(boltSize / 2)
            .extrude(diameter)
            .translate((0 , 0, height/2 - 2))
        )
        boltHead = (
            cq.Workplane("YZ")
            .circle(boltSize / 2 + 1.5)
            .extrude(diameter)
            .translate((diameter/2-2, 0, height/2 - 2))
        )
        bolt = bolt.union(boltHead)
        knob = knob.cut(bolt)
    # add axle nut
    if axleNut:
        nut = (
            cq.Workplane("XY")
            .rect(boltSize-1, boltSize + 3)
            .extrude(height/2 + boltSize)
            .translate((axleRadius + 2, 0, 0))
        )
        knob = knob.cut(nut)
    
    # add turning side
    if turnPlusSide != "None":
        plusSign = (
            cq.Workplane("XY")
            .polyline([(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 1), (3, 1), (3, 0), (2, 0), (2, -1), (1, -1), (1,0), (0, 0)])
            .close()
            .extrude(0.6)
            .translate((-3, diameter/2-6, height))
        )
        text = cq.Workplane("XY").text("\u21BA", diameter/1.2, 0.6, 0.5, "center", "center").translate((0, 0, height))
        knob = knob.union(plusSign).union(text)
        if turnPlusSide == "Right":
            knob = knob.mirror("XZ")
    return knob

show_object(create_knob(), "Knob")