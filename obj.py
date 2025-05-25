import trimesh
import numpy as np

def generate_visualization(meshes):
    valid_meshes = [mesh for mesh in meshes if len(mesh) > 1]
    
    if not valid_meshes:
        print("No valid meshes to visualize. Please draw at least one mesh with more than one point.")
        return
    
    scene = trimesh.Scene()
    
    for mesh_coords in valid_meshes:
        points = np.array(mesh_coords)
        
        if len(points) < 2:
            continue
            
        edges = np.column_stack((np.arange(len(points) - 1), np.arange(1, len(points))))
        
        path = trimesh.path.Path3D(entities=[
            trimesh.path.entities.Line(e) for e in edges
        ], vertices=points, colors=[(0, 255, 0)] * len(edges))
        
        scene.add_geometry(path)
    
    scene.show()

