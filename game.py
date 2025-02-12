import imgui
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader

class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = -1
        self.camera = Camera(height, width)
        self.shaders = [Shader(object_shader['vertex_shader'], object_shader['fragment_shader'])]
        self.objects = []

    def InitScreen(self):
        if self.screen == 0:
            pass
        if self.screen == 1:
            pass
        if self.screen == 2:
            pass
    def ProcessFrame(self, inputs, time):
        if self.screen == -1:
            self.screen = 0
            self.InitScreen()
        if self.screen == 0:
            self.DrawText()
            self.UpdateScene(inputs, time)
        if self.screen == 1:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
    def DrawText(self):
        if self.screen == 0:
           pass
        if self.screen == 1:
           pass
        if self.screen == 2:
           pass
    def UpdateScene(self, inputs, time):
        if self.screen == 0:
            pass
        if self.screen == 1:
          pass
            
    def DrawScene(self):
        if self.screen == 1:
            for shader in self.shaders:
                self.camera.Update(shader)
 
            for obj in self.objects:
                obj.Draw()
            
            
        

