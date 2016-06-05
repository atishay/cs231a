from visual import *
from Pic import Pic
from Scene import Scene
from Object import Object
import sys


class Main:
    def keyInput(self, evt):
        s = evt.key
        c = scene.center
        if (s == 'up'):
            scene.center = (c[0], 1 + c[1], c[2])
        elif (s == 'down'):
            scene.center = (c[0], c[1] - 1, c[2])

    def __init__(self, im, shape, faces):
        self.pic = Pic(im, faces)
        scene.background = [1, 1, 1]
        self.scene = Scene(scene, self.pic)
        scene.bind('keydown', self.keyInput)
        Object(self.pic, self.scene, shape)
        self.scene.background.visible = false


def main():
    shape = None
    faces = 4
    if len(sys.argv) > 1:
        im = sys.argv[1]
        if len(sys.argv) > 2:
            shape = sys.argv[2]
            if len(sys.argv) > 3:
                try:
                    faces = int(sys.argv[3])
                except ValueError:
                    faces = 4
    else:
        im = 'coke.jpg'
    Main(im, shape, faces)


if __name__ == "__main__":
    main()
