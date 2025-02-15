import imgui
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from assets.objects.objects import playerProps, backgroundProps, platformProps
import glfw
import copy

class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = -1  # -1: uninitialized, 0: menu, 1: game, 2: victory screen
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

    def InitScreen(self):
        if self.screen == 1:
            self.start_time = glfw.get_time()
            # Create background and player
            self.objects = [
                Object(self.shader, backgroundProps),
                Object(self.shader, playerProps)
            ]
            
            # Create platforms at different x positions
            platform_x_positions = [-200, 0, 200]  # Positions across the river
            for x_pos in platform_x_positions:
                platform_props = copy.deepcopy(platformProps)
                platform_props['position'] = np.array([x_pos, 0, 0], dtype=np.float32)
                platform = Object(self.shader, platform_props)
                self.platforms.append(platform)
                self.objects.append(platform)  # Add to objects for rendering

            # Set initial player position
            self.player_position = np.array([-400.0, 0.0, 0.0], dtype=np.float32)
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
            
            # Subtitle
            subtitle_text = "Start Menu"
            imgui.set_window_font_scale(1.5)  # Make subtitle slightly smaller than title
            subtitle_width = imgui.calc_text_size(subtitle_text).x
            imgui.set_cursor_pos_x((window_width - subtitle_width) * 0.5)
            imgui.text(subtitle_text)
            
            imgui.set_window_font_scale(1.0)  # Reset font scale for rest of UI
            
            imgui.dummy(0, 20)  # Add some vertical spacing
            
            # Buttons
            button_width = 200
            button_height = 40
            
            # Center each button
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("New Game", width=button_width, height=button_height):
                self.screen = 1
                self.InitScreen()
            
            imgui.dummy(0, 10)  # Space between buttons
            
            imgui.set_cursor_pos_x((window_width - button_width) * 0.5)
            if imgui.button("Load Game", width=button_width, height=button_height):
                pass  # Add settings functionality later
            
            imgui.dummy(0, 10)  # Space between buttons
            
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

    def UpdateScene(self, inputs, time):
        if self.screen == 1:
            # Calculate movement based on input
            move_x = 0.0
            move_y = 0.0
            
            # Use the inputs provided by window_manager
            if "W" in inputs:
                move_y += self.player_speed
            if "S" in inputs:
                move_y -= self.player_speed
            if "A" in inputs:
                move_x -= self.player_speed
            if "D" in inputs:
                move_x += self.player_speed

            # Normalize movement vector
            magnitude = np.sqrt(move_x**2 + move_y**2)
            if magnitude > 0:
                move_x = move_x / magnitude
                move_y = move_y / magnitude

            # Store old position for collision resolution
            old_position = self.player_position.copy()

            # Update player position using deltaTime for smooth movement
            self.player_position[0] += move_x * time["deltaTime"] * self.player_speed
            self.player_position[1] += move_y * time["deltaTime"] * self.player_speed

            # Add boundaries to keep player on screen
            self.player_position[0] = max(-500, min(500, self.player_position[0]))
            self.player_position[1] = max(-500, min(500, self.player_position[1]))

            # Update platform positions
            for platform in self.platforms:
                pos = platform.properties['position']
                speed = platform.properties['speed']
                direction = platform.properties['direction']
                bounds = platform.properties['bounds']
                
                # Update Y position
                new_y = pos[1] + speed * direction * time["deltaTime"]
                
                # Check bounds and reverse direction if needed
                if new_y > bounds[1] or new_y < bounds[0]:
                    platform.properties['direction'] *= -1
                else:
                    platform.properties['position'][1] = new_y

            # Update player position and check collisions
            self.objects[1].properties['position'] = np.array([
                self.player_position[0], 
                self.player_position[1], 
                0
            ], dtype=np.float32)
            
            self.check_collisions(time["deltaTime"])

    def DrawScene(self):
        self.camera.Update(self.shader)
        
        for obj in self.objects:
            obj.Draw()
            
            
    def check_collisions(self, deltaTime):
        player_pos = self.objects[1].properties['position']
        player_radius = 30

        # Check platform collisions
        for platform in self.platforms:
            platform_pos = platform.properties['position']
            # Simple AABB collision check
            if (abs(player_pos[0] - platform_pos[0]) < 50 and  # Platform width is 100
                abs(player_pos[1] - platform_pos[1]) < 25):    # Platform height is 50
                # Player is on platform, don't apply water damage
                return

        # Check river boundaries
        left_bank = -400.0
        right_bank = 400.0

        # Check win condition
        if np.allclose(player_pos, np.array([400, 0, 0], dtype=np.float32), rtol=1e-5):
            self.screen = 2
            return

        # Check if player is in the river
        if left_bank < player_pos[0] < right_bank:
            self.player_speed = 250.0
            damage_per_second = 5
            damage_this_frame = int(damage_per_second * deltaTime)
            if damage_this_frame > 0:
                self.player_health = max(0, self.player_health - damage_this_frame)
            
            if self.player_health <= 0 and self.player_lives > 0:
                self.player_lives -= 1
                self.player_health = 100
                self.player_position = np.array([-450, 0, 0], dtype=np.float32)
                self.objects[1].properties['position'] = self.player_position
        else:
            self.player_speed = 500.0

