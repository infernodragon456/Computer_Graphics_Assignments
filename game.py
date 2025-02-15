import imgui
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from assets.objects.objects import playerProps, backgroundProps, platformProps, keyProps
import glfw
import copy
import time
import json
import os

class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = -1  # -1: uninitialized, 0: menu, 1: game, 2: victory screen, 3: game over screen
        self.camera = Camera(height, width)
        self.shader = Shader(object_shader['vertex_shader'], object_shader['fragment_shader'])
        self.objects = []
        # Add player stats
        self.player_health = 100
        self.player_lives = 3
        # Add map and time tracking
        self.current_map = 1
        self.start_time = None
        self.elapsed_time = 0
        # Add player movement properties
        self.player_speed = 500.0  # Increased speed to account for scaling
        self.player_position = np.array([-0.8, 0.0, 0.0], dtype=np.float32)  # Starting position
        self.platforms = []  # List to store platform objects
        self.keys_collected = 0
        self.keys = []  # List to store key objects
        self.player_velocity_z = 0  # Changed from y to z
        self.jump_speed = 400.0
        self.gravity = 800.0
        self.is_grounded = False
        self.paused = False  # Add pause state
        self.save_file = "savegame.txt"

    def InitScreen(self):
        if self.screen == 1:
            self.start_time = glfw.get_time()
            self.keys_collected = 0
            
            # Initialize objects list with background and player in correct order
            self.objects = [
                Object(self.shader, backgroundProps),  # Index 0: background
                Object(self.shader, playerProps)       # Index 1: player
            ]
            
            # Clear existing platforms and keys
            self.platforms = []
            self.keys = []
            
            # Create platforms after player
            vertical_positions = [-300, -100, 100, 300]
            for x_pos in vertical_positions:
                platform_props = copy.deepcopy(platformProps)
                platform_props['position'] = np.array([x_pos, 0, 0], dtype=np.float32)
                platform_props['movement_type'] = 'vertical'
                platform_props['speed'] = 150.0
                platform = Object(self.shader, platform_props)
                self.platforms.append(platform)
                self.objects.append(platform)  # Added after player

            horizontal_positions = [-200, 0, 200]
            y_positions = [-150, 0, 150]
            for x_pos, y_pos in zip(horizontal_positions, y_positions):
                platform_props = copy.deepcopy(platformProps)
                platform_props['position'] = np.array([x_pos, y_pos, 0], dtype=np.float32)
                platform_props['movement_type'] = 'horizontal'
                platform_props['speed'] = 120.0
                platform_props['bounds'] = [-350, 350]
                platform = Object(self.shader, platform_props)
                self.platforms.append(platform)
                self.objects.append(platform)
            
            # Create keys last
            key_platform_indices = [0, 3, 5]
            for i in key_platform_indices:
                platform_pos = self.platforms[i].properties['position']
                key_props = copy.deepcopy(keyProps)
                key_props['position'] = np.array([
                    platform_pos[0], 
                    platform_pos[1] + 15,
                    2.0
                ], dtype=np.float32)
                key_props['platform_index'] = i
                key = Object(self.shader, key_props)
                self.keys.append(key)
                self.objects.append(key)

            # Set initial player position
            self.player_position = np.array([-450.0, 0.0, 1.0], dtype=np.float32)
            self.objects[1].properties['position'] = self.player_position

    def ProcessFrame(self, inputs, time):
        if self.screen == -1:
            self.screen = 0  # Start at menu screen
        
        # Handle menu inputs
        if self.screen == 0:
            if "1" in inputs:  # New Game
                self.screen = 1
                self.InitScreen()
        
        self.DrawText()
        if self.screen == 1:  # Only update and draw scene in game mode
            self.UpdateScene(inputs, time)
            self.DrawScene()

    def DrawText(self):
        if self.screen == 0:  # Menu Screen
            # Center the window
            window_width = 1000
            window_height = 1000
            imgui.set_next_window_size(window_width, window_height)
            imgui.set_next_window_position(
                (self.width - window_width) / 2,
                (self.height - window_height) / 2
            )
            
            # Style the window
            style = imgui.get_style()
            style.window_rounding = 8
            style.frame_rounding = 20  # Rounded buttons
            style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.1, 0.05, 0.15, 1.0)  # Dark purple background
            style.colors[imgui.COLOR_TEXT] = (1.0, 0.33, 0.33, 1.0)  # Coral red text
            style.colors[imgui.COLOR_BUTTON] = (0.5, 0.33, 0.33, 0.8)  # Coral red buttons
            style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.5, 0.4, 0.4, 1.0)  # Lighter red on hover
            style.colors[imgui.COLOR_BUTTON_ACTIVE] = (0.6, 0.3, 0.3, 1.0)  # Darker red when clicked
            style.colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0.1, 0.05, 0.15, 1.0)
            style.colors[imgui.COLOR_TITLE_BACKGROUND] = (0.1, 0.05, 0.15, 1.0)
            
            # Remove window border
            imgui.begin(
                "Portal Shenanigans", 
                flags=imgui.WINDOW_NO_RESIZE | 
                      imgui.WINDOW_NO_MOVE | 
                      imgui.WINDOW_NO_COLLAPSE |
                      imgui.WINDOW_NO_TITLE_BAR
            )
            
            # Center align text
            window_width = imgui.get_window_width()
            
            # Move content down to center vertically
            imgui.dummy(0, 300)  # Add padding at the top
            
            # Title
            title_text = "Portal Shenanigans"
            imgui.set_window_font_scale(3)  # Make title bigger
            title_width = imgui.calc_text_size(title_text).x
            imgui.set_cursor_pos_x((window_width - title_width) * 0.5)
            imgui.text(title_text)
            
            imgui.dummy(0, 20)
            
            # Buttons
            button_width = 200
            button_height = 40
            imgui.set_window_font_scale(1.0)
            
            # Start Game button
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("New Game", width=button_width, height=button_height):
                self.screen = 1
                self.player_lives = 3
                self.player_health = 100
                self.keys_collected = 0
                self.elapsed_time = 0
                self.start_time = glfw.get_time()
                self.InitScreen()
            
            imgui.dummy(0, 10)
            
            # Load Game button
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("Load Game", width=button_width, height=button_height):
                if self.load_game():
                    self.screen = 1  # Switch to game screen after successful load
            
            imgui.dummy(0, 10)
            
            # Quit button
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("Quit", width=button_width, height=button_height):
                exit(0)
            
            imgui.end()

        elif self.screen == 2:  # Victory Screen
            # Center the window
            window_width = 1000
            window_height = 1000
            imgui.set_next_window_size(window_width, window_height)
            imgui.set_next_window_position(
                (self.width - window_width) / 2,
                (self.height - window_height) / 2
            )
            
            # Style the window
            style = imgui.get_style()
            style.window_rounding = 8
            style.frame_rounding = 20  # Rounded buttons
            style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.1, 0.05, 0.15, 1.0)  # Dark purple background
            style.colors[imgui.COLOR_TEXT] = (0.33, 1.0, 0.33, 1.0)  # Green text for victory
            style.colors[imgui.COLOR_BUTTON] = (0.33, 0.5, 0.33, 0.8)  # Green buttons
            style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.4, 0.6, 0.4, 1.0)
            style.colors[imgui.COLOR_BUTTON_ACTIVE] = (0.3, 0.5, 0.3, 1.0)
            style.colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0.1, 0.05, 0.15, 1.0)
            style.colors[imgui.COLOR_TITLE_BACKGROUND] = (0.1, 0.05, 0.15, 1.0)
            
            # Remove window border
            imgui.begin(
                "Victory Screen", 
                flags=imgui.WINDOW_NO_RESIZE | 
                      imgui.WINDOW_NO_MOVE | 
                      imgui.WINDOW_NO_COLLAPSE |
                      imgui.WINDOW_NO_TITLE_BAR
            )
            
            # Center align text
            window_width = imgui.get_window_width()
            
            # Move content down to center vertically
            imgui.dummy(0, 300)  # Add padding at the top
            
            # Victory message
            title_text = "You Won!"
            imgui.set_window_font_scale(3.0)  # Make title bigger
            title_width = imgui.calc_text_size(title_text).x
            imgui.set_cursor_pos_x((window_width - title_width) * 0.5)
            imgui.text(title_text)
            
            # Completion time
            time_text = f"Time: {int(self.elapsed_time // 60):02d}:{int(self.elapsed_time % 60):02d}"
            imgui.set_window_font_scale(1.5)
            time_width = imgui.calc_text_size(time_text).x
            imgui.set_cursor_pos_x((window_width - time_width) * 0.5)
            imgui.text(time_text)
            
            imgui.dummy(0, 20)  # Add some vertical spacing
            
            # Buttons
            button_width = 200
            button_height = 40
            imgui.set_window_font_scale(1.0)
            
            # Center each button
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("Play Again", width=button_width, height=button_height):
                self.screen = 1
                self.InitScreen()
            
            imgui.dummy(0, 10)  # Space between buttons
            
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("Main Menu", width=button_width, height=button_height):
                self.screen = 0
            
            imgui.dummy(0, 10)  # Space between buttons
            
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("Quit", width=button_width, height=button_height):
                exit(0)
            
            imgui.end()

        elif self.screen == 3:  # Game Over Screen
            # Center the window
            window_width = 1000
            window_height = 1000
            imgui.set_next_window_size(window_width, window_height)
            imgui.set_next_window_position(
                (self.width - window_width) / 2,
                (self.height - window_height) / 2
            )
            
            # Style the window
            style = imgui.get_style()
            style.window_rounding = 8
            style.frame_rounding = 20
            style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.15, 0.05, 0.05, 1.0)  # Dark red background
            style.colors[imgui.COLOR_TEXT] = (1.0, 0.33, 0.33, 1.0)  # Red text
            style.colors[imgui.COLOR_BUTTON] = (0.5, 0.2, 0.2, 0.8)  # Dark red buttons
            style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.6, 0.3, 0.3, 1.0)
            style.colors[imgui.COLOR_BUTTON_ACTIVE] = (0.7, 0.2, 0.2, 1.0)
            style.colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0.15, 0.05, 0.05, 1.0)
            style.colors[imgui.COLOR_TITLE_BACKGROUND] = (0.15, 0.05, 0.05, 1.0)
            
            # Remove window border
            imgui.begin(
                "Game Over", 
                flags=imgui.WINDOW_NO_RESIZE | 
                      imgui.WINDOW_NO_MOVE | 
                      imgui.WINDOW_NO_COLLAPSE |
                      imgui.WINDOW_NO_TITLE_BAR
            )
            
            # Center align text
            window_width = imgui.get_window_width()
            
            # Move content down to center vertically
            imgui.dummy(0, 300)
            
            # Game Over text
            title_text = "Game Over"
            imgui.set_window_font_scale(3.0)
            title_width = imgui.calc_text_size(title_text).x
            imgui.set_cursor_pos_x((window_width - title_width) * 0.5)
            imgui.text(title_text)
            
            # Time survived
            time_text = f"Time Survived: {int(self.elapsed_time // 60):02d}:{int(self.elapsed_time % 60):02d}"
            imgui.set_window_font_scale(1.5)
            time_width = imgui.calc_text_size(time_text).x
            imgui.set_cursor_pos_x((window_width - time_width) * 0.5)
            imgui.text(time_text)
            
            imgui.dummy(0, 20)
            
            # Buttons
            button_width = 200
            button_height = 40
            imgui.set_window_font_scale(1.0)
            
            # Try Again button
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("Try Again", width=button_width, height=button_height):
                self.screen = 1
                # Reset all game parameters
                self.player_lives = 3
                self.player_health = 100
                self.keys_collected = 0
                self.elapsed_time = 0
                self.start_time = glfw.get_time()
                self.InitScreen()
            
            imgui.dummy(0, 10)
            
            # Main Menu button
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("Main Menu", width=button_width, height=button_height):
                self.screen = 0
                # Reset all game parameters
                self.player_lives = 3
                self.player_health = 100
                self.keys_collected = 0
                self.elapsed_time = 0
            
            imgui.dummy(0, 10)
            
            # Quit button
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("Quit", width=button_width, height=button_height):
                exit(0)
            
            imgui.end()

        elif self.screen == 1:  # Game Screen - Draw HUD
            # Update elapsed time
            if self.start_time is not None:
                self.elapsed_time = glfw.get_time() - self.start_time
            
            # Create a window for the HUD
            imgui.set_next_window_position(10, 10)
            imgui.set_next_window_size(250, 120)  # Made taller for additional text
            
            # Style the HUD
            style = imgui.get_style()
            style.window_rounding = 0
            style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.0, 0.0, 0.0, 0.7)
            
            imgui.begin(
                "HUD",
                flags=imgui.WINDOW_NO_RESIZE | 
                      imgui.WINDOW_NO_MOVE | 
                      imgui.WINDOW_NO_COLLAPSE |
                      imgui.WINDOW_NO_TITLE_BAR
            )
            
            draw_list = imgui.get_window_draw_list()
            window_pos = imgui.get_cursor_screen_pos()
            pos_x = window_pos[0]
            pos_y = window_pos[1]
            
            # Draw hearts for lives
            heart_size = 20
            heart_spacing = 5
            heart_color = int(0xFFFF0000)
            
            for i in range(self.player_lives):
                heart_x = pos_x + (i * (heart_size + heart_spacing))
                draw_list.add_rect_filled(
                    heart_x, pos_y,
                    heart_x + heart_size, pos_y + heart_size,
                    heart_color
                )
            
            # Health bar dimensions
            bar_width = 200
            bar_height = 20
            bar_y = pos_y + heart_size + 10
            
            # Calculate health percentage
            health_percentage = self.player_health / 100.0
            filled_width = bar_width * health_percentage
            
            # Colors
            black = int(0xFF000000)
            green = int(0xFF00FF00)
            white = int(0xFFFFFFFF)
            
            # Draw black background
            draw_list.add_rect_filled(
                pos_x, bar_y,
                pos_x + bar_width, bar_y + bar_height,
                black
            )
            
            # Draw green health fill
            if health_percentage > 0:
                draw_list.add_rect_filled(
                    pos_x, bar_y,
                    pos_x + filled_width, bar_y + bar_height,
                    green
                )
            
            # Draw health text
            draw_list.add_text(
                pos_x + (bar_width / 2) - 25, bar_y + 2,
                white,
                f"{int(self.player_health)}/100"
            )
            
            # Draw map number and time
            text_y = bar_y + bar_height + 10
            draw_list.add_text(
                pos_x, text_y,
                white,
                f"Map: {self.current_map}/3"
            )
            
            # Format time as minutes:seconds
            minutes = int(self.elapsed_time) // 60
            seconds = int(self.elapsed_time) % 60
            draw_list.add_text(
                pos_x + bar_width - 70, text_y,
                white,
                f"Time: {minutes:02d}:{seconds:02d}"
            )
            
            imgui.end()

            # Draw pause menu if paused
            if self.paused:
                # Center the pause menu
                window_width = 400
                window_height = 300
                imgui.set_next_window_size(window_width, window_height)
                imgui.set_next_window_position(
                    (self.width - window_width) / 2,
                    (self.height - window_height) / 2
                )
                
                # Style the pause menu
                style = imgui.get_style()
                style.window_rounding = 8
                style.frame_rounding = 20
                style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.1, 0.1, 0.1, 0.95)  # Semi-transparent dark background
                style.colors[imgui.COLOR_TEXT] = (1.0, 1.0, 1.0, 1.0)
                style.colors[imgui.COLOR_BUTTON] = (0.2, 0.2, 0.3, 0.8)
                style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.3, 0.3, 0.4, 1.0)
                style.colors[imgui.COLOR_BUTTON_ACTIVE] = (0.4, 0.4, 0.5, 1.0)
                style.colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0.1, 0.1, 0.1, 1.0)
                style.colors[imgui.COLOR_TITLE_BACKGROUND] = (0.1, 0.1, 0.1, 1.0)
                
                # Create pause menu window
                imgui.begin(
                    "Pause Menu",
                    flags=imgui.WINDOW_NO_RESIZE | 
                          imgui.WINDOW_NO_MOVE | 
                          imgui.WINDOW_NO_COLLAPSE |
                          imgui.WINDOW_NO_TITLE_BAR
                )
                
                # Center align text and buttons
                window_width = imgui.get_window_width()
                
                # Title
                title_text = "PAUSED"
                imgui.set_window_font_scale(2.0)
                title_width = imgui.calc_text_size(title_text).x
                imgui.set_cursor_pos_x((window_width - title_width) * 0.5)
                imgui.text(title_text)
                
                imgui.dummy(0, 20)
                
                # Buttons
                button_width = 200
                button_height = 40
                imgui.set_window_font_scale(1.0)
                
                # Save Game button
                imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
                if imgui.button("Save Game", width=button_width, height=button_height):
                    self.save_game()
                
                imgui.dummy(0, 10)
                
                # Load Game button
                imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
                if imgui.button("Load Game", width=button_width, height=button_height):
                    if self.load_game():
                        self.paused = False  # Unpause after successful load
                
                imgui.dummy(0, 10)
                
                # Main Menu button
                imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
                if imgui.button("Main Menu", width=button_width, height=button_height):
                    self.screen = 0
                    self.paused = False
                
                imgui.dummy(0, 10)
                
                # Resume button
                imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
                if imgui.button("Resume", width=button_width, height=button_height):
                    self.paused = False
                
                # Instructions
                
                
                imgui.end()

    def UpdateScene(self, inputs, time):
        if self.screen == 1:
            # Add pause toggle with F key
            if "F" in inputs and self.paused == False:
                self.paused = True
                return  # Skip updates when newly paused
            
            # Skip game updates if paused
            if self.paused:
                return

            # Update platform positions first
            for platform in self.platforms:
                pos = platform.properties['position']
                speed = platform.properties['speed']
                direction = platform.properties['direction']
                bounds = platform.properties['bounds']
                movement_type = platform.properties['movement_type']
                
                if movement_type == 'vertical':
                    new_y = pos[1] + speed * direction * time["deltaTime"]
                    if new_y > bounds[1] or new_y < bounds[0]:
                        platform.properties['direction'] *= -1
                    else:
                        platform.properties['position'][1] = new_y
                else:  # horizontal movement
                    new_x = pos[0] + speed * direction * time["deltaTime"]
                    if new_x > bounds[1] or new_x < bounds[0]:
                        platform.properties['direction'] *= -1
                    else:
                        platform.properties['position'][0] = new_x

            # Player movement
            move_x = 0.0
            move_y = 0.0  # Added back Y movement
            
            if "A" in inputs:
                move_x -= self.player_speed
            if "D" in inputs:
                move_x += self.player_speed
            if "W" in inputs:  # Added back W movement
                move_y += self.player_speed
            if "S" in inputs:  # Added back S movement
                move_y -= self.player_speed
            
            # Jump with spacebar when grounded
            if "SPACE" in inputs and self.is_grounded:
                self.player_velocity_z = self.jump_speed
                self.is_grounded = False
            
            # Only apply gravity if player is above ground level
            if self.player_position[2] > 0 or self.player_velocity_z > 0:
                self.player_velocity_z -= self.gravity * time["deltaTime"]
            else:
                self.player_position[2] = 0
                self.player_velocity_z = 0
                self.is_grounded = True
            
            # Update position
            self.player_position[0] += move_x * time["deltaTime"]
            self.player_position[1] += move_y * time["deltaTime"]  # Added Y position update
            self.player_position[2] += self.player_velocity_z * time["deltaTime"]
            
            # Adjusted scale calculation
            base_scale = 20.0
            scale_factor = base_scale + ((self.player_position[2] / 100.0) * 5)
            
            # Update player object position and scale
            self.objects[1].properties['position'] = np.array([
                self.player_position[0],
                self.player_position[1],
                self.player_position[2]
            ], dtype=np.float32)
            
            self.objects[1].properties['scale'] = np.array([
                scale_factor,
                scale_factor,
                1.0
            ], dtype=np.float32)

            self.check_collisions(time["deltaTime"])

    def DrawScene(self):
        self.camera.Update(self.shader)
        
        for obj in self.objects:
            # Only draw keys that haven't been collected
            if not (isinstance(obj, Object) and 
                   'collected' in obj.properties and 
                   obj.properties['collected']):
                obj.Draw()
            
    def check_collisions(self, deltaTime):
        player_pos = self.objects[1].properties['position']
        player_radius = 30

        self.is_grounded = False

        # Check platform collisions
        for platform in self.platforms:
            platform_pos = platform.properties['position']
            distance = np.sqrt(
                (player_pos[0] - platform_pos[0])**2 + 
                (player_pos[1] - platform_pos[1])**2
            )
            
            if distance < 60:
                if player_pos[2] > platform_pos[2]:
                    self.is_grounded = True
                    self.player_position[2] = platform_pos[2] + 40
                    self.player_velocity_z = 0

        # Check key collection
        for key in self.keys:
            if not key.properties['collected']:
                key_pos = key.properties['position']
                key_distance = np.sqrt(
                    (player_pos[0] - key_pos[0])**2 + 
                    (player_pos[1] - key_pos[1])**2
                )
                if key_distance < 70:
                    key.properties['collected'] = True
                    self.keys_collected += 1
                    print(f"Key collected! Total: {self.keys_collected}/3")

        # Ground (banks) collision
        if self.player_position[0] <= -400 or self.player_position[0] >= 400:
            if self.player_position[2] <= 0:
                self.player_position[2] = 0
                self.player_velocity_z = 0
                self.is_grounded = True

        # Check if in water and not on platform
        if -400 < player_pos[0] < 400 and not self.is_grounded:
            if self.player_position[2] <= 10:  # Small threshold for water level
                if self.player_lives > 1:  # Changed from > 0 to > 1
                    self.player_lives -= 1
                    self.player_health = 100
                    self.player_position = np.array([-450, 0, 0], dtype=np.float32)
                    self.player_velocity_z = 0
                    self.is_grounded = True
                    self.objects[1].properties['position'] = self.player_position
                else:
                    # Game Over
                    self.screen = 3
            self.player_speed = 250.0
        else:
            self.player_speed = 500.0

        # Check win condition
        if (player_pos[0] > 400) and (player_pos[1] > -50) and (player_pos[1] < 50) and (self.keys_collected == 3):
            self.screen = 2
            return

    def save_game(self):
        save_data = {
            'lives': self.player_lives,
            'health': self.player_health,
            'keys_collected': self.keys_collected,
            'elapsed_time': self.elapsed_time,
            'platform_data': [
                {
                    'position': platform.properties['position'].tolist(),
                    'movement_type': platform.properties['movement_type'],
                    'speed': platform.properties['speed'],
                    'direction': platform.properties['direction'],
                    'bounds': platform.properties['bounds']
                } for platform in self.platforms
            ],
            'key_data': [
                {
                    'position': key.properties['position'].tolist(),
                    'collected': key.properties['collected']
                } for key in self.keys
            ]
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=4)
            print("Game saved successfully!")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        try:
            if not os.path.exists(self.save_file):
                print("No save file found!")
                return False

            with open(self.save_file, 'r') as f:
                save_data = json.load(f)

            # Reset current game state
            self.objects = [
                Object(self.shader, backgroundProps),
                Object(self.shader, playerProps)
            ]
            
            # Load player stats
            self.player_lives = save_data['lives']
            self.player_health = save_data['health']
            self.keys_collected = save_data['keys_collected']
            self.elapsed_time = save_data['elapsed_time']
            
            # Clear and reload platforms
            self.platforms = []
            for platform_data in save_data['platform_data']:
                platform_props = copy.deepcopy(platformProps)
                platform_props['position'] = np.array(platform_data['position'], dtype=np.float32)
                platform_props['movement_type'] = platform_data['movement_type']
                platform_props['speed'] = platform_data['speed']
                platform_props['direction'] = platform_data['direction']
                platform_props['bounds'] = platform_data['bounds']
                
                platform = Object(self.shader, platform_props)
                self.platforms.append(platform)
                self.objects.append(platform)

            # Clear and reload keys
            self.keys = []
            for key_data in save_data['key_data']:
                key_props = copy.deepcopy(keyProps)
                key_props['position'] = np.array(key_data['position'], dtype=np.float32)
                key_props['collected'] = key_data['collected']
                
                key = Object(self.shader, key_props)
                self.keys.append(key)
                self.objects.append(key)

            # Reset player position to spawn
            self.player_position = np.array([-450, 0, 0], dtype=np.float32)
            self.player_velocity_z = 0
            self.is_grounded = True
            self.objects[1].properties['position'] = self.player_position
            
            print("Game loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return False

