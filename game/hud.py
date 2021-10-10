import OpenGL.GL as gl
import numpy
from PIL import Image, ImageDraw, ImageFont


class Hud:
    def __init__(self):
        print("Hud: init")
        self.data = dict()
        self.window_width = None
        self.window_height = None
        self.img_data = None
        self.textureID = None
        self.font = ImageFont.truetype("FiraSans-Bold.ttf", 25)

    def reshape(self, width: int, height: int):
        print(f"Hud: received window dimensions {width}x{height}")
        self.window_width = width
        self.window_height = height

    def update(self, data: dict):
        self.data = data
        img = Image.new('RGBA', (300, 100), color=(15, 15, 15))
        d = ImageDraw.Draw(img)
        text = self.data.get('text', None)
        d.text((10, 10), text, fill=(55, 85, 255), font=self.font)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        self.img_data = numpy.array(list(img.getdata()), numpy.int8)

        self.textureID = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT);
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT);
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR);
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR);

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, img.size[0], img.size[1], 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
                        self.img_data)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def draw(self):
        if not self.textureID:
            return

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        gl.glTexEnvi(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_REPLACE)

        gl.glBegin(gl.GL_QUADS)

        gl.glTexCoord2f(0, 1)
        gl.glVertex2f(self.window_width - 300, 25)

        gl.glTexCoord2f(1, 1)
        gl.glVertex2f(self.window_width - 25, 25)

        gl.glTexCoord2f(1, 0)
        gl.glVertex2f(self.window_width - 25, 125)

        gl.glTexCoord2f(0, 0)
        gl.glVertex2f(self.window_width - 300, 125)

        gl.glEnd()

        gl.glDisable(gl.GL_TEXTURE_2D)
