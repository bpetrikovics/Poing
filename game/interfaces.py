from abc import ABC, abstractmethod

from color import Color


class IColorable(ABC):
    @abstractmethod
    def set_color(self, color: Color):
        pass

    @abstractmethod
    def get_color(self):
        pass


class IMovable(ABC):
    @abstractmethod
    def move_to(self, dest_x: int, dest_y: int):
        pass

    @abstractmethod
    def move_by(self, dx: int, dy: int):
        pass

    @abstractmethod
    def set_speed(self, speed_x: int, speed_y: int):
        pass

    @abstractmethod
    def get_speed(self):
        pass

    @abstractmethod
    def get_coords(self):
        pass

    @abstractmethod
    def move(self):
        pass


class IAnimation(ABC):
    @abstractmethod
    def update(self, dt: int):
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        pass

    @abstractmethod
    def set_target(self, target: IMovable):
        pass


class IScene(ABC):
    @abstractmethod
    def __init__(self, keyboard_manager):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def unpause(self):
        pass

    @abstractmethod
    def set_display_dimensions(self, width: int, height: int):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def reshape(self, width: int, height: int):
        pass

    def set_fullscreen_callback(self, callback):
        self.fullscreen_callback = callback
