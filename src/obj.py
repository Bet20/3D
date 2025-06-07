import trimesh
import numpy as np
from datetime import datetime

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

def export_to_obj(meshes, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mesh_export_{timestamp}.obj"
    
    valid_meshes = [mesh for mesh in meshes if len(mesh) > 1]
    
    if not valid_meshes:
        print("No valid meshes to export.")
        return
    
    scene = trimesh.Scene()
    
    for mesh_coords in valid_meshes:
        points = np.array(mesh_coords)
        edges = np.column_stack((np.arange(len(points) - 1), np.arange(1, len(points))))
        
        line_mesh = trimesh.Trimesh(
            vertices=points,
            faces=edges,
            process=False
        )
        
        scene.add_geometry(line_mesh)
    
    try:
        combined = trimesh.util.concatenate(scene.dump())
        combined.export(filename)
        print(f"Mesh exported to {filename}")
        return filename
    except Exception as e:
        print(f"Error exporting mesh: {e}")
        return None

