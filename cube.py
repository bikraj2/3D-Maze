
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from utils import  glRGBColor, load_texture
from generate_maze import Maze
camera_pos = np.array([0.0, 0.7, 5.0])
camera_1 = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw = -90.0  # yaw is initialized to -90.0 to look along the -Z axis
pitch = 0.0
lastX, lastY = 400, 300
first_mouse = True
sensitivity = 0.1
texture_id_1=0
texture_id_2=0
texture_id_3=0
texture_id_ground=0
maze = Maze(10,10)
generated_maze = maze.maze
print(np.matrix(generated_maze))
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
def display():
    global x_rotation, y_rotation, z_rotation,generated_maze,maze
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_pos[0] + camera_1[0], camera_pos[1] + camera_1[1], camera_pos[2] + camera_1[2],
              camera_up[0], camera_up[1], camera_up[2])
    for i in range(maze.width):
        for j in range(maze.height):
            if generated_maze[i][j]==1:
                glPushMatrix()
                glTranslatef((-5+i)*2,0,(-5+j)*2 )
                cube()
                glPopMatrix() 
    # glBegin(GL_QUADS)
    # glVertex3f(-25,-1,-25)
    # glVertex3f(-25,-1,25)
    # glVertex3f(25,-1,25)
    # glVertex3f(25,-1,-25)
    # glEnd()
    glutSwapBuffers()
def check_collision(new_pos):
    global generated_maze, maze
    camera_size = 0.1  # Size of the camera's bounding box
    for i in range(maze.width):
        for j in range(maze.height):
            if generated_maze[i][j] == 1:
                wall_pos = np.array([(-5 + i) * 2, 0, (-5 + j) * 2])
                if (np.abs(new_pos[0] - wall_pos[0]) < camera_size + 1 and
                    np.abs(new_pos[2] - wall_pos[2]) < camera_size + 1):
                    return True
    return False
def reshape(width, height):
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    fov = 75
    gluPerspective(fov, aspect_ratio, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,10,0,0,0,0,0,-1,0)
    glLoadIdentity()

def keyboard(key, x, y):
    global camera_pos, camera_1, camera_up
    camera_speed = 0.1
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
    int_camera_pos[1]=0.7
    
    # if not check_collision(int_camera_pos):
    camera_pos[:] = int_camera_pos
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
    y_offset *= sensitivity

    yaw += x_offset

    # Constrain the pitch
    if pitch > 89.0:
        pitch = 89.0
    
    print("yaw",yaw)
    # Update camer 1 vector
    front = np.array([
        np.cos(np.radians(yaw)) * np.cos(np.radians(pitch)),
        np.sin(np.radians(pitch)),
        np.sin(np.radians(yaw)) * np.cos(np.radians(pitch))
    ])
    camera_1 = front / np.linalg.norm(1)
    glutPostRedisplay()
def main():
    global texture_id_1,texture_id_2,texture_id_3,texture_id_ground,generated_maze
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(2440, 1080)
    glutCreateWindow("OpenGL Cube")

    init()
    texture_id_1 = load_texture("minecraft.jpg")
    texture_id_2 = load_texture("minecraft_top.jpg")
    texture_id_3 =load_texture('minecraft_bottom.jpg')
    texture_id_ground = load_texture("minecraft_bottom.jpg")
         
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutPassiveMotionFunc(mouse_motion)
    glutKeyboardFunc(keyboard)
    # draw_axes()
    glutMainLoop()
# def ground():
#     global texture_id_ground
#     glBindTexture(GL_TEXTURE_2D, texture_id_ground)
#     glBegin(GL_QUADS)
#     # Define the vertices for the ground plane
#     size = 1.0  # Adjust the size as needed
#     glTexCoord2f(0.0, 0.0)
#     glVertex3f(-size, -1.0, -size)
#     glTexCoord2f(size, 0.0)
#     glVertex3f(size, -1.0, -size)
#     glTexCoord2f(size, size)
#     glVertex3f(size, -1.0, size)
#     glTexCoord2f(0.0, size)
#     glVertex3f(-size, -1.0, size)
#     glEnd()
   

def cube():
    global texture_id_1, texture_id_2,texture_id_3
    

    # 1 face (use texture_id_1)
    glBindTexture(GL_TEXTURE_2D, texture_id_1)
    glBegin(GL_QUADS)
    # 1 Face
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glEnd()

    # Back face
    glBindTexture(GL_TEXTURE_2D, texture_id_1)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glEnd()

    # 2 face (use texture_id_2)
    glBindTexture(GL_TEXTURE_2D, texture_id_2)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glEnd()

    # Bottom face
    glBindTexture(GL_TEXTURE_2D, texture_id_3)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glEnd()

    # Right face
    glBindTexture(GL_TEXTURE_2D, texture_id_1)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, -1.0,1.0) 
    glEnd()
    glBindTexture(GL_TEXTURE_2D, texture_id_1)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glEnd()
    glClearColor(0,0,0,1)
# def draw_axes():
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
