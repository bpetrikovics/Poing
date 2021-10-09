from threading import Lock
from pynput import keyboard
from collections import deque


class KeyboardManager:

    def __init__(self):

        self._lock = Lock()
        self.keys_pressed = dict()
        self.queue = deque()

        print("Keyboard: start")
        self.listener = keyboard.Listener(
            on_press=self.on_press_handler,
            on_release=self.on_release_handler
        )

        self.listener.start()

    def on_press_handler(self, key):
        if key not in self.keys_pressed:
            with self._lock:
                self.keys_pressed[key] = True

    def on_release_handler(self, key):
        if key in self.keys_pressed:
            with self._lock:
                del(self.keys_pressed[key])
                self.queue.appendleft(key)

    def next(self):
        if len(self.queue):
            return self.queue.pop()
        else:
            return None

    def is_pressed(self, key):
        with self._lock:
            return self.keys_pressed.get(keyboard.KeyCode.from_char(key), False)

    def get_keys(self):
        with self._lock:
            return self.keys_pressed
