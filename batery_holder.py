# Copyright © 2023 Jeremy Wright
#
# License: BSD
#
# THIS SOFTWARE IS PROVIDED BY JEREMY WRIGHT AS IS AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL JEREMY WRIGHT BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import cadquery as cq
from ocp_vscode import show_object

# All units are in mm

# Battery Parameters

battery_diameter = 14.3  # AA
# battery_diameter = 10.2  # Uncomment for AAA
# battery_diameter = 16.75  # Uncomment for 18650
# battery_diameter = 17  # Uncomment for CR123 (fit is untested)
# battery_diameter = 26.2  # Uncomment for C (fit is untested)
# battery_diameter = 34.2  # Uncomment for D (fit is untested)

# Will control how loose or tight the battery pockets are
battery_clearance = 0.25

# Sets the grid size for the pockets as well as how thick the box is
number_of_rows = 2
number_of_columns = 4
box_thickness = 10

# We need the radius of the battery for hole circle size
battery_radius = battery_diameter / 2.0

# Calculate the overall box size
box_width = (number_of_rows * (battery_diameter + battery_diameter * 0.3))
box_length = (number_of_columns * (battery_diameter + battery_diameter * 0.3))

# Build the main box
battery_box = cq.Workplane().box(box_width, box_length, box_thickness)

# Add the battery holes to the box
battery_box = (battery_box.faces(">Z").workplane(invert=True)
                          .rarray(battery_diameter * 1.25, battery_diameter * 1.25, number_of_rows, number_of_columns)
                          .circle(battery_radius + battery_clearance)
                          .cutBlind(box_thickness - 1.0))

# Cut access holes in the bottom of the battery pockets
battery_box = (battery_box.faces("<Z").workplane()
                          .rarray(battery_diameter * 1.25, battery_diameter * 1.25, number_of_rows, number_of_columns)
                          .circle(battery_radius * 0.75)
                          .cutThruAll())

# Add fillets to make the box look nicer
battery_box = battery_box.edges("|Z").fillet(2.0)
battery_box = battery_box.faces(">Z").edges("not %CIRCLE").fillet(0.5)
battery_box = battery_box.faces("<Z").edges("not %CIRCLE").fillet(0.5)

# Uncomment and change the path to export
# cq.exporters.export(battery_box, '/path/to/model/battery_box_AA_2x4.stl')

# Assumes that the model is being run inside CQ-editor
show_object(battery_box)