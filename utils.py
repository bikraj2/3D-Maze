from OpenGL.GL import * 
from OpenGL.raw.GL.ARB import texture_view
from PIL import Image
import numpy as np
import pygame
import pywavefront
def glRGBColor(red:int,blue:int,green:int):
    glColor3fv( [red/256,blue/256,green/256])
def load_texture(img_path):
    image = pygame.image.load(img_path)
    img_data = pygame.image.tostring(image, 'RGB', 1)
    width, height = image.get_width(), image.get_height()

    # Enable texture mapping
    texture_id = glGenTextures(1)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glClearColor(1, 0, 0, 0) 
    
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)  
    return texture_id

def render_model(model):
    for mesh in model.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*model.vertices[vertex_i])
        glEnd()


def load_model(filename):
    return pywavefront.Wavefront(filename, collect_faces=True)
