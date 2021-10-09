from abc import abstractmethod
import OpenGL.GL as gl

from color import Color
from interfaces import IColorable, IMovable, IAnimation


class Entity:
    """ Simple entity that knows its position only """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<Entity x={self.x}, y={self.y}>"


class MovableMixin(IMovable):
    """ Mixin that provides the ability to move to a position or by given dx/dy amount """
    def move_to(self, dest_x: int, dest_y: int):
        self.x = dest_x
        self.y = dest_y

    def move_by(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def get_speed(self):
        return self.speed_x, self.speed_y

    def set_speed(self, speed_x: int, speed_y: int):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def get_coords(self):
        return self.x, self.y

    def set_coords(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y


class DrawableMixin:
    """ Mixin that provides the ability for the entity to draw itself (abstract) """
    @abstractmethod
    def draw(self):
        pass


class ColorableMixin(IColorable):
    """ Mixin that provides the ability to have color """
    DEFAULT_COLOR = Color(255, 255, 255)

    def set_color(self, color: Color):
        self.color = color

    def get_color(self):
        return self.color


class AnimatedMixin:
    """ Mixin to provide the ability to have a number of animations applied to the object """
    def __init__(self):
        self.clear_animations()
        self.target = None

    def clear_animations(self):
        print(f"AnimatedMixin: Clearing all animations on {self}")
        self.animations = []

    def add_animation(self, animation: IAnimation):
        animation.set_target(self)
        self.animations.append(animation)

    def delete_animation(self, animation: IAnimation):
        if animation in self.animations:
            self.animations.remove(animation)

    def animate(self, dt: int):
        for anim in list(self.animations):
            anim.update(dt)
            if anim.is_finished():
                print(f"AnimatedMixin: {anim} is finished and being removed")
                self.delete_animation(anim)


class Rectangle(Entity, DrawableMixin, ColorableMixin):
    """ Simple drawable, colorable rectangle """
    def __init__(self, x: int, y: int, width: int, height: int, color=None):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.set_color(color if color is not None else ColorableMixin.DEFAULT_COLOR)

    def draw(self):
        gl.glBegin(gl.GL_QUADS)
        gl.glColor3ub(self.color.r, self.color.g, self.color.b)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

    def __repr__(self):
        return f"<Rectangle x={self.x}, y={self.y}>"


class Ball(Rectangle, MovableMixin, AnimatedMixin):
    """ Implementation of the ball in game """
    def __init__(self, *args):
        super().__init__(*args)
        AnimatedMixin.__init__(self)
        self.set_speed(0, 0)

    # When bouncing on the left/right edge, providing a possibility to
    # also adjust vertical speed e.g. when the pad was moving
    def bounce_x(self, adjust_x: int = 0):
        self.speed_x = -self.speed_x
        if adjust_x:
            print("Ball: Increasing vertical speed")
            self.speed_y += adjust_x

    def bounce_y(self):
        self.speed_y *= -1

    def update(self, dt: int):
        self.animate(dt)
        self.move()

    def increase_speed(self):
        self.speed_x += 1
        self.speed_y += 1

    def __repr__(self):
        return f"<Ball x={self.x}, y={self.y}>"


class Pad(Rectangle, MovableMixin, AnimatedMixin):
    """ Implementation of the pad in game """
    def __init__(self, *args):
        super().__init__(*args)
        AnimatedMixin.__init__(self)

    def update(self, dt: int):
        self.animate(dt)

    def __repr__(self):
        return f"<Pad x={self.x}, y={self.y}>"
