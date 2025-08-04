import cadquery as cq
from ocp_vscode import show_object
import os

class TubeHolder:
    def __init__(self, bwidth=160, bheight=80, diameter=16):
        self.bwidth = bwidth
        self.bheight = bheight
        self.diameter = diameter
        self.row = int(self.bwidth / (self.diameter + 10))
        self.corner_radius = self.diameter / 2 + 4
        self.hole = cq.Workplane("XY").circle(self.diameter / 2).extrude(self.bheight - 3).edges("<Z").chamfer(2)
        self.model = self._create_box()

    def _create_box(self):
        box = (
            cq.Workplane("XY")
            .box(self.bwidth, self.bwidth, self.bheight)
            .edges("|Z").fillet(self.corner_radius)
            .edges("<Z").chamfer(2)
        )
        return box

    def add_holes(self):
        wp = self.model
        for i in range(self.row):
            for j in range(self.row):
                x = (j - (self.row - 1) / 2) * (self.bwidth / self.row)
                y = (i - (self.row - 1) / 2) * (self.bwidth / self.row)
                wp = wp.cut(self.hole.translate((x, y, 0)))
        self.model = wp
        return self

    def finalize(self):
        self.model = self.model.edges(">Z").chamfer(1)
        return self

    def export(self, filename):
        self.model.export(f"{filename}")

    def show(self):
        show_object(self.model)

if __name__ == "__main__":
    holder = TubeHolder()
    holder.add_holes().finalize()
    holder.show()
    holder.export(f"tube_holder_{holder.bwidth}x{holder.bwidth}x{holder.bheight}_d{holder.diameter}")