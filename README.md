# Poing

Minimalistic OpenGL "Pong" game. Nothing fancy or special, it's mostly about me
learning how to write a very simple game while also learning the basics of OpenGL
(immediate mode, for now, yes). Maybe it helps someone else learn a bit or two
about basic OpenGL concepts.

It has both a GLUT and a GLFW display managers, and supports multiple game modes
aka. scenes.

### Usage

Install necessary packages via your OS package manager or (preferred) prepare a
virtual environment:

```
export PROJECT_DIR=./Poing
mkdir -p $PROJECT_DIR && CD $PROJECT_DIR
virtualenv -p python3 venv
pip install -r requirements.txt
```

Then just run the game (virtualenv will be auto-detected and used):

```
./poing.py
```

Once running, you can control the game with the following keys:

```
Q - move Pad upwards
A - move Pad downwards
Spacebar - pause
R - restart game after losing
```

### TODOs and issues
- Implement proper (non immediate mode) OpenGL
- Handle different perceived game speed between GLUT and GLFW+VSync (same frame rate but fewer game updates occurring - fix "tick" logic?)
- In GLUT mode, the ball appears BEHIND the hud while in GLFW mode, it's in front
- Colors!
- Textures
- Backdrop

### Stuff to read
- https://github.com/jcteng/python-opengl-tutorial
- https://www.glfw.org/docs/3.3
