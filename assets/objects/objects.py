import numpy as np

def CreateCircle(center, radius, colour, points = 10, offset = 0, semi = False):
    vertices = [center[0], center[1], center[2], colour[0], colour[1], colour[2]]
    indices = []

    if semi == True:
        for i in range(points+1):
            vertices += [
                center[0] + radius * np.cos(float(i * np.pi)/points),
                center[1] + radius * np.sin(float(i * np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]
    else:
        for i in range(points):
            vertices += [
                center[0] + radius * np.cos(float(i * 2* np.pi)/points),
                center[1] + radius * np.sin(float(i * 2* np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points-1 else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]

    return (vertices, indices)    

def CreatePlayer():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [220/255, 183/255, 139/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreateBackground():
    grassColour = [0,1,0]
    waterColour = [0,0,1]

    vertices = [
        -500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        -400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        -400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
    ]

    indices = [
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]

    return vertices, indices

def CreatePlatform():
    # Create a circular platform
    vertices = [0, 0, 0, 0.6, 0.3, 0.0]  # Center point, brown color
    indices = []
    
    # Create circle points
    points = 32  # More points for smoother circle
    for i in range(points):
        angle = 2 * np.pi * i / points
        vertices.extend([
            40 * np.cos(angle), 40 * np.sin(angle), 0,  # Position
            0.6, 0.3, 0.0  # Color (brown)
        ])
        if i < points - 1:
            indices.extend([0, i + 1, i + 2])
        else:
            indices.extend([0, points, 1])  # Close the circle
    
    return vertices, indices

def CreateKey():
    # Create a larger, brighter key
    vertices = [
        0.0,   25.0, 0.0,   1.0, 1.0, 0.0,  # Top, bright yellow color
        25.0,  0.0,  0.0,   1.0, 1.0, 0.0,  # Right
        0.0,   -25.0, 0.0,  1.0, 1.0, 0.0,  # Bottom
        -25.0, 0.0,  0.0,   1.0, 1.0, 0.0,  # Left
    ]
    
    indices = [
        0, 1, 2,  # First triangle
        0, 2, 3,  # Second triangle
    ]
    
    return vertices, indices

def CreateEnemy():
    # Create a red triangle for the enemy
    vertices = [
        0.0,   20.0, 0.0,   1.0, 0.0, 0.0,  # Top, red color
        20.0,  -20.0, 0.0,  1.0, 0.0, 0.0,  # Bottom right
        -20.0, -20.0, 0.0,  1.0, 0.0, 0.0,  # Bottom left
    ]
    
    indices = [0, 1, 2]  # Single triangle
    
    return vertices, indices

def CreateJungleBackground():
    jungleGreen = [0.0, 0.5, 0.0]  # Darker green for jungle
    waterColor = [0.4, 0.494, 0.173]   # #667E2C converted to RGB

    vertices = [
        -500.0, 500.0, -0.9, jungleGreen[0], jungleGreen[1], jungleGreen[2],
        -400.0, 500.0, -0.9, jungleGreen[0], jungleGreen[1], jungleGreen[2],
        -400.0, -500.0, -0.9, jungleGreen[0], jungleGreen[1], jungleGreen[2],
        -500.0, -500.0, -0.9, jungleGreen[0], jungleGreen[1], jungleGreen[2],

        500.0, 500.0, -0.9, jungleGreen[0], jungleGreen[1], jungleGreen[2],
        400.0, 500.0, -0.9, jungleGreen[0], jungleGreen[1], jungleGreen[2],
        400.0, -500.0, -0.9, jungleGreen[0], jungleGreen[1], jungleGreen[2],
        500.0, -500.0, -0.9, jungleGreen[0], jungleGreen[1], jungleGreen[2],

        -400.0, 500.0, -0.9, waterColor[0], waterColor[1], waterColor[2],
        400.0, 500.0, -0.9, waterColor[0], waterColor[1], waterColor[2],
        400.0, -500.0, -0.9, waterColor[0], waterColor[1], waterColor[2],
        -400.0, -500.0, -0.9, waterColor[0], waterColor[1], waterColor[2],
    ]

    indices = [
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]

    return vertices, indices

def CreateLeafPlatform():
    # Create a leaf-shaped platform
    vertices = [0, 0, 0, 0.0, 0.8, 0.0]  # Center point, bright green
    indices = []
    
    # Create leaf shape with more points on one side
    points = 24
    for i in range(points):
        angle = 2 * np.pi * i / points
        # Modify radius to create leaf shape
        radius = 40 * (1 + 0.3 * np.sin(3 * angle))
        vertices.extend([
            radius * np.cos(angle), radius * np.sin(angle), 0,  # Position
            0.0, 0.8, 0.0  # Color (bright green)
        ])
        if i < points - 1:
            indices.extend([0, i + 1, i + 2])
        else:
            indices.extend([0, points, 1])
    
    return vertices, indices

playerVerts, playerInds = CreatePlayer()
playerProps = {
    'vertices' : np.array(playerVerts, dtype = np.float32),
    
    'indices' : np.array(playerInds, dtype = np.uint32),

    'position' : np.array([-0.8, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32)
}

backgroundVerts, backgroundInds = CreateBackground()
backgroundProps = {
    'vertices' : np.array(backgroundVerts, dtype = np.float32),
    
    'indices' : np.array(backgroundInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0]
}

platformVerts, platformInds = CreatePlatform()
platformProps = {
    'vertices': np.array(platformVerts, dtype=np.float32),
    'indices': np.array(platformInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
    'speed': 100.0,  # Movement speed
    'direction': 1,  # 1 for up/right, -1 for down/left
    'movement_type': 'vertical',  # 'vertical' or 'horizontal'
    'bounds': [-300, 300]  # Movement bounds
}

keyVerts, keyInds = CreateKey()
keyProps = {
    'vertices': np.array(keyVerts, dtype=np.float32),
    'indices': np.array(keyInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1.0, 1.0, 1], dtype=np.float32),  # Increased scale
    'collected': False
}

enemyVerts, enemyInds = CreateEnemy()
enemyProps = {
    'vertices': np.array(enemyVerts, dtype=np.float32),
    'indices': np.array(enemyInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
    'movement_type': 'vertical',
    'speed': 200.0,
    'direction': 1,
    'bounds': [-200, 200]  # Y-axis bounds
}