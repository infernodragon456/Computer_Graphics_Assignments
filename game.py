import imgui
import numpy as np
from OpenGL.GL import *  # Add this import for OpenGL functions
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import standard_shader, ui_shader
from assets.objects.objects import (create_transporter, create_pirate, create_planet, 
                                  create_space_station, create_laser, create_arrow, create_crosshair)

class Game:
    def __init__(self, height, width, gui):
        self.gui = gui
        self.height = height
        self.width = width
        self.screen = 0
        self.gameState = {}

    def InitScene(self):
        if self.screen == 1:
            print("\nInitializing Scene:")
            
            # Initialize shaders
            self.shaders = {
                'standard': Shader(standard_shader["vertex_shader"], standard_shader["fragment_shader"]),
                'ui': Shader(ui_shader["vertex_shader"], ui_shader["fragment_shader"])
            }
            print("Shaders initialized")
            
            # Initialize camera with proper lookAt vector
            self.camera = Camera(self.height, self.width)
            self.camera.position = np.array([0, -20, 10], dtype=np.float32)
            self.camera.lookAt = np.array([0, 0, 0], dtype=np.float32)  # Look at origin
            print(f"Camera initialized at position {self.camera.position}, looking at {self.camera.lookAt}")
            
            # Define world boundaries
            self.worldMin = np.array([-5000, -5000, -5000], dtype=np.float32)
            self.worldMax = np.array([5000, 5000, 5000], dtype=np.float32)
            
            # Set up light position
            self.lightPos = np.array([1000, 1000, 1000], dtype=np.float32)
            print(f"Light position set to {self.lightPos}")
            
            # Initialize transporter
            print("\nCreating objects:")
            transporter_vertices, transporter_indices = create_transporter()
            print(f"Transporter mesh created with {len(transporter_vertices)/6} vertices")
            self.gameState["transporter"] = Object("transporter", self.shaders['standard'], {
                'vertices': transporter_vertices,
                'indices': transporter_indices,
                'position': np.array([0, 0, 0], dtype=np.float32),
                'rotation': np.array([0, 0, np.pi/2], dtype=np.float32),  # Back to original: 90 degrees around Z
                'scale': np.array([0.5, 0.5, 0.5], dtype=np.float32),
                'colour': np.array([0.7, 0.7, 0.9, 1.0], dtype=np.float32),
                'velocity': np.array([0, 0, 0], dtype=np.float32),
                'view': 1
            })
            print("Transporter initialized")

            # Initialize planets and space stations
            self.n_planets = 5  # Reduced number for testing
            self.gameState["planets"] = []
            self.gameState["spaceStations"] = []
            
            planet_vertices, planet_indices = create_planet()
            station_vertices, station_indices = create_space_station()
            
            # Create planets at random positions
            for i in range(self.n_planets):
                # Random position within world bounds (but not too close to center)
                min_dist = 100  # Minimum distance from center
                max_dist = 500  # Maximum distance from center
                
                angle = np.random.uniform(0, 2 * np.pi)
                distance = np.random.uniform(min_dist, max_dist)
                height = np.random.uniform(-200, 200)
                
                position = np.array([
                    distance * np.cos(angle),
                    distance * np.sin(angle),
                    height
                ], dtype=np.float32)
                
                # Create planet
                planet = Object("planet", self.shaders['standard'], {
                    'vertices': planet_vertices,
                    'indices': planet_indices,
                    'position': position,
                    'rotation': np.random.uniform(0, 2 * np.pi, 3),
                    'scale': np.array([20, 20, 20], dtype=np.float32),
                    'colour': np.array([
                        np.random.uniform(0.3, 0.8),
                        np.random.uniform(0.2, 0.5),
                        np.random.uniform(0.2, 0.5),
                        1.0
                    ], dtype=np.float32)
                })
                self.gameState["planets"].append(planet)
                
                # Create space station orbiting the planet
                orbit_radius = 30  # Distance from planet
                station_angle = np.random.uniform(0, 2 * np.pi)
                station_pos = position + np.array([
                    orbit_radius * np.cos(station_angle),
                    orbit_radius * np.sin(station_angle),
                    10
                ], dtype=np.float32)
                
                station = Object("spacestation", self.shaders['standard'], {
                    'vertices': station_vertices,
                    'indices': station_indices,
                    'position': station_pos,
                    'rotation': np.array([0, station_angle, 0], dtype=np.float32),
                    'scale': np.array([5, 5, 5], dtype=np.float32),
                    'colour': np.array([0.8, 0.8, 0.8, 1.0], dtype=np.float32),
                    'orbit_center': position,
                    'orbit_radius': orbit_radius,
                    'orbit_angle': station_angle,
                    'orbit_speed': 0.001  # Radians per frame
                })
                self.gameState["spaceStations"].append(station)
            
            print(f"Created {self.n_planets} planets with space stations")

            # Initialize minimap arrow
            arrow_vertices, arrow_indices = create_arrow()
            self.gameState["arrow"] = Object("arrow", self.shaders['ui'], {
                'vertices': arrow_vertices,
                'indices': arrow_indices,
                'position': np.array([0.8, -0.8, 0], dtype=np.float32),  # Bottom right corner
                'rotation': np.array([0, 0, 0], dtype=np.float32),
                'scale': np.array([0.1, 0.1, 0.1], dtype=np.float32),
                'colour': np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
            })

            # Initialize crosshair
            crosshair_vertices, crosshair_indices = create_crosshair()
            self.gameState["crosshair"] = Object("crosshair", self.shaders['ui'], {
                'vertices': crosshair_vertices,
                'indices': crosshair_indices,
                'position': np.array([0, 0, 0], dtype=np.float32),
                'rotation': np.array([0, 0, 0], dtype=np.float32),
                'scale': np.array([1, 1, 1], dtype=np.float32),
                'colour': np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
            })

            print("\nScene initialization complete")

    def ProcessFrame(self, inputs, time):
        self.UpdateScene(inputs, time)
        self.DrawScene()
        self.DrawText()

    def DrawText(self):
        if self.screen == 0:  # Start screen
            window_w, window_h = 400, 200
            x_pos = (self.width - window_w) / 2
            y_pos = (self.height - window_h) / 2

            imgui.new_frame()
            imgui.set_next_window_position(x_pos, y_pos)
            imgui.set_next_window_size(window_w, window_h)
            imgui.begin("Main Menu", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

            imgui.set_cursor_pos_x((window_w - imgui.calc_text_size("Press 1: New Game")[0]) / 2)
            imgui.text("Press 1: New Game")

            imgui.end()
            imgui.render()
            self.gui.render(imgui.get_draw_data())

    def UpdateScene(self, inputs, time):
        if self.screen == 0:  # Start screen
            if inputs["1"]:
                self.screen = 1
                self.InitScene()
        
        if self.screen == 1:  # Game screen
            # Update space stations orbits
            if "spaceStations" in self.gameState:
                for station in self.gameState["spaceStations"]:
                    # Update orbit angle
                    station.properties["orbit_angle"] += station.properties["orbit_speed"]
                    
                    # Calculate new position
                    center = station.properties["orbit_center"]
                    radius = station.properties["orbit_radius"]
                    angle = station.properties["orbit_angle"]
                    
                    station.properties["position"] = center + np.array([
                        radius * np.cos(angle),
                        radius * np.sin(angle),
                        10
                    ], dtype=np.float32)
                    
                    # Update rotation to face orbit direction
                    station.properties["rotation"][1] = angle

            if "transporter" in self.gameState:
                transporter = self.gameState["transporter"]
                
                # Rotation speeds (in radians per frame)
                rotation_speed = 0.05
                
                # Calculate current nose direction before rotation
                forward = np.array([0, 1, 0], dtype=np.float32)  # Base forward vector
                yaw = transporter.properties["rotation"][1]
                pitch = transporter.properties["rotation"][0]
                roll = transporter.properties["rotation"][2]
                
                # Create rotation matrices
                yaw_matrix = np.array([
                    [np.cos(yaw), 0, np.sin(yaw)],
                    [0, 1, 0],
                    [-np.sin(yaw), 0, np.cos(yaw)]
                ], dtype=np.float32)
                
                pitch_matrix = np.array([
                    [1, 0, 0],
                    [0, np.cos(pitch), -np.sin(pitch)],
                    [0, np.sin(pitch), np.cos(pitch)]
                ], dtype=np.float32)
                
                roll_matrix = np.array([
                    [np.cos(roll), -np.sin(roll), 0],
                    [np.sin(roll), np.cos(roll), 0],
                    [0, 0, 1]
                ], dtype=np.float32)
                
                # Calculate current nose direction
                nose_direction = roll_matrix @ pitch_matrix @ yaw_matrix @ forward
                print(f"Current nose direction: {nose_direction}")
                
                # Handle rotations
                if inputs["W"]:  # Pitch up
                    print("W pressed - Attempting to pitch up")
                    transporter.properties["rotation"][1] -= rotation_speed  # Use Y-axis for pitch, inverted
                    print(f"New rotation: {transporter.properties['rotation']}")
                if inputs["S"]:  # Pitch down
                    print("S pressed - Attempting to pitch down")
                    transporter.properties["rotation"][1] += rotation_speed  # Use Y-axis for pitch, inverted
                    print(f"New rotation: {transporter.properties['rotation']}")
                if inputs["A"]:  # Yaw left
                    transporter.properties["rotation"][2] += rotation_speed  # Use Z-axis for yaw
                if inputs["D"]:  # Yaw right
                    transporter.properties["rotation"][2] -= rotation_speed  # Use Z-axis for yaw
                if inputs["Q"]:  # Roll clockwise
                    transporter.properties["rotation"][0] -= rotation_speed  # Use X-axis for roll, inverted
                if inputs["E"]:  # Roll counterclockwise
                    transporter.properties["rotation"][0] += rotation_speed  # Use X-axis for roll, inverted

                # Calculate new nose direction after rotation
                yaw = transporter.properties["rotation"][1]
                pitch = transporter.properties["rotation"][0]
                roll = transporter.properties["rotation"][2]
                
                yaw_matrix = np.array([
                    [np.cos(yaw), 0, np.sin(yaw)],
                    [0, 1, 0],
                    [-np.sin(yaw), 0, np.cos(yaw)]
                ], dtype=np.float32)
                
                pitch_matrix = np.array([
                    [1, 0, 0],
                    [0, np.cos(pitch), -np.sin(pitch)],
                    [0, np.sin(pitch), np.cos(pitch)]
                ], dtype=np.float32)
                
                roll_matrix = np.array([
                    [np.cos(roll), -np.sin(roll), 0],
                    [np.sin(roll), np.cos(roll), 0],
                    [0, 0, 1]
                ], dtype=np.float32)
                
                new_nose_direction = roll_matrix @ pitch_matrix @ yaw_matrix @ forward
                print(f"New nose direction: {new_nose_direction}")

                # Handle forward movement (only on SPACE)
                if inputs["SPACE"]:
                    # Calculate forward direction based on current rotation
                    forward = np.array([0, 1, 0], dtype=np.float32)  # Base forward vector (pointing along Y)
                    
                    # Create rotation matrices
                    # Yaw (Y-axis rotation)
                    yaw = transporter.properties["rotation"][1]
                    yaw_matrix = np.array([
                        [np.cos(yaw), 0, np.sin(yaw)],
                        [0, 1, 0],
                        [-np.sin(yaw), 0, np.cos(yaw)]
                    ], dtype=np.float32)
                    
                    # Pitch (X-axis rotation)
                    pitch = transporter.properties["rotation"][0]
                    pitch_matrix = np.array([
                        [1, 0, 0],
                        [0, np.cos(pitch), -np.sin(pitch)],
                        [0, np.sin(pitch), np.cos(pitch)]
                    ], dtype=np.float32)
                    
                    # Apply rotations to get forward direction
                    # Note: Roll doesn't affect forward direction
                    forward = yaw_matrix @ pitch_matrix @ forward
                    
                    # Update velocity (with speed limit)
                    acceleration = 0.1
                    max_speed = 2.0
                    
                    new_velocity = transporter.properties["velocity"] + forward * acceleration
                    speed = np.linalg.norm(new_velocity)
                    if speed > max_speed:
                        new_velocity = (new_velocity / speed) * max_speed
                    
                    transporter.properties["velocity"] = new_velocity
                
                # Apply velocity to position
                transporter.properties["position"] += transporter.properties["velocity"]
                
                # Add drag to slow down when not accelerating
                drag = 0.99
                transporter.properties["velocity"] *= drag

                # Keep camera static for now
                """
                # Update camera to follow transporter
                camera_distance = 20
                camera_height = 10
                
                # Calculate camera position based on transporter's rotation
                # Start with base offset (behind and above)
                camera_offset = np.array([0, -camera_distance, camera_height], dtype=np.float32)
                
                # Create rotation matrices for camera
                # Yaw (Y-axis rotation)
                yaw = transporter.properties["rotation"][1]  # Use current yaw
                yaw_matrix = np.array([
                    [np.cos(yaw), 0, np.sin(yaw)],
                    [0, 1, 0],
                    [-np.sin(yaw), 0, np.cos(yaw)]
                ], dtype=np.float32)
                
                # Pitch (X-axis rotation)
                pitch = transporter.properties["rotation"][0]  # Use current pitch
                pitch_matrix = np.array([
                    [1, 0, 0],
                    [0, np.cos(pitch), -np.sin(pitch)],
                    [0, np.sin(pitch), np.cos(pitch)]
                ], dtype=np.float32)
                
                # Apply rotations to camera offset
                # Apply yaw first, then pitch
                rotated_offset = yaw_matrix @ pitch_matrix @ camera_offset
                
                # Update camera position and look target
                self.camera.position = transporter.properties["position"] + rotated_offset
                self.camera.lookAt = transporter.properties["position"]
                """

    def DrawScene(self):
        if self.screen == 1:
            # Update camera for standard shader
            self.camera.Update(self.shaders['standard'])
            
            # Set lighting uniforms for standard shader
            self.shaders['standard'].Use()
            lightPosLoc = glGetUniformLocation(self.shaders['standard'].ID, "lightPos".encode('utf-8'))
            viewPosLoc = glGetUniformLocation(self.shaders['standard'].ID, "viewPos".encode('utf-8'))
            
            if lightPosLoc == -1 or viewPosLoc == -1:
                print("Warning: Could not find light/view position uniforms in shader")
            
            glUniform3f(lightPosLoc, self.lightPos[0], self.lightPos[1], self.lightPos[2])
            glUniform3f(viewPosLoc, self.camera.position[0], self.camera.position[1], self.camera.position[2])
            
            # Draw planets
            if "planets" in self.gameState:
                for planet in self.gameState["planets"]:
                    planet.Draw()
            
            # Draw space stations
            if "spaceStations" in self.gameState:
                for station in self.gameState["spaceStations"]:
                    station.Draw()
            
            # Draw transporter
            if "transporter" in self.gameState:
                self.gameState["transporter"].Draw()
            
            # Draw UI elements
            if "arrow" in self.gameState:
                self.gameState["arrow"].Draw()
            
            if "crosshair" in self.gameState and self.gameState["transporter"].properties["view"] == 2:
                self.gameState["crosshair"].Draw()

