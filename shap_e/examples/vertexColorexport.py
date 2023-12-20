import bpy

# Open the .obj file
with open("/content/shap-e/example_mesh_0.obj", "r") as f:
    lines = f.readlines()

# Initialize lists for storing vertices and vertex colors
vertices = []
vertex_colors = []

# Iterate over the lines in the file
for line in lines:
    # If the line starts with "v ", it is a vertex position
    if line.startswith("v "):
        # Split the line into its components
        components = line.strip().split(" ")
        # Extract the x, y, and z coordinates of the vertex
        x, y, z = float(components[1]), float(components[2]), float(components[3])
        # Append the vertex to the vertices list
        vertices.append((x, y, z))
    # If the line starts with "vc ", it is a vertex color
    elif line.startswith("vc "):
        # Split the line into its components
        components = line.strip().split(" ")
        # Extract the r, g, and b components of the vertex color
        r, g, b = float(components[1]), float(components[2]), float(components[3])
        # Append the vertex color to the vertex_colors list
        vertex_colors.append((r, g, b))

# Open a new file for writing
output_file_path = "./outputvertexcolor.csv"
try:  
    with open(output_file_path, "w") as f:  
        # Write the header row to the file  
        f.write("X,Y,Z,R,G,B\n")  
        # Iterate over the vertices and vertex colors and write them to the file  
        for i, (x, y, z) in enumerate(vertices):  
            # Check if the vertex_colors list is not empty and has enough elements  
            if vertex_colors and i < len(vertex_colors):  
                r, g, b = vertex_colors[i]  
            else:  
                # If the vertex_colors list is empty or does not have enough elements,  
                # set the vertex color to white  
                r, g, b = 1.0, 1.0, 1.0  
            f.write(f"{x},{y},{z},{r},{g},{b}\n")  
    print(f"Vertex colors saved to {output_file_path}")  
except Exception as e:  
    print(f"Error saving vertex colors to {output_file_path}: {e}")  