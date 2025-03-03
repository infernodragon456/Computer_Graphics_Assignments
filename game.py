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
        self.gameState = {
            "transporter": None,
            "pirates": [],
            "planets": [],
            "spacestations": [],
            "lasers": [],
            "crosshair": None,
            "destination": None,  # Will store the destination space station
            "game_won": False,    # Flag to track if player has reached destination
            "direction_angle": 0  # Angle for the direction indicator
        }

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
            self.camera.position = np.array([-20, 0, 10], dtype=np.float32)
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
                'rotation': np.array([0, 0, 0], dtype=np.float32),  # 90 degrees around Y and Z
                'scale': np.array([0.5, 0.5, 0.5], dtype=np.float32),
                'colour': np.array([0.7, 0.7, 0.9, 1.0], dtype=np.float32),
                'velocity': np.array([0, 0, 0], dtype=np.float32),
                'view': 1
            })
            print("Transporter initialized")

            # Initialize planets and space stations
            self.n_planets = 5  # Reduced number for testing
            self.gameState["planets"] = []
            self.gameState["spacestations"] = []
            
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
                    'scale': np.array([2, 2, 2], dtype=np.float32),
                    'colour': np.array([0.8, 0.8, 0.8, 1.0], dtype=np.float32),
                    'orbit_center': position,
                    'orbit_radius': orbit_radius,
                    'orbit_angle': station_angle,
                    'orbit_speed': 0.001  # Radians per frame
                })
                self.gameState["spacestations"].append(station)
            
            print(f"Created {self.n_planets} planets with space stations")

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

            # Select a random space station as destination
            if self.gameState["spacestations"]:
                self.gameState["destination"] = np.random.choice(self.gameState["spacestations"])
                # Make the destination station a different color (green)
                self.gameState["destination"].properties["colour"] = np.array([0.0, 1.0, 0.0, 1.0], dtype=np.float32)

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

            imgui.set_cursor_pos_x((window_w - imgui.calc_text_size("Press 2: Exit")[0]) / 2)
            imgui.text("Press 2: Exit")

            imgui.end()
            imgui.render()
            self.gui.render(imgui.get_draw_data())

        # Add direction indicator to DrawText method
        if self.screen == 1 and self.gameState["destination"]:
            # Draw direction indicator in bottom right
            indicator_size = 80
            x_pos = self.width - indicator_size - 20  # 20px padding from right edge
            y_pos = self.height - indicator_size - 20  # 20px padding from bottom edge
            
            # Create a new ImGui window for the indicator
            imgui.new_frame()
            imgui.set_next_window_position(x_pos, y_pos)
            imgui.set_next_window_size(indicator_size, indicator_size)
            imgui.begin("Direction", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
            
            # Calculate direction text based on angle
            angle_degrees = np.degrees(self.gameState["direction_angle"]) % 360
            
            # Determine cardinal direction
            if 22.5 <= angle_degrees < 67.5:
                direction_text = "NE →"
            elif 67.5 <= angle_degrees < 112.5:
                direction_text = "N ↑"
            elif 112.5 <= angle_degrees < 157.5:
                direction_text = "NW ←"
            elif 157.5 <= angle_degrees < 202.5:
                direction_text = "W ←"
            elif 202.5 <= angle_degrees < 247.5:
                direction_text = "SW ←"
            elif 247.5 <= angle_degrees < 292.5:
                direction_text = "S ↓"
            elif 292.5 <= angle_degrees < 337.5:
                direction_text = "SE →"
            else:  # 337.5-360 or 0-22.5
                direction_text = "E →"
            
            # Display direction text
            imgui.text(f"Target")
            imgui.text(direction_text)
            
            # Display distance
            if self.gameState["transporter"] and self.gameState["destination"]:
                player_pos = self.gameState["transporter"].properties["position"]
                dest_pos = self.gameState["destination"].properties["position"]
                distance = np.linalg.norm(dest_pos - player_pos)
                imgui.text(f"Dist: {distance:.0f}")
            
            imgui.end()
            imgui.render()
            self.gui.render(imgui.get_draw_data())

    def UpdateScene(self, inputs, time):
        if self.screen == 0:  # Start screen
            if inputs["1"]:
                self.screen = 1
                self.InitScene()
            if inputs["2"]:
                print("Exiting game...")
                import sys
                sys.exit(0)
        

        if self.screen == 1:  # Game screen
            # Update space stations orbits
            if "spacestations" in self.gameState:
                for station in self.gameState["spacestations"]:
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

            # Handle transporter controls with deltaTime
            if "transporter" in self.gameState and self.gameState["transporter"]:
                transporter = self.gameState["transporter"]
                
                # Base speeds - units per second instead of per frame
                base_rotation_speed = 1.0  # radians per second
                base_movement_speed = 20.0  # units per second
                
                # Apply deltaTime to get frame-independent speeds
                rotation_speed = base_rotation_speed * time
                movement_speed = base_movement_speed * time
                
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
                
                # Handle movement (when SPACE is pressed)
                if inputs["SPACE"]:
                    # Calculate forward direction based on current rotation
                    # Note: We use only pitch and yaw for forward direction, ignoring roll
                    pitch = transporter.properties["rotation"][1]
                    yaw = transporter.properties["rotation"][2]
                    
                    # Calculate forward vector (excluding roll)
                    forward = np.array([
                        -np.sin(yaw) * np.cos(pitch),
                        np.cos(yaw) * np.cos(pitch),
                        np.sin(pitch)
                    ], dtype=np.float32)
                    
                    # Move in the forward direction
                    transporter.properties["position"] += forward * movement_speed
                
                # Update camera to follow transporter
                if self.camera:
                    # Get transporter's position and rotation
                    trans_pos = transporter.properties["position"]
                    pitch = transporter.properties["rotation"][1]
                    yaw = transporter.properties["rotation"][2]
                    
                    # Calculate camera offset (behind and above the transporter)
                    camera_distance = 30.0  # Distance from transporter
                    camera_height = 5.0    # Height above transporter
                    
                    # Calculate camera position based on transporter's rotation (pitch and yaw only)
                    camera_offset = np.array([
                        np.sin(yaw) * np.cos(pitch),  # X offset
                        -np.cos(yaw) * np.cos(pitch), # Y offset
                        -np.sin(pitch)                # Z offset
                    ], dtype=np.float32)
                    
                    # Position camera behind the transporter
                    self.camera.position = trans_pos - camera_offset * camera_distance
                    self.camera.position[2] += camera_height  # Add height
                    
                    # Look at the transporter
                    self.camera.lookAt = trans_pos
                    
                    # Update the camera
                    self.camera.Update(self.shaders['standard'])

            # Update direction angle for UI arrow
            if self.gameState["destination"] and self.gameState["transporter"]:
                # Get positions
                player_pos = self.gameState["transporter"].properties["position"]
                dest_pos = self.gameState["destination"].properties["position"]
                
                # Calculate direction vector from player to destination (in XY plane for compass)
                direction = dest_pos - player_pos
                direction[2] = 0  # Ignore Z component for 2D direction
                
                # Calculate angle in XY plane
                self.gameState["direction_angle"] = np.arctan2(direction[1], direction[0])
                
                # Check if player has reached destination
                distance_to_destination = np.linalg.norm(direction)
                if distance_to_destination < 10 and not self.gameState["game_won"]:  # Within 10 units
                    self.gameState["game_won"] = True
                    print("\n*** CONGRATULATIONS! You've reached the destination! ***\n")

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
            if "spacestations" in self.gameState:
                for station in self.gameState["spacestations"]:
                    station.Draw()
            
            # Draw transporter
            if "transporter" in self.gameState:
                self.gameState["transporter"].Draw()
            
            if "crosshair" in self.gameState and self.gameState["transporter"].properties["view"] == 2:
                self.gameState["crosshair"].Draw()

            # Display win message if game is won
            if self.gameState["game_won"]:
                # Position text in center of screen
                x_pos = self.width / 2 - 100
                y_pos = self.height / 2
                
                imgui.new_frame()
                imgui.set_next_window_position(x_pos, y_pos)
                imgui.set_next_window_size(200, 100)
                imgui.begin("Win Message", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
                imgui.text("MISSION ACCOMPLISHED!")
                imgui.text("You've reached the destination!")
                imgui.end()
                imgui.render()
                self.gui.render(imgui.get_draw_data())

