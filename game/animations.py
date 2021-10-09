from interfaces import IMovable, IAnimation, IScene
from color import Color


class FadeOut(IAnimation):
    """ Applies fadeout effect on a ColorableMixin object, from a given color """

    COLOR_SPEED = 180

    def __init__(self, color: Color):
        print(f"Animation.FadeOut: starting from {color}")
        self.target = None
        self.color = color
        self.color_r = color.r
        self.color_g = color.g
        self.color_b = color.b

    def update(self, dt):
        self.color_r = int(max(self.color_r - FadeOut.COLOR_SPEED * dt, 0))
        self.color_g = int(max(self.color_g - FadeOut.COLOR_SPEED * dt, 0))
        self.color_b = int(max(self.color_b - FadeOut.COLOR_SPEED * dt, 0))

        out_color = Color(self.color_r, self.color_g, self.color_b)
        self.target.set_color(out_color)

    def is_finished(self) -> bool:
        return self.color_r == 0 and self.color_g == 0 and self.color_b == 0

    def set_target(self, target: IMovable):
        print(f"Animation.FadeOut: got target={target}")
        self.target = target

    def __repr__(self):
        return f"<FadeOut color={self.color}>"


class BallBounceOff(IAnimation):
    """ Bounce animation to be played when the pad misses the ball, should be used with FadeOut """

    ACCEL_Y = 15

    def __init__(self, scene: IScene):

        print(f"Animation.BallBounceOff: scene is {scene}")
        self.target = None
        self.scene = scene

    def update(self, dt: int):
        self.speed_y += BallBounceOff.ACCEL_Y * dt
        self.target.set_speed(self.speed_x, int(self.speed_y))

    def is_finished(self) -> bool:
        return self.target.y >= self.scene.height

    def set_target(self, target: IMovable):
        self.target = target
        (self.speed_x, self.speed_y) = target.get_speed()

        print(f"Animation.BallBounceOff: got target={target}, initial object speed is (dx={self.speed_x}, dy={self.speed_y})")

        self.speed_x *= -1
        self.speed_y = -5

        target.set_speed(self.speed_x, self.speed_y)

    def __repr__(self):
        return f"<BallBounceOff>"


class Flash(IAnimation):
    """ Quick flash animation when ball bounces off a wall """

    COLOR_SPEED = 250

    def __init__(self, flash_color: Color, speed: int = COLOR_SPEED):
        print(f"Animation.Flash: color={flash_color}, speed={speed}")
        self.target = None
        self.speed = speed
        self.target_color = None
        self.flash_color = flash_color

    def update(self, dt):
        # We'll mutate the flash_color towards the direction of the desired target color
        self.flash_color.r = min(self.flash_color.r + int(self.speed * dt), 255)
        self.flash_color.g = min(self.flash_color.g + int(self.speed * dt), 255)
        self.flash_color.b = min(self.flash_color.b + int(self.speed * dt), 255)

        self.target.set_color(self.flash_color)

    def is_finished(self) -> bool:
        return self.flash_color.r == self.target_color.r and self.flash_color.g == self.target_color.g and self.flash_color.b == self.target_color.b

    def set_target(self, target: IMovable):
        self.target = target
        self.target_color = target.get_color()
        self.target.set_color(self.flash_color)
        print(f"Animation.Flash: got target={target}, target_color={self.target_color})")

    def __repr__(self):
        return f"<Flash color={self.target_color}>"
