import cadquery as cq
from ocp_vscode import show_object
import math

# User's Parameters
tube1_diameter = 12  # mm, outer diameter of the tube
tube2_diameter = 10  # mm, outer diameter of the tube
thickness = 2  # mm, thickness of the tube wall
length = 30    # mm, length of the tube
ribs = True  # if true, add ribs to the tube

def create_socket(tube_diameter, length, thickness, ribs=False):
    socket = (
        cq.Workplane("XY")
        .circle(tube_diameter / 2)
        .extrude(length)
        .faces("<Z")
        .chamfer(thickness / 2)  # Add a chamfer to the top edge
    )
    hole = (
        cq.Workplane("XY")
        .circle((tube_diameter - 2*thickness) / 2)
        .extrude(length)
    )
    def create_rib():
        return (
            cq.Workplane("XY")
            .circle(tube_diameter / 2)
            .extrude(2, taper=-30)
        )

    
    if ribs:
        # Add ribs to the socket
        num_ribs = 3  # Number of ribs
        for i in range(1, num_ribs+1):
            rib = create_rib()
            # Position the rib at equal intervals along the length of the socket
            rib = rib.translate((0, 0, i * (length*(2/3) / num_ribs)))
            socket = socket.union(rib)
    # Cut the hole in the socket

    socket = socket.cut(hole)
    #new_socket = socket.mirror("XY").translate((0, 0, 2*length))
    #socket = socket.union(new_socket)

    return socket

def create_adapter(tube1_diameter, tube2_diameter, length, thickness, transition_angle=45, ribs=True):
    
    # Ensure the tube diameters are greater than the thickness
    if tube1_diameter <= 2 * thickness or tube2_diameter <= 2 * thickness:
        raise ValueError("Tube diameters must be greater than twice the thickness.")
    if tube1_diameter < tube2_diameter:
        raise ValueError("Tube 1 diameter must be greater or equal than Tube 2 diameter.")
    # Create the transition section
    if tube1_diameter == tube2_diameter:
        transition_length = 1
    else:
        transition_length =  (tube1_diameter - tube2_diameter) / 2 / math.tan(math.radians(transition_angle))
    transition = (
        cq.Workplane("XY")
        .circle(tube1_diameter / 2)
        .workplane(offset=transition_length)
        .circle(tube2_diameter / 2)
        .loft()
        .translate((0, 0, length))
    )
    hole_transition = (
        cq.Workplane("XY")
        .circle(tube1_diameter / 2- thickness)
        .workplane(offset=transition_length)
        .circle(tube2_diameter / 2- thickness)
        .loft()
        .translate((0, 0, length))
    )
    transition = transition.cut(hole_transition)
    # Create the first socket
    socket1 = create_socket(tube1_diameter, length, thickness, ribs)
    # Create the second socket
    socket2 = create_socket(tube2_diameter, length, thickness, ribs)
    # Position the second socket at the end of the first one
    socket2 = socket2.mirror("XY").translate((0, 0, 2*length+transition_length))
    # Combine both sockets
    adapter = socket1.union(transition).union(socket2)
    return adapter

show_object(create_adapter(tube1_diameter, tube2_diameter, length, thickness), "Silicone Tube Connector")