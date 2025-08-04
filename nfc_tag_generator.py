import cadquery as cq
from ocp_vscode import show_object
import os

class NFCTagGenerator:
    def __init__(
        self,
        width=30,
        height=30,
        thickness=3,
        circle_radius=1.5,
        nfc_diameter=20,
        export_folder="nfc_tags"
    ):
        self.width = width
        self.height = height
        self.thickness = thickness
        self.circle_radius = circle_radius
        self.nfc_diameter = nfc_diameter
        self.export_folder = export_folder

    def create_nfc_tag_base(self):
        if self.width < (self.nfc_diameter + 2) or self.height < (self.nfc_diameter + 2):
            raise ValueError("Width and height must be at least 2mm larger than the NFC diameter.")
        tag = (
            cq.Workplane("XY")
            .box(self.width, self.height, self.thickness)
            .edges("|Z")
            .fillet(3)
        )
        hole = (
            cq.Workplane("XY")
            .circle(self.circle_radius)
            .extrude(self.thickness + 1)
            .translate((self.width/2 - self.circle_radius*2, self.height/2 - self.circle_radius*2, -self.thickness / 2))
        )
        tag = tag.cut(hole).faces("#Z").chamfer(0.6)
        nfc_insert = (
            cq.Workplane("XY")
            .circle(self.nfc_diameter / 2)
            .extrude(1)
            .translate((0, 0, -0.5))
        )
        tag = tag.cut(nfc_insert)
        return tag

    @staticmethod
    def format_text(text, max_length=20, chunk_size=10):
        if len(text) > max_length:
            text = text[:max_length-1] + "…"
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        return "\n".join(chunks)

    def add_text_to_nfc_tag(self, tag, text="NFC\nTag", font_size=4):
        text = self.format_text(text)
        tag = tag.faces(">Z").workplane().text(text, font_size, -0.6)
        return tag

    def generate_tags(self, texts):
        tags = []
        for text in texts:
            tag = self.create_nfc_tag_base()
            tag = self.add_text_to_nfc_tag(tag, text)
            tags.append(tag)
        return tags

    def distribute_tags(self, tags, rows=3, cols=3, spacing=None):
        if spacing is None:
            spacing = self.height / 2 + 3
        distributed_tags = []
        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j
                if idx < len(tags):
                    tag = tags[idx]
                    tag = tag.translate((
                        j * (tag.val().BoundingBox().xmax + spacing),
                        i * (tag.val().BoundingBox().ymax + spacing),
                        0
                    ))
                    distributed_tags.append(tag)
        return distributed_tags

    def export_tag(self, tag, filename):
        tag.export(filename)

    def ensure_export_folder(self):
        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)

if __name__ == "__main__":
    generator = NFCTagGenerator()
    generator.ensure_export_folder()
    nfc_tags = generator.generate_tags(["NFC Tag 1", "NFC Tag 2", "NFC Tag 3"])
    nfc_tags = generator.distribute_tags(nfc_tags)
    for idx, nfc_tag in enumerate(nfc_tags):
        show_object(nfc_tag)
        generator.export_tag(nfc_tag, f"{generator.export_folder}/nfc_tag_{idx}.stl")