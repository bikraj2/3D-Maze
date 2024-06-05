from OpenGL.GLUT import *
from utils import display,keyboard,mouse_motion,reshape,init
from cube import cube
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1080, 720)
    glutCreateWindow("OpenGL Cube")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutPassiveMotionFunc(mouse_motion)
    glutKeyboardFunc(keyboard)
     
    init()
    # draw_axes()
    glutMainLoop()

if __name__ == "__main__":
    main()
