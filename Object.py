##############################################################################
#                           Object.py
#            Represents the object drawn in the 3D world
##############################################################################
from visual import *
import numpy as np
from scipy.signal import savgol_filter


class Object:
    def __init__(self, pic, scene, shape):
        if shape == 'square':
            self.points = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        elif shape == 'triangle':
            self.points = [(-1, -1), (0, 1), (1, -1)]
        elif shape == 'custom1':
            self.points = [(-1, 1), (1, 1), (0, 0), (1, -1), (-1, -1)]
        elif shape == 'custom2':
            self.points = [(0, 0), (1, 1), (1, 0)]
        else:
            self.points = None
        self.scene = scene
        # x = pic.closestEdge(x)
        self.pic = pic
        # self.pic.cut()
        x = self.pic.topleft()
        limit = pic.size
        self.x = x
        pt = self.pic.findp2(x)
        self.e = curve(pos=[self.x, pt], color=color.blue, radius=2)
        self.limit = limit

        self.p2(pt)
        self.getDown()

    def p2(self, pt):
        m = int(self.limit / 2)
        pt = (max(-m, min(m, pt[0])), max(-m, min(m, pt[1])))
        # self.epos = [self.x, pt]
        self.y = pt
        self.center = ((self.x[0] + self.y[0]) / 2,
                       (self.x[1] + self.y[1]) / 2,
                       0)
        self.w = abs((self.x[0] - self.y[0]))
        self.h = 2 * abs(pt[1] - self.x[1])

    def getDown(self):
        p4 = self.pic.findAlongY(self.center)
        self.p4(p4)
        self.render3D(self.scene)

    def p3(self, pt):
        self.z = pt
        w = abs((self.x[0] - self.y[0]))
        h = 2 * abs(pt[1] - self.x[1])
        self.center = ((self.x[0] + self.y[0]) / 2,
                       (self.x[1] + self.y[1]) / 2,
                       0)
        # points = [(p[0] * w, p[1] * h) for p in self.points]
        self.e.shape = shapes.ellipse(width=w, height=h)
        self.e.pos = self.center
        self.w = w
        self.h = h

    def p4(self, pt, place=false):
        p = (pt[0], pt[1], 0)
        if not hasattr(self, 'section'):
            self.zpos = [self.center, self.center]
            self.section = curve(pos=[self.center, self.center])
        # The last parameter of the curve is to be changed
        self.zpos[len(self.zpos) - 1] = p

        if place:
            self.zpos.append(p)
        self.section.pos = self.zpos
        self.displaySides()

    # @throttle(seconds=0.05)
    def displaySides(self):
        # We move self.x and self.y along angle between self.center and
        # self.zpos
        if not hasattr(self, 'p'):
            self.p = (self.x[0], self.x[1], 0)
            self.q = (self.y[0], self.y[1], 0)
            self.xSection = curve(pos=[self.p, self.p], color=color.red)
            self.ySection = curve(pos=[self.q, self.q], color=color.red)
        self.xzpos = [self.p, self.p]
        self.yzpos = [self.q, self.q]
        c = ((self.p[0] + self.q[0]) / 2,
             (self.p[1] + self.q[1]) / 2,
             0)
        l = self.zpos[len(self.zpos) - 1]
        # Get angle between p, c, len(zpos)
        # a = self.angle(c, l, self.p)
        # Move p & q along angle a. Find points that coincide in a vicinity
        # Give weights to matching. But the user may want something that may be
        # occluded so we go along the weight ratio
        # TODO: Ideally this should be smart Livewire via running something
        # like dijkstra's algo.
        p = self.p
        q = self.q
        for i in range(int(c[1]), int(l[1]), -1):
            p = (p[0], p[1] - 1)
            q = (q[0], q[1] - 1)
            p = self.pic.closestLeft(p)
            q = self.pic.closestRight(q)
            self.xzpos[len(self.xzpos) - 1] = p
            self.xzpos.append(p)
            self.yzpos[len(self.yzpos) - 1] = q
            self.yzpos.append(q)
        self.xzpos = [x for x in self.xzpos if x is not None]
        self.yzpos = [x for x in self.yzpos if x is not None]
        self.xSection.pos = self.xzpos
        self.ySection.pos = self.yzpos

    def angle(self, x, y, z):
        d_xy = self.distance(x, y)
        d_xz = self.distance(x, z)
        d_yz = self.distance(y, z)
        return math.acos((d_xy * d_xy + d_xz * d_xz - d_yz * d_yz) /
                         (2 * d_xy * d_xz))

    def distance(self, x, y):
        dx = (x[0] - y[0])
        dy = (x[1] - y[1])
        return math.sqrt(dx * dx + dy * dy)

    def render3D(self, scene):
        self.section.visible = false
        self.xSection.visible = false
        self.ySection.visible = false
        self.scene = scene
        # Lets create a shape.
        # TODO: Get the correct camera position
        self.e.visible = false
        radius = self.w / 2.0
        r = range(0, min(len(self.yzpos), len(self.xzpos)) - 1)
        p = np.array([(self.xzpos[i][0] + self.yzpos[i][0]) / 2.0
                      for i in r])
        p = savgol_filter(p, 51, 3)
        epos = [(p[i], self.xzpos[i][1], 0)
                for i in range(0, len(self.xzpos) - 1)]
        a = np.array([float(self.yzpos[i][0] - self.xzpos[i][0]) / self.w
                      for i in r])
        # a = savgol_filter(a, 51, 3)
        scale = [(a[i], a[i]) for i in r]
        if self.points is None:
            shape = shapes.circle(radius=radius)
        else:
            points = [(pt[0] * self.w, pt[1] * self.w) for pt in self.points]
            shape = Polygon(points)

        self.model = extrusion(shape=shape,
                               frame=frame(), pos=epos, scale=scale)
        self.addTexture(max(a) * radius)

    def addTexture(self, z):
        texture = self.pic.extract(self.xzpos, self.yzpos)
        tex = materials.texture(data=texture,
                                mapping="spherical")
        self.model.frame.pos = (0, 0, -z)
        self.model.material = tex
