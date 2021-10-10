from interfaces import IScene


class TestScene(IScene):
    def __init__(self, keyboard_manager):
        self.width = None
        self.height = None
        self.keyboard = keyboard_manager
        self.fullscreen_callback = None

    def pause(self):
        pass

    def unpause(self):
        pass

    def set_display_dimensions(self, width: int, height: int):
        print(f"{self}: received display dimensions {width}x{height}")
        self.width = width
        self.height = height

    def update(self, dt):
        pass

    def reshape(self, width: int, height: int):
        print(f"{self}: received new resolution {width}x{height}")
        self.width = width
        self.height = height

    def __repr__(self):
        return "<scenes.TestScene>"
