# Poing

Minimalistic OpenGL "Pong" game

### Usage

Install necessary packages via your OS package manager or (preferred) prepare a virtual environment:

```buildoutcfg
export PROJECT_DIR=./Poing
mkdir -p $PROJECT_DIR && CD $PROJECT_DIR
virtualenv -p python3 venv
pip install -r requirements.txt
```

Then just run the game:

```
./poing.py
```

Once running, you can control the game with the following keys:

```buildoutcfg
Q - move Pad upwards
A - move Pad downwards
Spacebar: pause
R - restart game after losing
```

### TODOs and issues
- implement proper (non immediate mode) OpenGL
- handle different perceived game speed between GLUT and GLFW+VSync (same frame rate buf fewer game updates occuring?)
- in GLUT mode, the ball appears BEHIND the hud while in GLFW mode, it's in front

### Readme
- https://github.com/jcteng/python-opengl-tutorial
- https://www.glfw.org/docs/3.3
