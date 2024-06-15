from OpenGL.GL import * 
from objloader import ObjLoader
import pygame
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


# def render_model(model):
#     for mesh in model.mesh_list:
#         glPushMatrix()
#         glScalef(4, 4, 4)
#         glBegin(GL_TRIANGLES)
#         for face in mesh.faces:
#             print(face)
#             for vertex_index, texcoord_index in face:
#                 # Assuming texcoord_index gives you the index to fetch color from
#                 if texcoord_index is not None:
#                     glColor3fv(model.vertices[vertex_index].texcoords[texcoord_index])
#                 glVertex3fv(model.vertices[vertex_index].vertex)
#         glEnd()
#         glPopMatrix()
# #
# def load_model(filename):
#     return pywavefront.Wavefront(filename, collect_faces=True,parse=True)

def load_model(filename):
    indices, buffer = ObjLoader.load_model(f"objs/{filename}")
    return buffer
def draw_model( buffer):
    glPushMatrix()
    glScale(0.1,0.1,0.1)
    glBegin(GL_TRIANGLES)
    for i in range(0, len(buffer),8):
        vertex_index =i  
        texcoord_index = i + 3
        normal_index =i  + 5
        glVertex3f(buffer[vertex_index], buffer[vertex_index + 1], buffer[vertex_index + 2])
        glTexCoord2f(buffer[texcoord_index], buffer[texcoord_index + 1])
        glNormal3f(buffer[normal_index], buffer[normal_index + 1], buffer[normal_index + 2])
    glEnd()
    glPopMatrix()

# def load_ply(filename):
#     plydata = PlyData.read(filename)
#     vertex_data = plydata['vertex']
#     print("Available vertex properties are",vertex_data) 
#     if 'red' in vertex_data.data.dtype.names:
#         colors = np.vstack([vertex_data['red'], vertex_data['green'], vertex_data['blue']]).T / 255.0
#     elif 'r' in vertex_data.data.dtype.names:
#         colors = np.vstack([vertex_data['r'], vertex_data['g'], vertex_data['b']]).T / 255.0
#     else:
#         raise ValueError("No suitable color fields found in the PLY file")
#     
#     vertices = np.vstack([vertex_data['x'], vertex_data['y'], vertex_data['z']]).T
#     return vertices, colors
# def render_ply(vertices, colors):
#     glBegin(GL_TRIANGLES)
#     for i in range(len(vertices)):
#         glColor3f(colors[i][0], colors[i][1], colors[i][2])
#         glVertex3f(vertices[i][0], vertices[i][1], vertices[i][2])
#     glEnd()
