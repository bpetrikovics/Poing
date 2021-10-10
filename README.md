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

TODO:
- implement proper (non immediate mode) OpenGL
- switch from GLUT to GLFW

E.g.: https://github.com/jcteng/python-opengl-tutorial
 