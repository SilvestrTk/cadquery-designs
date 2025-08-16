import cadquery as cq
import math
from ocp_vscode import show_object

# Parameters
text = "+ >>> -"
radius = 10
font_size = 3
font = "Arial"

# Calculate angle per character
angle_per_char = 90 / len(text)

# Create a workplane for the text
result = cq.Workplane("XY")

for i, char in enumerate(text):
    if char.isspace():
        continue  # Skip spaces or non-renderable characters
    angle = i * angle_per_char
    # Calculate position on the circle
    x = radius * math.cos(math.radians(angle))
    y = radius * math.sin(math.radians(angle))
    # Place each character and rotate it tangentially
    char_obj = cq.Workplane("XY").transformed(offset=(x, y, 0), rotate=(0, 0, angle + 90)).text(
        char, font_size, 1, font=font, kind="regular"
    )
    result = result.add(char_obj)

show_object(result)
