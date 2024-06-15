
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from utils import  draw_model, load_model,  load_texture  
from generate_maze import Maze
# import math
camera_pos = np.array([0.0, 0.7, 5.0])
camera_1 = np.array([0.0, 0.0, 4.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw = 90.0  # yaw is initialized to -90.0 to look along the -Z axis
pitch = -17.0
lastX, lastY = 400, 300
first_mouse = True
sensitivity = 0.4
texture_id_1=0
texture_id_2=0
texture_id_3=0
texture_id_ground=0
chibi_texture = 0
maze = Maze(10,10)
first_person =False 
buffer1 =[]
generated_maze = maze.maze
running = True
jumping = False
jump_velocity = 0.2
gravity = -0.01
jump_height = 0.0
print(np.matrix(generated_maze))
object_pos = [camera_pos[0],-1.0,camera_pos[2]]
def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 10, 0))  # Position of the light
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.6, 0.6, 0.6, 1))  # Ambient light
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))  # Diffuse light
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))  # Specular light

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
def display():
    global x_rotation, y_rotation, z_rotation,generated_maze,maze,jumping,jump_height,jump_velocity

    glClearColor(135.0 /255.0 , 206.0 /255.0 , 235.0 /255.0 , 1.0 );
    glClear(GL_COLOR_BUFFER_BIT )
    glClear(GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)
    if first_person:    
        gluLookAt(object_pos[0], camera_pos[1], object_pos[2],
              camera_pos[0] + camera_1[0]*2, camera_pos[1] + camera_1[1]*2, camera_pos[2] + camera_1[2]*2,
              camera_up[0], camera_up[1], camera_up[2])
    else:
        look_from_above()
    # print(camera_pos)
    # print( camera_pos[0] + camera_1[0]*0.2, camera_pos[1] + camera_1[1]*0.2, camera_pos[2] + camera_1[2]*0.2)
    glEnable(GL_CULL_FACE);  # Enable face culling
    glCullFace(GL_BACK);  
    for i in range(maze.width):
        for j in range(maze.height):
            if generated_maze[i][j]==1: 
                glPushMatrix()
                glTranslatef((-5+i)*2,0,(-5+j)*2 )
                cube()

                glPopMatrix()
    for i in range(-10,maze.width+10):
        for j in range(-10,maze.height+10):
            glPushMatrix()
            glTranslatef((-5+i)*2,0,(-5+j)*2 )
            
            ground()
            glPopMatrix()    

    if jumping:
        jump_height += jump_velocity
        jump_velocity += gravity
        if jump_height <= 0.0:
            jump_height = 0.0
            jump_velocity = 0.2
            jumping = False
    render_camera_attached_object()

    glutSwapBuffers()

def look_from_above():
    global camera_pos
    maze_center_x = 0
    maze_center_z = 0
    cam_height = 50
    gluLookAt(maze_center_x, cam_height, maze_center_z,
              maze_center_x, 0, maze_center_z,
              0, 0, -1)
def check_collision(new_pos):
    global generated_maze, maze
    camera_size = 0.3  # Size of the camera's bounding box
    for i in range(maze.width):
        for j in range(maze.height):
            if generated_maze[i][j] == 1:
                wall_pos = np.array([(-5 + i) * 2, 0, (-5 + j) * 2])
                if (np.abs(new_pos[0] - wall_pos[0]) < camera_size +1 and
                    np.abs(new_pos[2] - wall_pos[2]) < camera_size +1 ):
                    return True
    return False
