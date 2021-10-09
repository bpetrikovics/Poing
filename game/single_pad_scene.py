import random

import OpenGL.GL as gl
import OpenGL.GLUT as glut
from pynput import keyboard as kb

from animations import FadeOut, BallBounceOff, Flash
from color import Color
from entities import Pad, Ball
from interfaces import IScene


class SinglePadScene(IScene):
    """ Defines a single pad game scene """

    BALL_COLOR = Color(255, 255, 255)
    BALL_XSIZE = 20
    BALL_YSIZE = 20
    BALL_SPEED_X = 3
    BALL_SPEED_Y = 3

    PAD_COLOR = Color(255, 255, 255)
    PAD_XSIZE = 10
    PAD_YSIZE = 100
    PAD_MOVE_FACTOR = 5

    def __init__(self, keyboard_manager):
        print("SinglePadScene: created")
        self.width = None
        self.height = None

        self.paused = False
        self.ended = False

        self.keyboard = keyboard_manager
        self.fullscreen_callback = None

        # these will be initialized once we have our display dimensions
        self.ball = None
        self.pad = None

    def pause(self):
        if self.paused:
            return
        self.paused = True

    def unpause(self):
        if not self.paused:
            return
        self.paused = False

    def set_display_dimensions(self, width: int, height: int):
        print(f"SinglePadScene: received display dimensions")
        self.width = width
        self.height = height

        self.ball = Ball(int(self.width / 2), int(self.height / 2), SinglePadScene.BALL_XSIZE, SinglePadScene.BALL_YSIZE, SinglePadScene.PAD_COLOR)
        self.ball.c = SinglePadScene.BALL_COLOR
        self.ball.set_speed(SinglePadScene.BALL_SPEED_X, SinglePadScene.BALL_SPEED_Y)

        self.pad = Pad(5, 0, SinglePadScene.PAD_XSIZE, SinglePadScene.PAD_YSIZE, SinglePadScene.BALL_COLOR)
        self.ball.c = SinglePadScene.PAD_COLOR

    def update(self, dt):
        # Check keyboard
        next_key = self.keyboard.next()

        # Spacebar for pause
        if next_key == kb.Key.space:
            if self.paused:
                self.unpause()
            else:
                self.pause()
        # Toggle fullscreen
        elif next_key == kb.KeyCode.from_char('f'):
            if self.fullscreen_callback:
                self.fullscreen_callback()
            pass
        # 'r' to restart when game ended
        elif self.ended and next_key == kb.KeyCode.from_char('r'):
            print("SinglePadScene: restarting")
            self.ended = False
            random.seed()
            self.ball.set_coords(random.randint(50, self.width), random.randint(0, self.height))
            self.ball.clear_animations()
            self.ball.set_color(SinglePadScene.BALL_COLOR)
            self.ball.set_speed(SinglePadScene.BALL_SPEED_X, SinglePadScene.BALL_SPEED_Y)

        pad_move = 0

        if not self.ended and self.keyboard.is_pressed('a'):
            self.pad.move_by(0, SinglePadScene.PAD_MOVE_FACTOR)
            pad_move = 1

        if not self.ended and self.keyboard.is_pressed('q'):
            self.pad.move_by(0, -SinglePadScene.PAD_MOVE_FACTOR)
            pad_move = -1

        if self.pad.y < 0:
            self.pad.y = 0
        if self.pad.y + self.pad.height > self.height:
            self.pad.y = self.height - self.pad.height

        # Need to update even when game ended so we properly run animations
        if not self.paused:
            self.ball.update(dt)
            self.pad.update(dt)

        self.ball.draw()
        self.pad.draw()

        # Ball at pad width distance from the left wall, checking for collision with the pad
        if self.ball.x <= self.pad.x + self.pad.width:
            if self.ball.y <= self.pad.y + self.pad.height and self.ball.y + self.ball.height >= self.pad.y:
                # Ball is touching the pad, bouncing back
                # If the pad was moving, also adjust vertical speed
                self.ball.bounce_x(pad_move)
                self.ball.increase_speed()
                self.pad.add_animation(Flash(Color(255, 64, 64), speed=500))
                if pad_move:
                    self.ball.add_animation(Flash(Color(64, 128, 255)))
            else:
                # We hit the wall
                if self.ball.x <= 0 and self.ended is not True:
                    self.ended = True
                    # how to detect if animations are over?
                    self.ball.clear_animations()
                    self.ball.add_animation(FadeOut(Color(255, 150, 150)))
                    self.ball.add_animation(BallBounceOff(self))

        if not self.ended and self.ball.x + self.ball.width > self.width:
            self.ball.bounce_x()

        if not self.ended and self.ball.y < 0 or self.ball.y + self.ball.height > self.height:
            self.ball.bounce_y()

        # show what we've drawn
        glut.glutSwapBuffers()

    def reshape(self, width: int, height: int):
        print(f"SinglePadScene: reshape to {width}x{height}")
        self.width = width
        self.height = height
        gl.glViewport(0, 0, width, height)

        # Check if objects are out of screen after a resize
        # Ball first
        if self.ball.x+self.ball.width > self.width or self.ball.y+self.ball.height > self.height:
            self.ended = True
        # Then the pad
        if self.pad.y < 0:
            self.pad.y = 0
        elif self.pad.y+self.pad.height > self.height:
            self.pad.y = self.height - self.pad.height

    def __repr__(self):
        return "<SinglePadScene>"
