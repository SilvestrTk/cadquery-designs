import cadquery as cq
from ocp_vscode import show_object
import math

# User's Parameters
keychainLength = 50     # mm
keychainWidth = 20      # mm
keychainThickness = 3   # mm
keychainText = "Some cool"  # Text to engrave on the keychain

# Function to create the keychain
def create_keychain():
    global keychainText
    # Create the base rectangle for the keychain
    keychain = (
        cq.Workplane("XY")
        .rect(keychainLength, keychainWidth)
        .extrude(keychainThickness)
        .edges("|Z")
        .fillet(3)  # Fillet the edges for a smoother finish
    )
    offset = (
        cq.Workplane("XY")
        .rect(keychainLength, keychainWidth)
        .extrude(0.6)
        .edges("|Z")
        .fillet(3)
        .faces("|Z")
        .shell(-1)
        .translate((0, 0, keychainThickness))
    )
    keychain = keychain.union(offset)
    # Add a hole for the keyring
    hole = (
        cq.Workplane("XY")
        .workplane(offset=keychainThickness / 2)
        .circle(1.5)  # radius of the hole for the keyring
        .extrude(-(keychainThickness+6))  # Extrude downwards
        .translate((keychainLength / 2 - 3, keychainWidth / 2 - 3, keychainThickness+1))  # Position the hole
    )
    keychain = keychain.cut(hole)

    # Add a small chamfer to the hole
    keychain = keychain.edges("<Z").chamfer(0.5)

    #format text: ensure the text is not longer than the MAX_TEXT_LENGTH and wrap if necessary (priority by the spaces, if not possible divide the word)
    MAX_TEXT_LENGTH = 20
    if len(keychainText) > MAX_TEXT_LENGTH:
        print(f"Warning: Keychain text is too long ({len(keychainText)} characters). It will be truncated to {MAX_TEXT_LENGTH} characters.")
        keychainText = keychainText[:MAX_TEXT_LENGTH]
    MAX_LINE_LENGTH = 10
    lines = []
    for word in keychainText.split():
        #if word length is greater than MAX_LINE_LENGTH, split it into smaller parts
        while len(word) > MAX_LINE_LENGTH:
            lines.append(word[:MAX_LINE_LENGTH])
            word = word[MAX_LINE_LENGTH:]
        if len(lines) == 0 or len(lines[-1]) + len(word) + 1 > MAX_LINE_LENGTH:
            lines.append(word)
        else:
            lines[-1] += " " + word
    if len(lines) > 2:
        lines = lines[:2]

    keychainText = "\n".join(lines)
    fontsize = 8 if len(lines) == 1 else 6

    # Add text engraving
    text = (
        cq.Workplane("XY")
        .workplane(offset=keychainThickness / 2)
        .text(keychainText, fontsize, 0.6, 0.5, "center", "center")
        .translate((0, 0, keychainThickness / 2))
    )

    keychain = keychain.union(text)
    return keychain


show_object(create_keychain(), "Keychain")