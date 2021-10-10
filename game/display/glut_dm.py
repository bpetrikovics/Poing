import sys
import time

import OpenGL.GL as gl
import OpenGL.GLUT as glut

from interfaces import IScene


class DisplayManager:
    """ A display manager implementation using GLUT """

    TARGET_FPS = 60
    FRAME_TIME = 1 / TARGET_FPS

    def __init__(self, width: int, height: int, title: str):
        self.width = self.original_width = width
        self.height = self.original_height = height
        self.fullscreen = False
        self.title = title
        self.scene = None

        self.old_time = None
        self.new_time = None
        self.time_diff = 0
        self.tick = 0
        self.elapsed = 0

        print("DisplayManager: checking GLUT")
        if not bool(glut.glutInit):
            print("OpenGL not installed?")
            sys.exit(1)

        print(f"DisplayManager: init {width}x{height}")

        # Initialize a glut instance which will allow us to customize our window
        glut.glutInit()

        glut.glutInitDisplayMode(glut.GLUT_RGBA)  # Set the display mode to be colored
        glut.glutInitWindowSize(width, height)  # Set the width and height of your window

        self.window = glut.glutCreateWindow(title)

    def set_scene(self, scene: IScene):
        print("DisplayManager: setting refresh functions to scene")

        self.scene = scene
        self.scene.set_display_dimensions(self.width, self.height)
        self.scene.set_fullscreen_callback(self.toggle_fullscreen)

        glut.glutDisplayFunc(self.update)  # Tell OpenGL to call the showScreen method continuously
        glut.glutIdleFunc(self.update)  # Draw any graphics or shapes in the showScreen function at all times

        glut.glutReshapeFunc(self.reshape)  # Called whenever window is resized

    def refresh2d(self):
        gl.glViewport(0, 0, self.width, self.height)

        # Set up properties of camera view
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, self.width, self.height, 0.0, 0.0, 1.0)

        # Set up object transformation
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    @staticmethod
    def clear():
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

    def update(self):
        self.clear()
        self.refresh2d()

        self.scene.update(self.time_diff)

        glut.glutSwapBuffers()

        # Timekeeping
        self.old_time = self.new_time
        self.new_time = time.time()

        # first cycle, we cannot compute interval yet
        if self.old_time is None:
            return

        self.time_diff = self.new_time - self.old_time
        self.elapsed += self.time_diff
        fps = 1.0 / self.time_diff
        sleep_time = DisplayManager.FRAME_TIME - self.time_diff if self.time_diff < DisplayManager.FRAME_TIME else 0

        self.tick += 1
        if self.elapsed >= 1:
            glut.glutSetWindowTitle(
                f"{self.title} | {fps:.2f} FPS dt={self.time_diff:.4f} ticks={self.tick} elapsed={self.elapsed:.4f}")
            self.tick = 0
            self.elapsed = 0

        if sleep_time != 0:
            time.sleep(sleep_time)

    def reshape(self, width: int, height: int):
        print(f"DisplayManager: reshape from ({self.width}x{self.height}) to ({width}x{height})")
        gl.glViewport(0, 0, width, height)
        self.width = width
        self.height = height
        self.scene.reshape(width, height)

    def toggle_fullscreen(self):
        if self.fullscreen:
            print("DisplayManager: switching back from fullscreen")
            glut.glutPositionWindow(0, 0)
            glut.glutReshapeWindow(self.original_width, self.original_height)
            self.fullscreen = False
        else:
            print("Display: setting fullscreen")
            self.original_width = self.width
            self.original_height = self.height
            glut.glutFullScreen(self.window)
            self.fullscreen = True

    @staticmethod
    def main_loop():
        print("DisplayManager: starting the mainloop")
        glut.glutMainLoop()  # Keeps the window created above displaying/running in a loop
