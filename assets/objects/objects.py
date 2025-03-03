import numpy as np
import os

###############################################################
# Write logic to load OBJ Files:
    # Will depend on type of object. For example if normals needed along with vertex positions 
    # then will need to load slightly differently.

# Can use the provided OBJ files from assignment_2_template/assets/objects/models/
# Can also download other assets or model yourself in modelling softwares like blender

###############################################################
# Create Transporter, Pirates, Stars(optional), Minimap arrow, crosshair, planet, spacestation, laser

def load_obj_file(file_path):
    vertices = []
    normals = []
    indices = []
    
    # Dictionary to store unique vertex-normal combinations
    vertex_dict = {}
    vertex_count = 0
    
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):  # Vertex position
                # Split line and convert to float, removing the 'v' prefix
                v = list(map(float, line.strip().split()[1:]))
                vertices.append(v)
            elif line.startswith('vn '):  # Vertex normal
                # Split line and convert to float, removing the 'vn' prefix
                vn = list(map(float, line.strip().split()[1:]))
                normals.append(vn)
            elif line.startswith('f '):  # Face
                # Split line and get vertex/normal indices, removing the 'f' prefix
                face = line.strip().split()[1:]
                triangle = []
                for vertex in face:
                    # OBJ files can have different formats for faces
                    # We're interested in vertex/texture/normal format or just vertex/normal
                    parts = vertex.split('/')
                    v_idx = int(parts[0]) - 1  # OBJ indices start at 1
                    # If normal index is present, use it
                    vn_idx = int(parts[-1]) - 1 if len(parts) > 1 and parts[-1] else 0
                    
                    # Create a unique key for this vertex-normal combination
                    key = (v_idx, vn_idx)
                    
                    # If we haven't seen this combination before, add it
                    if key not in vertex_dict:
                        vertex_dict[key] = vertex_count
                        vertex_count += 1
                    
                    triangle.append(vertex_dict[key])
                
                # Add triangles (handles both triangular and quad faces)
                indices.extend(triangle[:3])
                if len(triangle) == 4:  # Quad face
                    indices.extend([triangle[0], triangle[2], triangle[3]])

    # Create final vertex array with positions and normals interleaved
    final_vertices = []
    for (v_idx, vn_idx), _ in vertex_dict.items():
        final_vertices.extend(vertices[v_idx])  # Position
        final_vertices.extend(normals[vn_idx])  # Normal

    return np.array(final_vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def create_transporter():
    model_path = os.path.join("assets", "objects", "models", "transporter.obj")
    return load_obj_file(model_path)

def create_pirate():
    model_path = os.path.join("assets", "objects", "models", "pirate.obj")
    return load_obj_file(model_path)

def create_planet():
    model_path = os.path.join("assets", "objects", "models", "planet.obj")
    return load_obj_file(model_path)

def create_space_station():
    model_path = os.path.join("assets", "objects", "models", "spacestation.obj")
    return load_obj_file(model_path)

def create_laser():
    # Create a simple elongated cube for laser beam
    # Each vertex has position (3 floats) followed by normal (3 floats)
    vertices = np.array([
        # Front face - positions and normals
        -0.1,  0.1,  1.0,   0.0, 0.0, 1.0,  # top-right
         0.1,  0.1,  1.0,   0.0, 0.0, 1.0,  # top-left
         0.1, -0.1,  1.0,   0.0, 0.0, 1.0,  # bottom-left
        -0.1, -0.1,  1.0,   0.0, 0.0, 1.0,  # bottom-right
        
        # Back face - positions and normals
        -0.1,  0.1, -1.0,   0.0, 0.0, -1.0,  # top-right
         0.1,  0.1, -1.0,   0.0, 0.0, -1.0,  # top-left
         0.1, -0.1, -1.0,   0.0, 0.0, -1.0,  # bottom-left
        -0.1, -0.1, -1.0,   0.0, 0.0, -1.0,  # bottom-right
        
        # Top face - positions and normals
        -0.1,  0.1, -1.0,   0.0, 1.0, 0.0,  # back-right
         0.1,  0.1, -1.0,   0.0, 1.0, 0.0,  # back-left
         0.1,  0.1,  1.0,   0.0, 1.0, 0.0,  # front-left
        -0.1,  0.1,  1.0,   0.0, 1.0, 0.0,  # front-right
        
        # Bottom face - positions and normals
        -0.1, -0.1, -1.0,   0.0, -1.0, 0.0,  # back-right
         0.1, -0.1, -1.0,   0.0, -1.0, 0.0,  # back-left
         0.1, -0.1,  1.0,   0.0, -1.0, 0.0,  # front-left
        -0.1, -0.1,  1.0,   0.0, -1.0, 0.0,  # front-right
        
        # Right face - positions and normals
         0.1,  0.1, -1.0,   1.0, 0.0, 0.0,  # back-top
         0.1, -0.1, -1.0,   1.0, 0.0, 0.0,  # back-bottom
         0.1, -0.1,  1.0,   1.0, 0.0, 0.0,  # front-bottom
         0.1,  0.1,  1.0,   1.0, 0.0, 0.0,  # front-top
        
        # Left face - positions and normals
        -0.1,  0.1, -1.0,  -1.0, 0.0, 0.0,  # back-top
        -0.1, -0.1, -1.0,  -1.0, 0.0, 0.0,  # back-bottom
        -0.1, -0.1,  1.0,  -1.0, 0.0, 0.0,  # front-bottom
        -0.1,  0.1,  1.0,  -1.0, 0.0, 0.0,  # front-top
    ], dtype=np.float32)
    
    # Define indices for the cube (6 faces, 2 triangles each, 3 vertices per triangle)
    indices = np.array([
        0, 1, 2, 2, 3, 0,       # Front face
        4, 5, 6, 6, 7, 4,       # Back face
        8, 9, 10, 10, 11, 8,    # Top face
        12, 13, 14, 14, 15, 12, # Bottom face
        16, 17, 18, 18, 19, 16, # Right face
        20, 21, 22, 22, 23, 20  # Left face
    ], dtype=np.uint32)
    
    return vertices, indices

def create_arrow():
    # Simple 2D arrow for minimap
    vertices = np.array([
        0.0,  0.5, 0.0,  0.0, 0.0, 1.0,  # Top
       -0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  # Bottom left
        0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  # Bottom right
    ], dtype=np.float32)
    
    indices = np.array([0, 1, 2], dtype=np.uint32)
    
    return vertices, indices

def create_crosshair():
    # Simple crosshair (plus sign)
    size = 0.03
    vertices = np.array([
        # Vertical line
        -size/2, -size*2, 0.0,  0.0, 0.0, 1.0,
         size/2, -size*2, 0.0,  0.0, 0.0, 1.0,
         size/2,  size*2, 0.0,  0.0, 0.0, 1.0,
        -size/2,  size*2, 0.0,  0.0, 0.0, 1.0,
        # Horizontal line
        -size*2, -size/2, 0.0,  0.0, 0.0, 1.0,
         size*2, -size/2, 0.0,  0.0, 0.0, 1.0,
         size*2,  size/2, 0.0,  0.0, 0.0, 1.0,
        -size*2,  size/2, 0.0,  0.0, 0.0, 1.0,
    ], dtype=np.float32)
    
    indices = np.array([
        0, 1, 2, 2, 3, 0,  # Vertical
        4, 5, 6, 6, 7, 4   # Horizontal
    ], dtype=np.uint32)
    
    return vertices, indices

###############################################################