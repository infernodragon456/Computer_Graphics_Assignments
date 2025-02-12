import imgui
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from assets.objects.objects import playerProps, backgroundProps

class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = -1  # -1: uninitialized, 0: menu, 1: game
        self.camera = Camera(height, width)
        self.shader = Shader(object_shader['vertex_shader'], object_shader['fragment_shader'])
        self.objects = []

    def InitScreen(self):
        if self.screen == 1:  # Only initialize game objects when starting game
            self.objects = [
                Object(self.shader, backgroundProps),
                Object(self.shader, playerProps)
            ]

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

    def UpdateScene(self, inputs, time):
        if self.screen == 1:
            pass  # Add game update logic here

    def DrawScene(self):
        self.camera.Update(self.shader)
        for obj in self.objects:
            obj.Draw()

        

