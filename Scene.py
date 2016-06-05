##############################################################################
#                           Scene.py
#            A wrapper over the VPython Scene to take care
#               of rendering the 3D scene on the screen
##############################################################################
from visual import *


class Scene:
    def drawImage(self):
        # We want the image to not obstruct the view. This is just background
        # aid. The user is doing extrusion in the real world
        # with restrictions based on the image frame to assist him/her
        # We draw at z = 0
        # TODO: Fix this. The formula is incorrect
        # Derive it mathemtically here.
        scale = 4
        newSize = int(self.pic.size * scale)
        im = self.pic.scaled(newSize)
        tex = materials.texture(data=im, mapping='rectangular')
        location = ((1 - scale) / 2.0) * self.position[2]

        self.background = box(pos=(0, 0, location), axis=(0, 0, 1),
                              length=0.1, height=newSize,
                              width=newSize, material=tex)

    def __init__(self, scene, pic, zoom=1):
        scene.material = materials.shiny
        self.pic = pic
        scene.title = 'Reconstruction Studio'
        scene.range = r = pic.size / 2  # This is measured from the center
        scene.width = pic.size * zoom
        scene.height = pic.size * zoom
        scene.autoscale = false
        scene.fov = radians(60)  # 60 Degree Camera FOV

        self.raw = scene
        # Lets find the position of the camera
        self.position = (0, 0, 2 * r / tan(scene.fov / 2))
        # box(pos=(0, 0, 20), axis=(0, 0, 1),
        #     length=0.1, height= r, width= r,
        #     material=materials.silver)
        # Opposite side of the camera at the same distance
        self.drawImage()
