######################################################
# Write other shaders for minimap and crosshair (Since they need orthographic projection)

# Standard shader with diffuse lighting
standard_shader = {
    "vertex_shader": '''
        #version 330 core
        layout(location = 0) in vec3 vertexPosition;
        layout(location = 1) in vec3 vertexNormal;

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform float focalLength;

        out vec3 Normal;
        out vec3 FragPos;

        void main() {
            vec4 camCoordPos = viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * vec4(focalLength * (camCoordPos[0] / abs(camCoordPos[2])), 
                                                focalLength * (camCoordPos[1] / abs(camCoordPos[2])), 
                                                camCoordPos[2], 1.0);
            
            FragPos = vec3(modelMatrix * vec4(vertexPosition, 1.0));
            Normal = mat3(transpose(inverse(modelMatrix))) * vertexNormal;
        }
    ''',

    "fragment_shader": '''
        #version 330 core
        out vec4 outputColour;

        in vec3 Normal;
        in vec3 FragPos;

        uniform vec4 objectColour;
        uniform vec3 lightPos;
        uniform vec3 viewPos;

        void main() {
            // Ambient
            float ambientStrength = 0.3;
            vec3 ambient = ambientStrength * vec3(1.0, 1.0, 1.0);

            // Diffuse
            vec3 norm = normalize(Normal);
            vec3 lightDir = normalize(lightPos - FragPos);
            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse = diff * vec3(1.0, 1.0, 1.0);

            vec3 result = (ambient + diffuse) * objectColour.rgb;
            outputColour = vec4(result, objectColour.a);
        }
    '''
}

# Orthographic shader for UI elements (minimap arrow and crosshair)
ui_shader = {
    "vertex_shader": '''
        #version 330 core
        layout(location = 0) in vec3 vertexPosition;

        uniform mat4 modelMatrix;
        
        void main() {
            gl_Position = modelMatrix * vec4(vertexPosition, 1.0);
        }
    ''',

    "fragment_shader": '''
        #version 330 core
        out vec4 outputColour;
        uniform vec4 objectColour;

        void main() {
            outputColour = objectColour;
        }
    '''
}
######################################################