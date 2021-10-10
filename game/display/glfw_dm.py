import sys
import time

import OpenGL.GL as gl
import glfw

from interfaces import IScene


class DisplayManager:
    """ A display manager implementation using GLFW """

    TARGET_FPS = 60
    FRAME_TIME = 1 / TARGET_FPS
    VSYNC = False
    DOUBLEBUFFER = glfw.TRUE

    def __init__(self, width: int, height: int, title: str):
        self.width = self.original_width = width
        self.height = self.original_height = height
        self.original_x = self.original_y = None;
        self.fullscreen = False
        self.title = title
        self.scene = None

        self.old_time = None
        self.new_time = None
        self.time_diff = 0
        self.tick = 0
        self.elapsed = 0

        glfw.set_error_callback(self.glfw_error_callback)

        if not glfw.init():
            print("Could not initialize GLFW, exiting")
            sys.exit(-1)

        print(
            f"DisplayManager: GLFW {glfw.VERSION_MAJOR}.{glfw.VERSION_MINOR}.{glfw.VERSION_REVISION} init {width}x{height}")

        # These are the default values anyway
        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
        glfw.window_hint(glfw.DOUBLEBUFFER, DisplayManager.DOUBLEBUFFER)

        # Antialiasing (0, 4)
        glfw.window_hint(glfw.SAMPLES, 4)

        # OpenGL API version for our context
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

        # We use compat profile to stay compatible with the older immediate mode code
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)

        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            print("DisplayManager: Could not create window, exiting")
            sys.exit(-1)

        glfw.make_context_current(self.window)
        glfw.swap_interval(DisplayManager.VSYNC)
        glfw.set_window_size_callback(self.window, self.reshape)

        gl.glClearColor(0, 0, 0, 0)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_DEPTH_TEST)

    @staticmethod
    def glfw_error_callback(error: int, description: str):
        print(f"GLFW error {error}: {description.decode('UTF-8')}")

    def set_scene(self, scene: IScene):
        print("DisplayManager: setting refresh functions to scene")

        self.scene = scene
        self.scene.set_display_dimensions(self.width, self.height)
        self.scene.set_fullscreen_callback(self.toggle_fullscreen)

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
        glfw.poll_events()

        self.clear()
        self.refresh2d()

        self.scene.update(self.time_diff)

        glfw.swap_buffers(self.window)

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
            glfw.set_window_title(self.window,
                                  f"{self.title} | {fps:.2f} FPS dt={self.time_diff:.4f} ticks={self.tick} ")
            self.tick = 0
            self.elapsed = 0

        if sleep_time != 0:
            time.sleep(sleep_time)

    def reshape(self, window, width: int, height: int):
        print(f"DisplayManager: reshape from ({self.width}x{self.height}) to ({width}x{height})")
        gl.glViewport(0, 0, width, height)
        self.width = width
        self.height = height
        self.scene.reshape(width, height)

    def toggle_fullscreen(self):
        monitor = glfw.get_primary_monitor()
        screen_size = glfw.get_video_mode(monitor).size

        if self.fullscreen:
            print("DisplayManager: switching back from fullscreen")
            glfw.set_window_monitor(self.window, None, self.original_x, self.original_y, self.original_width,
                                    self.original_height, glfw.DONT_CARE)
            self.fullscreen = False
        else:
            print("Display: setting fullscreen")
            self.original_width = self.width
            self.original_height = self.height
            self.original_x, self.original_y = glfw.get_window_pos(self.window)
            print(f"Original x,y was {self.original_x}, {self.original_y}")
            glfw.set_window_monitor(self.window, monitor, 0, 0, screen_size.width, screen_size.height, glfw.DONT_CARE)
            self.fullscreen = True

    def main_loop(self):
        print("DisplayManager: starting the mainloop")
        while not glfw.window_should_close(self.window):
            self.update()

        glfw.terminate()
