#!/usr/bin/env python3

""" Minimal "Pong" game with OpenGL (immediate mode) graphics """

# https://stackabuse.com/brief-introduction-to-opengl-in-python-with-pyopengl/
# https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/

import sys
import os.path

WIDTH = 1280
HEIGHT = 720


def main():
    display_manager = DisplayManager(WIDTH, HEIGHT, "Poing!")
    keyboard_manager = KeyboardManager()
    scene = Scene(keyboard_manager)

    # This sets GLUT's display update callbacks to the scene
    # (multiple scenes supported this way). Will also allow the active scene
    # to send callbacks
    display_manager.set_scene(scene)

    # Will run the GLUT main loop, not returning
    display_manager.main_loop()


if __name__ == '__main__':
    app_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(app_dir, "game"))

    from venvtools import activate
    activate(app_dir)

    from keyboard_manager import KeyboardManager

    from scenes import SinglePadScene as Scene
    from display import GLFWdm as DisplayManager

    main()
