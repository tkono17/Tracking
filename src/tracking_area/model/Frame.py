from dataclasses import dataclass
import math

@dataclass
class Frame:
    p1: numpy.ndarray
    p2: numpy.ndarray
    width: int
    height: int

    def __post_init__(self):

class FrameHelper:
    def __init__(self, frame):
        self.frame = frame
        #
        x1, y1 = self.frame.p1[0], self.frame.p1[1]
        x2, y2 = self.frame.p2[0], self.frame.p2[1]
        self.pixelX = x2 - x1
        self.pixelY = y2 - y1

    def toX(self, c):
        return self.frame.p1[0] + self.pixelX*(c+0.5)

    def toY(self, r):
        return self.frame.p2[1] - self.pixel1*(r+0.5)

    def toXY(self, cr):
        c, r = cr[0], cr[1]
        return np.array( [self.toX(c), self.toY(r)] )

    def column(self, x):
        c = int( (x - self.frame.p1[0])/self.pixelX)
        if c < 0:
            c = 0
        elif c >= self.frame.width:
            c = self.frame.width - 1
        return c
    
    def row(self, y):
        r = int( (y - self.frame.p1[1])/self.pixelY)
        r = self.frame.height - r
        if r < 0:
            r = 0
        elif r >= self.frame.height:
            r = self.frame.height - 1
        return r

    def cr(self, xy):
        x, y = self.column(xy[0]), self.row(xy[1])
        return np.array([x, y])

    def drawLine(self, line, image):
        if abs(line.theta)<1.0:
            p1 = line.position
            x2 = self.frame.p2[0]
            p2 = np.array([x2, x2*math.tan(line.theta)])
        else:
            p1 = line.position
            y2 = self.frame.p2[1]
            p2 = np.array([x2, y2*math.tan(line.theta)])
            
