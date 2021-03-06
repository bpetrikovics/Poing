import random

from animations import FadeOut, BallBounceOff, Flash
from color import Color
from entities import Pad, Ball
from hud import Hud
from interfaces import IScene
from pynput import keyboard as kb


class SinglePlayerScene(IScene):
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
        print(f"{self}: created")
        self.width = None
        self.height = None

        self.paused = False
        self.ended = False

        self.hud = Hud()

        self.keyboard = keyboard_manager
        self.fullscreen_callback = None

        # these will be initialized once we have our display dimensions
        self.ball = None
        self.pad = None

        self.init_hud()

    def init_hud(self):
        self.hud.update({"text": "Q/A: move pad\nSPACE: pause\nF: toggle fullscreen"})

    def pause(self):
        if self.paused:
            return
        self.paused = True
        self.hud.update({"text": "Spacebar to unpause"})

    def unpause(self):
        if not self.paused:
            return
        self.paused = False
        self.init_hud()

    def set_display_dimensions(self, width: int, height: int):
        print(f"{self}: received display dimensions")
        self.width = width
        self.height = height
        self.hud.reshape(width, height)

        random.seed()
        self.ball = Ball(random.randint(50, self.width), random.randint(0, self.height), SinglePlayerScene.BALL_XSIZE,
                         SinglePlayerScene.BALL_YSIZE, SinglePlayerScene.PAD_COLOR)
        self.ball.c = SinglePlayerScene.BALL_COLOR
        self.ball.set_speed(SinglePlayerScene.BALL_SPEED_X, SinglePlayerScene.BALL_SPEED_Y)

        self.pad = Pad(5, int(self.height / 2 - SinglePlayerScene.PAD_YSIZE / 2), SinglePlayerScene.PAD_XSIZE,
                       SinglePlayerScene.PAD_YSIZE, SinglePlayerScene.BALL_COLOR)
        self.ball.c = SinglePlayerScene.PAD_COLOR

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
            print(f"{self}: restarting")
            self.init_hud()
            self.ended = False
            random.seed()
            self.ball.set_coords(random.randint(50, self.width), random.randint(0, self.height))
            self.ball.clear_animations()
            self.ball.set_color(SinglePlayerScene.BALL_COLOR)
            self.ball.set_speed(SinglePlayerScene.BALL_SPEED_X, SinglePlayerScene.BALL_SPEED_Y)

        # To help us tell whether the pad is moving right now, and if yes, its direction
        pad_move = 0

        if not self.ended and self.keyboard.is_pressed('a'):
            self.pad.move_by(0, SinglePlayerScene.PAD_MOVE_FACTOR)
            pad_move = 1

        if not self.ended and self.keyboard.is_pressed('q'):
            self.pad.move_by(0, -SinglePlayerScene.PAD_MOVE_FACTOR)
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
        self.hud.draw()

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
                    self.hud.update({"text": "Game over\nR to restart"})

        if not self.ended and self.ball.x + self.ball.width > self.width:
            self.ball.bounce_x()

        if not self.ended and self.ball.y < 0 or self.ball.y + self.ball.height > self.height:
            self.ball.bounce_y()

    def reshape(self, width: int, height: int):
        print(f"{self}: received new resolution {width}x{height}")
        self.width = width
        self.height = height

        self.hud.reshape(width, height)

        # Check if objects are out of screen after a resize
        # Ball first
        if self.ball.x + self.ball.width > self.width or self.ball.y + self.ball.height > self.height:
            self.ended = True
            self.hud.update({"text": "Ball out of bounds\nR to restart"})
        # Then the pad
        if self.pad.y < 0:
            self.pad.y = 0
        elif self.pad.y + self.pad.height > self.height:
            self.pad.y = self.height - self.pad.height

    def __repr__(self):
        return "<scenes.SinglePlayerScene>"
