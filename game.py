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
            "game_over": False,   # Flag to track if player has been defeated
            "direction_angle": 0,  # Angle for the direction indicator
            "first_person_mode": False,  # New flag for first-person mode
            "fp_pitch": 0,               # First-person view pitch
            "fp_yaw": 0                  # First-person view yaw
        }
        
        # Store reference to window for mouse capture
        # Will be set by the App class
        self.window = None

    def InitScene(self):
        if self.screen == 1:
            #print("\nInitializing Scene:")
            
            # Initialize shaders
            self.shaders = {
                'standard': Shader(standard_shader["vertex_shader"], standard_shader["fragment_shader"]),
                'ui': Shader(ui_shader["vertex_shader"], ui_shader["fragment_shader"])
            }
            #print("Shaders initialized")
            
            # Initialize camera with proper lookAt vector
            self.camera = Camera(self.height, self.width)
            self.camera.position = np.array([-20, 0, 10], dtype=np.float32)
            self.camera.lookAt = np.array([0, 0, 0], dtype=np.float32)  # Look at origin
            #print(f"Camera initialized at position {self.camera.position}, looking at {self.camera.lookAt}")
            
            # Define world boundaries
            self.worldMin = np.array([-5000, -5000, -5000], dtype=np.float32)
            self.worldMax = np.array([5000, 5000, 5000], dtype=np.float32)
            
            # Set up light position
            self.lightPos = np.array([1000, 1000, 1000], dtype=np.float32)
            #print(f"Light position set to {self.lightPos}")
            
            # Initialize transporter
            #print("\nCreating objects:")
            transporter_vertices, transporter_indices = create_transporter()
            #print(f"Transporter mesh created with {len(transporter_vertices)/6} vertices")
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
            #print("Transporter initialized")

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
            
            #print(f"Created {self.n_planets} planets with space stations")

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

            # Initialize pirate ships
            pirate_vertices, pirate_indices = create_pirate()
            self.n_pirates = 5  # Number of pirate ships
            self.gameState["pirates"] = []
            
            for i in range(self.n_pirates):
                # Random position within world bounds (but not too close to player)
                min_dist = 150  # Minimum distance from player
                max_dist = 400  # Maximum distance from player
                
                angle = np.random.uniform(0, 2 * np.pi)
                distance = np.random.uniform(min_dist, max_dist)
                
                # Calculate position based on angle and distance
                pirate_pos = np.array([
                    distance * np.cos(angle),
                    distance * np.sin(angle),
                    np.random.uniform(-20, 20)  # Random height
                ], dtype=np.float32)
                
                # Create pirate ship
                pirate = Object("pirate", self.shaders['standard'], {
                    'vertices': pirate_vertices,
                    'indices': pirate_indices,
                    'position': pirate_pos,
                    'rotation': np.array([0, 0, 0], dtype=np.float32),
                    'scale': np.array([0.4, 0.4, 0.4], dtype=np.float32),
                    'colour': np.array([0.9, 0.3, 0.3, 1.0], dtype=np.float32),  # Red color
                    'velocity': np.array([0, 0, 0], dtype=np.float32),
                    'speed': 15.0  # Speed at which pirates pursue the player
                })
                
                self.gameState["pirates"].append(pirate)
            
            print(f"Created {self.n_pirates} pirate ships")
            
            # Add player health
            self.gameState["player_health"] = 100

            # Select a random space station as destination
            if self.gameState["spacestations"]:
                self.gameState["destination"] = np.random.choice(self.gameState["spacestations"])
                # Make the destination station a different color (green)
                self.gameState["destination"].properties["colour"] = np.array([0.0, 1.0, 0.0, 1.0], dtype=np.float32)

            #print("\nScene initialization complete")

    def ProcessFrame(self, inputs, time):
        # Add debug code to print input keys when in first-person mode
        if "screen" in self.__dict__ and self.screen == 1 and "gameState" in self.__dict__ and "first_person_mode" in self.gameState and self.gameState["first_person_mode"]:
            print(f"Available inputs: {list(inputs.keys())}")  # Print available input keys
            if "mouse_dx" in inputs:
                print(f"Mouse DX: {inputs['mouse_dx']}")
            if "mouse_dy" in inputs:
                print(f"Mouse DY: {inputs['mouse_dy']}")
        
        self.UpdateScene(inputs, time)
        self.DrawScene(inputs)
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

        # Direction indicator in bottom right (with rotating arrow)
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
            
            # Get the drawing list for custom rendering
            draw_list = imgui.get_window_draw_list()
            
            # Calculate center of window
            center_x = x_pos + indicator_size / 2
            center_y = y_pos + indicator_size / 2
            
            # Arrow properties
            arrow_color = imgui.get_color_u32_rgba(1, 0, 0, 1)  # Red
            arrow_size = indicator_size * 0.4  # Size of arrow
            
            # Get direction angle
            angle = self.gameState["direction_angle"]
            
            # Calculate arrow points based on angle
            # Arrow tip
            tip_x = center_x + np.cos(angle) * arrow_size
            tip_y = center_y + np.sin(angle) * arrow_size
            
            # Arrow base points (making a triangle)
            base_angle1 = angle + 2.5  # Angle for first base point
            base_angle2 = angle - 2.5  # Angle for second base point
            base_dist = arrow_size * 0.5
            
            base1_x = center_x + np.cos(base_angle1) * base_dist
            base1_y = center_y + np.sin(base_angle1) * base_dist
            base2_x = center_x + np.cos(base_angle2) * base_dist
            base2_y = center_y + np.sin(base_angle2) * base_dist
            
            # Draw arrow as a filled triangle
            draw_list.add_triangle_filled(
                tip_x, tip_y,
                base1_x, base1_y,
                base2_x, base2_y,
                arrow_color
            )
            
            # Draw a circle in the background
            draw_list.add_circle(
                center_x, center_y,
                indicator_size / 2 - 5,
                imgui.get_color_u32_rgba(0.1, 0.1, 0.1, 0.7),  # Dark background
                12  # Number of segments
            )
            
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
                #print("Exiting game...")
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

            # Update lasers
            if "lasers" in self.gameState:
                current_time = time['currentTime']
                lasers_to_remove = []
                
                for i, laser in enumerate(self.gameState["lasers"]):
                    # Update laser position based on velocity
                    laser.properties["position"] += laser.properties["velocity"] * time['deltaTime']
                    
                    # Check if laser's lifetime has expired
                    creation_time = laser.properties["creation_time"]
                    lifetime = laser.properties["lifetime"]
                    
                    if current_time - creation_time > lifetime:
                        lasers_to_remove.append(i)
                
                # Remove expired lasers (in reverse order to avoid index issues)
                for index in sorted(lasers_to_remove, reverse=True):
                    del self.gameState["lasers"][index]

            # Update pirate ships
            if "pirates" in self.gameState and "transporter" in self.gameState:
                transporter_pos = self.gameState["transporter"].properties["position"]
                pirates_to_remove = []
                
                # Check for laser hits on pirates
                if "lasers" in self.gameState:
                    for i, pirate in enumerate(self.gameState["pirates"]):
                        pirate_pos = pirate.properties["position"]
                        
                        for j, laser in enumerate(self.gameState["lasers"]):
                            laser_pos = laser.properties["position"]
                            
                            # Calculate distance between laser and pirate
                            distance = np.linalg.norm(pirate_pos - laser_pos)
                            
                            # Check if laser hit pirate (within 2 units)
                            if distance < 2.0 and j not in lasers_to_remove:
                                print(f"Pirate {i} hit by laser!")
                                pirates_to_remove.append(i)
                                lasers_to_remove.append(j)
                                break  # One laser can only hit one pirate
                
                # Update pirate movement and check collisions with player
                for i, pirate in enumerate(self.gameState["pirates"]):
                    if i in pirates_to_remove:
                        continue  # Skip pirates that are already marked for removal
                    
                    pirate_pos = pirate.properties["position"]
                    
                    # Calculate direction to player
                    direction_to_player = transporter_pos - pirate_pos
                    distance_to_player = np.linalg.norm(direction_to_player)
                    
                    # Check for collision with player
                    if distance_to_player < 3.0 and self.gameState["player_health"] > 0:
                        print("Pirate collided with player!")
                        pirates_to_remove.append(i)
                        
                        # Reduce player health
                        self.gameState["player_health"] -= 25
                        print(f"Player health reduced to {self.gameState['player_health']}")
                        
                        # Check if player is defeated
                        if self.gameState["player_health"] <= 0:
                            print("Player defeated!")
                            self.gameState["game_over"] = True
                            self.gameState["player_health"] = 0  # Ensure health doesn't go below 0
                    else:
                        # Normalize direction and move pirate towards player
                        if distance_to_player > 0:
                            direction_normalized = direction_to_player / distance_to_player
                            
                            # Update pirate position
                            pirate_speed = pirate.properties["speed"] * time['deltaTime']
                            pirate.properties["position"] += direction_normalized * pirate_speed
                            
                            # Calculate rotation to face player
                            yaw = np.arctan2(direction_normalized[1], direction_normalized[0])
                            pirate.properties["rotation"][2] = yaw
                
                # Remove destroyed pirates
                for index in sorted(pirates_to_remove, reverse=True):
                    del self.gameState["pirates"][index]
                
                # Remove lasers that hit pirates (in reverse order to avoid index issues)
                for index in sorted(lasers_to_remove, reverse=True):
                    if index < len(self.gameState["lasers"]):  # Check if index is valid
                        del self.gameState["lasers"][index]

            if "transporter" in self.gameState:
                transporter = self.gameState["transporter"]
                
                # Toggle first-person mode with L_SHIFT
                if "L_SHIFT" in inputs and inputs["L_SHIFT"]:
                    self.gameState["first_person_mode"] = not self.gameState["first_person_mode"]
                    print(f"First-person mode: {self.gameState['first_person_mode']}")
                    
                    if self.gameState["first_person_mode"]:
                        # Initialize first-person view angles based on current rotation
                        self.gameState["fp_yaw"] = transporter.properties["rotation"][2]
                        self.gameState["fp_pitch"] = transporter.properties["rotation"][1]
                        
                        # Enable mouse capture for first-person mode
                        if self.window is not None:
                            self.window.EnableMouseCapture()
                        else:
                            print("Warning: Window reference not set, mouse capture not enabled")
                    else:
                        # Disable mouse capture when exiting first-person mode
                        if self.window is not None:
                            self.window.DisableMouseCapture()
                        else:
                            print("Warning: Window reference not set, mouse capture not disabled")
                
                # Handle ship controls only when not in first-person mode
                if not self.gameState["first_person_mode"]:
                    # Extract deltaTime
                    delta_time = time['deltaTime']
                    
                    # Rotation speeds (in radians per frame)
                    rotation_speed = 0.008 * delta_time * 60  # Scale by deltaTime, assuming 60fps baseline
                    
                    # Calculate current nose direction before rotation
                    forward = np.array([1, 0, 0], dtype=np.float32)  # Base forward vector along X-axis
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
                    
                    # Handle rotations
                    if inputs["W"]:  # Pitch up
                        transporter.properties["rotation"][1] -= rotation_speed  # Use Y-axis for pitch, inverted
                    if inputs["S"]:  # Pitch down
                        transporter.properties["rotation"][1] += rotation_speed  # Use Y-axis for pitch, inverted
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
                    
                    # Handle forward movement (only on SPACE)
                    if inputs["SPACE"]:
                        # Calculate forward direction based on current rotation
                        forward = np.array([1, 0, 0], dtype=np.float32)  # Base forward vector (pointing along X)
                        
                        # Create rotation matrices
                        # Yaw (Z-axis rotation)
                        yaw = transporter.properties["rotation"][2]
                        yaw_matrix = np.array([
                            [np.cos(yaw), -np.sin(yaw), 0],
                            [np.sin(yaw), np.cos(yaw), 0],
                            [0, 0, 1]
                        ], dtype=np.float32)
                        
                        # Pitch (Y-axis rotation)
                        pitch = transporter.properties["rotation"][1]
                        pitch_matrix = np.array([
                            [np.cos(pitch), 0, np.sin(pitch)],
                            [0, 1, 0],
                            [-np.sin(pitch), 0, np.cos(pitch)]
                        ], dtype=np.float32)
                        
                        # Roll (X-axis rotation)
                        roll = transporter.properties["rotation"][0]
                        roll_matrix = np.array([
                            [1, 0, 0],
                            [0, np.cos(roll), -np.sin(roll)],
                            [0, np.sin(roll), np.cos(roll)]
                        ], dtype=np.float32)
                        
                        # Apply rotations to get forward direction
                        # Apply in the same order as for calculating nose direction
                        forward = roll_matrix @ pitch_matrix @ yaw_matrix @ forward
                        
                        # Update velocity (with speed limit)
                        movement_speed = 0.1 * delta_time * 60  # Scale by deltaTime, assuming 60fps baseline
                        max_speed = 0.5
                        
                        new_velocity = transporter.properties["velocity"] + forward * movement_speed
                        speed = np.linalg.norm(new_velocity)
                        if speed > max_speed:
                            new_velocity = (new_velocity / speed) * max_speed
                        
                        transporter.properties["velocity"] = new_velocity
                    
                    # Apply velocity to position
                    transporter.properties["position"] += transporter.properties["velocity"]
                    
                    # Add drag to slow down when not accelerating
                    drag = 0.99
                    transporter.properties["velocity"] *= drag

                # First-person camera control with mouse when in first-person mode
                if self.gameState["first_person_mode"]:
                    # Get mouse delta from the inputs - this is the correct key based on the window_manager.py file
                    if "mouseDelta" in inputs:
                        mouse_dx = inputs["mouseDelta"][0]  # X-axis mouse movement
                        mouse_dy = inputs["mouseDelta"][1]  # Y-axis mouse movement
                        
                        # Mouse sensitivity factor - adjusted for potentially larger values
                        mouse_sensitivity = 0.002
                        
                        # Update yaw and pitch based on mouse movement
                        self.gameState["fp_yaw"] -= mouse_dx * mouse_sensitivity
                        self.gameState["fp_pitch"] -= mouse_dy * mouse_sensitivity
                        
                        # Clamp pitch to prevent over-rotation
                        self.gameState["fp_pitch"] = max(min(self.gameState["fp_pitch"], np.pi/2 - 0.1), -np.pi/2 + 0.1)
                        
                        if mouse_dx != 0 or mouse_dy != 0:
                            print(f"Mouse movement: DX={mouse_dx}, DY={mouse_dy}")
                            print(f"Updated camera: Yaw={self.gameState['fp_yaw']}, Pitch={self.gameState['fp_pitch']}")
                    
                    # Handle shooting with left mouse button in first-person mode
                    if "L_CLICK" in inputs and inputs["L_CLICK"]:
                        # Calculate direction based on first-person yaw and pitch
                        direction = np.array([
                            np.cos(self.gameState["fp_yaw"]) * np.cos(self.gameState["fp_pitch"]),
                            np.sin(self.gameState["fp_yaw"]) * np.cos(self.gameState["fp_pitch"]),
                            np.sin(self.gameState["fp_pitch"])
                        ], dtype=np.float32)
                        
                        # Normalize direction
                        direction = direction / np.linalg.norm(direction)
                        
                        # Create a new laser
                        laser_vertices, laser_indices = create_laser()
                        
                        # Get the ship's position as the starting point for the laser
                        ship_position = np.copy(transporter.properties["position"])
                        
                        # Position the laser slightly in front of the camera to avoid self-collision
                        laser_position = ship_position + direction * 2.0
                        
                        # Calculate rotation angles based on the laser direction
                        # The laser model is oriented along the Z-axis by default, so we need to rotate it
                        # to align with our direction vector
                        
                        # Calculate pitch (rotation around Y-axis)
                        pitch = np.arctan2(direction[2], np.sqrt(direction[0]**2 + direction[1]**2))
                        
                        # Calculate yaw (rotation around Z-axis)
                        yaw = np.arctan2(direction[1], direction[0])
                        
                        # Create the laser object with rotations set to align with the direction
                        new_laser = Object("laser", self.shaders['standard'], {
                            'vertices': laser_vertices,
                            'indices': laser_indices,
                            'position': laser_position,
                            'rotation': np.array([0, pitch, yaw], dtype=np.float32),
                            'scale': np.array([0.1, 0.1, 2.0], dtype=np.float32),  # Thinner and longer
                            'colour': np.array([1.0, 0.2, 0.2, 1.0], dtype=np.float32),  # Red
                            'velocity': direction * 20.0,  # Faster speed
                            'creation_time': time['currentTime'],
                            'lifetime': 3.0  # Seconds before the laser disappears
                        })
                        
                        # Add the laser to the gameState
                        self.gameState["lasers"].append(new_laser)
                        print(f"Laser fired: Position={laser_position}, Direction={direction}")
                
                # Update camera based on mode
                if self.camera:
                    if self.gameState["first_person_mode"]:
                        # First-person camera implementation
                        # Position camera above the transporter (on top of the ship)
                        ship_position = np.copy(transporter.properties["position"])
                        # Add height offset to place camera on top of the ship
                        ship_position[2] += 2.0  # Adjust this value based on ship size
                        self.camera.position = ship_position
                        
                        # Calculate lookAt direction based on first-person yaw and pitch
                        direction = np.array([
                            np.cos(self.gameState["fp_yaw"]) * np.cos(self.gameState["fp_pitch"]),
                            np.sin(self.gameState["fp_yaw"]) * np.cos(self.gameState["fp_pitch"]),
                            np.sin(self.gameState["fp_pitch"])
                        ], dtype=np.float32)
                        
                        # Set lookAt point
                        self.camera.lookAt = self.camera.position + direction * 10
                    else:
                        # Third-person camera implementation
                        camera_distance = 10
                        camera_height = 0
                        
                        # First position the camera behind and above the ship
                        camera_pos = np.copy(transporter.properties["position"])
                        
                        # Apply transformations in the correct order
                        # 1. Move back by camera_distance (along negative X since ship faces positive X)
                        camera_pos[0] -= camera_distance
                        
                        # 2. Move up by camera_height
                        camera_pos[2] += camera_height
                        
                        # 3. Rotate around the ship based on ship's rotation
                        # Get ship's rotation angles
                        yaw = transporter.properties["rotation"][2]  # Z-axis rotation
                        pitch = transporter.properties["rotation"][1]  # Y-axis rotation
                        
                        # Calculate rotation around the ship
                        # Create a vector from ship to camera
                        camera_vector = camera_pos - transporter.properties["position"]
                        
                        # Apply yaw rotation (around Z-axis)
                        yaw_rad = yaw
                        cos_yaw = np.cos(yaw_rad)
                        sin_yaw = np.sin(yaw_rad)
                        
                        new_x = camera_vector[0] * cos_yaw - camera_vector[1] * sin_yaw
                        new_y = camera_vector[0] * sin_yaw + camera_vector[1] * cos_yaw
                        
                        camera_vector[0] = new_x
                        camera_vector[1] = new_y
                        
                        # Apply pitch rotation (around Y-axis)
                        pitch_rad = pitch
                        cos_pitch = np.cos(pitch_rad)
                        sin_pitch = np.sin(pitch_rad)
                        
                        new_x = camera_vector[0] * cos_pitch + camera_vector[2] * sin_pitch
                        new_z = -camera_vector[0] * sin_pitch + camera_vector[2] * cos_pitch
                        
                        camera_vector[0] = new_x
                        camera_vector[2] = new_z
                        
                        # Set final camera position
                        self.camera.position = transporter.properties["position"] + camera_vector
                        self.camera.lookAt = transporter.properties["position"]
                    
                    # Update the camera in both modes
                    self.camera.Update(self.shaders['standard'])

            # Update direction angle for UI arrow
            if self.gameState["destination"] and self.gameState["transporter"]:
                # Get positions
                player_pos = self.gameState["transporter"].properties["position"]
                dest_pos = self.gameState["destination"].properties["position"]
                
                # Calculate direction vector from player to destination (in XY plane for compass)
                direction = dest_pos - player_pos
                direction[2] = 0  # Ignore Z component for 2D direction
                
                # Calculate angle in XY plane - FIXED: flip the angle calculation
                # The issue is that the screen coordinates are flipped compared to world coordinates
                self.gameState["direction_angle"] = np.arctan2(-direction[1], -direction[0])
                
                # Check if player has reached destination
                distance_to_destination = np.linalg.norm(direction)
                if distance_to_destination < 5 and not self.gameState["game_won"]:  # Within 10 units
                    self.gameState["game_won"] = True
                    #print("\n*** CONGRATULATIONS! You've reached the destination! ***\n")

    def DrawScene(self, inputs):
        if self.screen == 1:
            # Update camera for standard shader
            self.camera.Update(self.shaders['standard'])
            
            # Set lighting uniforms for standard shader
            self.shaders['standard'].Use()
            lightPosLoc = glGetUniformLocation(self.shaders['standard'].ID, "lightPos".encode('utf-8'))
            viewPosLoc = glGetUniformLocation(self.shaders['standard'].ID, "viewPos".encode('utf-8'))
            
            if lightPosLoc == -1 or viewPosLoc == -1:
                #print("Warning: Could not find light/view position uniforms in shader")
                pass
            
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
            
            # Draw pirates
            if "pirates" in self.gameState:
                for pirate in self.gameState["pirates"]:
                    pirate.Draw()
            
            # Draw lasers
            if "lasers" in self.gameState:
                for laser in self.gameState["lasers"]:
                    laser.Draw()
            
            if "crosshair" in self.gameState and self.gameState["transporter"].properties["view"] == 2:
                self.gameState["crosshair"].Draw()

            # Display win message if game is won
            if self.gameState["game_won"]:
                # Position text in center of screen
                x_pos = self.width / 2 - 150
                y_pos = self.height / 2 - 75
                
                imgui.new_frame()
                imgui.set_next_window_position(x_pos, y_pos)
                imgui.set_next_window_size(300, 150)
                imgui.begin("Win Message", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
                
                # Centered title
                text_width = imgui.calc_text_size("MISSION ACCOMPLISHED!")[0]
                imgui.set_cursor_pos_x((300 - text_width) / 2)
                imgui.text("MISSION ACCOMPLISHED!")
                
                # Centered subtitle
                text_width = imgui.calc_text_size("You've reached the destination!")[0]
                imgui.set_cursor_pos_x((300 - text_width) / 2)
                imgui.text("You've reached the destination!")
                
                # Add some space
                imgui.dummy(0, 20)
                
                # Centered button
                button_width = 200
                imgui.set_cursor_pos_x((300 - button_width) / 2)
                imgui.button("Press 4: Return to Main Menu", button_width, 30)
                    # Return to main menu when clickeda
                if inputs['4']:
                        self.screen = 0
                        print('entered')
                        self.gameState["game_won"] = False
                        
                
                imgui.end()
                imgui.render()
                self.gui.render(imgui.get_draw_data())

            # Display game over message if player is defeated
            if self.gameState["game_over"]:
                # Position text in center of screen
                x_pos = self.width / 2 - 150
                y_pos = self.height / 2 - 75
                
                imgui.new_frame()
                imgui.set_next_window_position(x_pos, y_pos)
                imgui.set_next_window_size(300, 150)
                imgui.begin("Game Over", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
                
                # Centered title
                text_width = imgui.calc_text_size("MISSION FAILED!")[0]
                imgui.set_cursor_pos_x((300 - text_width) / 2)
                imgui.text("MISSION FAILED!")
                
                # Centered subtitle
                text_width = imgui.calc_text_size("Your ship has been destroyed!")[0]
                imgui.set_cursor_pos_x((300 - text_width) / 2)
                imgui.text("Your ship has been destroyed!")
                
                # Add some space
                imgui.dummy(0, 20)
                
                # Centered button
                button_width = 200
                imgui.set_cursor_pos_x((300 - button_width) / 2)
                imgui.button("Press 4: Return to Main Menu", button_width, 30)
                # Return to main menu when pressed
                if inputs['4']:
                    self.screen = 0
                    self.gameState["game_over"] = False
                    self.gameState["player_health"] = 100  # Reset player health
                    # Reset pirates and other game elements
                    self.gameState["pirates"] = []
                    self.gameState["lasers"] = []
                    
                imgui.end()
                imgui.render()
                self.gui.render(imgui.get_draw_data())

            # Draw player health bar
            if self.gameState["player_health"] >= 0:
                # Position health bar at top left
                health_bar_width = 200
                health_bar_height = 20
                x_pos = 20
                y_pos = 20
                
                # Create window for health bar
                imgui.new_frame()
                imgui.set_next_window_position(x_pos, y_pos)
                imgui.set_next_window_size(health_bar_width + 40, health_bar_height + 40)
                imgui.begin("Health", False, 
                          imgui.WINDOW_NO_TITLE_BAR | 
                          imgui.WINDOW_NO_RESIZE | 
                          imgui.WINDOW_NO_MOVE)
                
                # Draw health label
                imgui.text("Health:")
                imgui.same_line()
                
                # Calculate health percentage
                health_percent = self.gameState["player_health"] / 100.0
                
                # Get drawing context
                draw_list = imgui.get_window_draw_list()
                
                # Draw background bar (gray)
                draw_list.add_rect_filled(
                    x_pos + 70, y_pos + 20,
                    x_pos + 70 + health_bar_width, y_pos + 20 + health_bar_height,
                    imgui.get_color_u32_rgba(0.2, 0.2, 0.2, 1.0)
                )
                
                # Draw health bar (green to red based on health)
                bar_color = imgui.get_color_u32_rgba(
                    1.0 - health_percent,  # Red component increases as health decreases
                    health_percent,        # Green component decreases as health decreases
                    0.0, 1.0
                )
                
                draw_list.add_rect_filled(
                    x_pos + 70, y_pos + 20,
                    x_pos + 70 + health_bar_width * health_percent, y_pos + 20 + health_bar_height,
                    bar_color
                )
                
                # Show health value text
                imgui.text(f"{self.gameState['player_health']}/100")
                
                imgui.end()
                imgui.render()
                self.gui.render(imgui.get_draw_data())

            # Draw crosshair in first-person mode using ImGui
            if self.gameState["first_person_mode"]:
                crosshair_size = 20  # Size of the crosshair
                line_thickness = 2.0  # Thickness of the crosshair lines
                
                # Position at center of screen
                center_x = self.width / 2
                center_y = self.height / 2
                
                # Create a new ImGui window for the crosshair
                imgui.new_frame()
                imgui.set_next_window_position(0, 0)
                imgui.set_next_window_size(self.width, self.height)
                imgui.begin("FP Crosshair", False, 
                          imgui.WINDOW_NO_TITLE_BAR | 
                          imgui.WINDOW_NO_RESIZE | 
                          imgui.WINDOW_NO_MOVE |
                          imgui.WINDOW_NO_SCROLLBAR |
                          imgui.WINDOW_NO_BACKGROUND)
                
                # Get the drawing list
                draw_list = imgui.get_window_draw_list()
                
                # Draw horizontal line
                draw_list.add_line(
                    center_x - crosshair_size, center_y,
                    center_x + crosshair_size, center_y,
                    imgui.get_color_u32_rgba(1, 1, 1, 1),  # White color
                    line_thickness
                )
                
                # Draw vertical line
                draw_list.add_line(
                    center_x, center_y - crosshair_size,
                    center_x, center_y + crosshair_size,
                    imgui.get_color_u32_rgba(1, 1, 1, 1),  # White color
                    line_thickness
                )
                
                imgui.end()
                imgui.render()
                self.gui.render(imgui.get_draw_data())

    def SetWindow(self, window):
        """Set the window reference for mouse capture"""
        self.window = window
        print("Window reference set for mouse capture")