def reshape(width, height):
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    fov = 45 
    gluPerspective(   fov, aspect_ratio, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard(key, x, y):
    global camera_pos, camera_1, camera_up , running,first_person,object_pos,jumping,jump_velocity,jump_height
    camera_speed = 0.5
     # if key ==b'\x2'
    int_camera_pos = camera_pos.copy()
    if key == b'w':  # Move forward
        int_camera_pos+= camera_speed * camera_1
    elif key == b's':  # Move backward
        int_camera_pos-= camera_speed * camera_1
    elif key == b'a':  # Move left
        int_camera_pos -= np.cross(camera_1, camera_up) * camera_speed
    elif key == b'd':  # Move right
        int_camera_pos += np.cross(camera_1, camera_up) * camera_speed
    elif key == b't':  # Toggle top-down view
        first_person = not first_person 
    elif key == b'\x1b':  # ESC key to exit
        running = False
    elif key == b' ':  # Space key to jump
        if not jumping:
            jumping = True
            jump_height = 0.0
            jump_velocity = 0.2
    int_camera_pos[1]=1
    if not check_collision(int_camera_pos):
        camera_pos[:] = int_camera_pos
        object_pos = [camera_pos[0],0.5,camera_pos[2]]
    glutPostRedisplay()
def mouse_motion(x, y):
    global yaw, pitch, lastX, lastY, first_mouse, camera_1
    if first_mouse:
        lastX = x
        lastY = y
        first_mouse = False

    x_offset = x - lastX
    y_offset = lastY -y  # reversed since y-coordinates go from bottom to 2
    lastX = x
    lastY = y

    x_offset *= sensitivity
    y_offset *=sensitivity
    yaw += x_offset
    # Update camer 1 vector
    front = np.array([
        np.cos(np.radians(yaw)) * np.cos(np.radians(pitch)),
        np.sin(np.radians(pitch)),
        np.sin(np.radians(yaw)) * np.cos(np.radians(pitch))
    ])
    # print(front)
    # print(np.linalg.norm(4))
    camera_1 = front / np.linalg.norm(front)
    glutPostRedisplay()



def render_camera_attached_object(scale=0.5):
    global camera_pos, camera_front, object_offset,vertices,colors,buffer

    # Calculate the object's position relative to the camera
    glPushMatrix()
    glTranslatef(camera_pos[0], -0.5+jump_height, camera_pos[2])
    angle = np.degrees(np.arctan2(camera_1[2], camera_1[0])) - 90 
    glRotatef(-angle,0,1,0)
    glBindTexture(GL_TEXTURE_2D,chibi_texture)
    draw_model(buffer1)
    # render a cube with the given scale 
    glPopMatrix()
def main():
    global texture_id_1,texture_id_2,texture_id_3,texture_id_ground,generated_maze,chibi_texture,buffer1,buffer2
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1080, 720)
    glutCreateWindow("3D Maze")

    init()
    texture_id_1 = load_texture("minecraft.jpg")
    texture_id_2 = load_texture("minecraft_top.jpg")
    texture_id_3 =load_texture('minecraft_bottom.jpg')
    texture_id_ground = load_texture("minecraft_bottom.jpg")
    chibi_texture  = load_texture("chibi.png")
    buffer1 =load_model("chibi.obj")     
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutPassiveMotionFunc(mouse_motion)
    glutKeyboardFunc(keyboard)
    # draw_axes()
    glutMainLoop()


def ground():
    global texture_id_ground
    glBindTexture(GL_TEXTURE_2D, texture_id_ground)
    glBegin(GL_QUADS)
    # glColor3f(1,1,1)
    # Front face
    scale_x,scale_y,scale_z =1,1,1
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0 * scale_x, -1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0 * scale_x, -1.0 * scale_y,  1.0 * scale_z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0 * scale_x, -1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f( 1.0 * scale_x, -1.0 * scale_y, -1.0 * scale_z)
    glEnd()
def cube():
    global texture_id_1, texture_id_2, texture_id_3
    
    # Define the scaling factors for the cube
    scale_x = 1.0
    scale_y = 1.0
    scale_z = 1.0

    # 1 face (use texture_id_1)
    glBindTexture(GL_TEXTURE_2D, texture_id_1)
    glBegin(GL_QUADS)
    # glColor3f(1,1,1)
    # Front face
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0 * scale_x, -1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0 * scale_x, -1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0 * scale_x, 1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0 * scale_x, 1.0 * scale_y, 1.0 * scale_z)
    glEnd()

    # Back face
    glBindTexture(GL_TEXTURE_2D, texture_id_1)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0 * scale_x, -1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0 * scale_x, 1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0 * scale_x, 1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0 * scale_x, -1.0 * scale_y, -1.0 * scale_z)
    glEnd()

    # 2 face (use texture_id_2)
    glBindTexture(GL_TEXTURE_2D, texture_id_2)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0 * scale_x, 1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0 * scale_x, 1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0 * scale_x, 1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0 * scale_x, 1.0 * scale_y, -1.0 * scale_z)
    glEnd()

    # Bottom face
    glBindTexture(GL_TEXTURE_2D, texture_id_3)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0 * scale_x, -1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0 * scale_x, -1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0 * scale_x, -1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0 * scale_x, -1.0 * scale_y, 1.0 * scale_z)
    glEnd()

    # Right face
    glBindTexture(GL_TEXTURE_2D, texture_id_1)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0 * scale_x, -1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0 * scale_x, 1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0 * scale_x, 1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0 * scale_x, -1.0 * scale_y, 1.0 * scale_z) 
    glEnd()

    # Left face
    glBindTexture(GL_TEXTURE_2D, texture_id_1)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0 * scale_x, -1.0 * scale_y, -1.0 * scale_z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0 * scale_x, -1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0 * scale_x, 1.0 * scale_y, 1.0 * scale_z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0 * scale_x, 1.0 * scale_y, -1.0 * scale_z)
    glEnd()

    # glClearColor(0,0,0,1)# def draw_axes():
#     glBegin(GL_LINE)
#     glRGBColor(256,0,0)
#     glVertex3f(0,0,100)
#     glVertex3f(0,0,-100) 
#     glBegin(GL_LINE)
#     glRGBColor(0,256,0)
#     glVertex3f(0,100,0)
#     glVertex3f(0,-100,0)
#     glBegin(GL_LINE)
#     glRGBColor(0,0,256)
#     glVertex3f(100,0,0)
#     glVertex3f(-100,0,0)
# def generate
if __name__ == "__main__":
  main()
