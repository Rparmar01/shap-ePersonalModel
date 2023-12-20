import bpy
import os
import numpy as np

from PIL import Image 

# Set the file paths for the input and output .obj files
input_path = "/content/shap-e/example_mesh_0.obj"
output_path = "/content/shap-e/colored_mesh_0.obj"


# Set the number of iterations and cameras per iteration
num_iterations = 10
num_cameras = 12

# Generate random latents for each iteration
latents = np.random.normal(size=(num_iterations, 512))

# Generate random camera positions for each iteration and camera
cameras = []
for i in range(num_iterations):
    camera_positions = np.random.normal(size=(num_cameras, 3))
    camera_targets = np.zeros((num_cameras, 3))
    camera_ups = np.tile(np.array([0, 1, 0]), (num_cameras, 1))
    cameras.append((camera_positions, camera_targets, camera_ups))

# Create the Vertex_Colors folder if it doesn't exist
vc_dir = os.path.join(os.path.dirname(output_path), "vertex_colors")
if not os.path.exists(vc_dir):
    os.makedirs(vc_dir)

# Get the directory path of the output .obj file  
# output_dir = os.path.dirname(output_path)  

# Append 'Vertex_Colors' to the directory path  
# vc_dir = os.path.join(output_dir, "Vertex_Colors")  
vc_dir = os.path.abspath("vertex_colors")

# Enable write permissions to new directory
os.chmod(vc_dir, 0o777)  

#bpy.ops.import_mesh.obj(filepath=input_path)

# Select the default cube object and delete it  
bpy.ops.object.select_all(action='SELECT')  
bpy.ops.object.delete(use_global=False)  
  
# Import the OBJ file into Blender  
bpy.ops.import_scene.obj(filepath=input_path)  
  
# Rename the imported object to "Mesh"  
bpy.context.selected_objects[0].name = "Mesh"  
  
# Set the active object to the imported object  
bpy.context.scene.objects.active = bpy.context.selected_objects[0]  
  
# Set the object in edit mode  
bpy.ops.object.mode_set(mode='EDIT')  
obj = bpy.context.active_object  

# Create a material for the object
mat = bpy.data.materials.new(name="Material")
obj.data.materials.append(mat)

# Bake the texture into the mesh
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.smart_project(island_margin=0.1)
bpy.ops.object.mode_set(mode='OBJECT')

# Load the PNG files and apply them as textures to the mesh
for i in range(num_iterations):
    for j in range(num_cameras):
        filename = f"color_{i}_{j}.png"
        img_path = os.path.join(vc_dir, filename)
        print("color png path",img_path)
        #Load PNG File
        img = Image.open(img_path)

        #Convert img to RGBA format
        img = img.convert("RGBA")

        #Get image as byte sequence
        data = img.tobytes()

        #img = bpy.data.images.load(img_path)
        
        if not img:
            img = bpy.data.images.new(filename, 64, 64)
        
        tex = bpy.data.textures.new(name=f"Texture_{i}_{j}", type='IMAGE')
        tex.image = img
        
        slot = mat.texture_slots.add()
        slot.texture = tex
        slot.texture_coords = 'UV'

# Set the bake type and bake the texture into the mesh
bpy.context.scene.render.bake_type = 'VERTEX'
bpy.ops.object.bake_image()

# Save the PNG files to the Vertex_Colors folder
for i in range(num_iterations):
    for j in range(num_cameras):
        filename = f"color_{i}_{j}.png"
        img_path = os.path.join(vc_dir, filename).replace("\\", "/") 
        img = bpy.data.images[f"Render Result_{i}_{j}"]
        img.save_render(img_path)

# Export the colored mesh as a new .obj file
bpy.ops.export_scene.obj(filepath=output_path, use_vertex_color=True)
