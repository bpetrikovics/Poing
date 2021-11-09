#!/usr/bin/env python3

""" Minimal "Pong" game with OpenGL (immediate mode) graphics """

# https://stackabuse.com/brief-introduction-to-opengl-in-python-with-pyopengl/
# https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/

import sys
import os.path
import argparse

WIDTH = 1280
HEIGHT = 720


def main():
    display_manager = DisplayManager(WIDTH, HEIGHT, "Poing!")
    keyboard_manager = KeyboardManager()
    scene = Scene(keyboard_manager)

    # This sets display update callbacks to the scene's own methods
    # (multiple scenes supported this way). Will also allow the active scene
    # to send callbacks
    display_manager.set_scene(scene)

    display_manager.main_loop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A very simple OpenGL Pong game")
    parser.add_argument('--display',
                        type=str,
                        choices=['glut', 'glfw'],
                        default='glfw',
                        help='Display manager to use')
    args = parser.parse_args()

    app_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(app_dir, "game"))

    from venvtools import activate
    activate(app_dir)

    if args.display == 'glfw':
        from display import GLFWdm as DisplayManager
    elif args.display == 'glut':
        from display import GLUTdm as DisplayManager
    else:
        print('WTF')

    from keyboard_manager import KeyboardManager
    from scenes import SinglePlayerScene as Scene

    main()
