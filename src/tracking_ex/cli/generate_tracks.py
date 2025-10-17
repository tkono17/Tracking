#!/usr/bin/env python3
import typer
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
import random
from ..model import Frame, FrameHelper, Line2D

app = typer.Typer()

nrows, ncols = 200, 200
frame = Frame(p1=(0.0, -0.5), p2=(1.0, 0.5), width=ncols, height=nrows)

def genTrack():
    ptmin = 0.1
    ptmax = 1.0E+6
    thetamin = -0.5
    thetamax = 0.5
    theta = random.uniform(thetamin, thetamax)
    y0 = random.uniform(-0.2, 0.2)
    #
    track = Line2D(np.array([0.0, y0]), theta)
    return track

@app.command('single')
def generate_single_track(theta: Optional[float] = None,
                          y0: Optional[float] = None, 
                          figname: str = 'image'):
    random.seed()

    frameHelper = FrameHelper(frame)
    frameHelper.createImage()
    detectorMask = frameHelper.image.copy()

    x0 = int(ncols/10)
    dx = int(ncols/50)
    dx = 10
    #x0, dx, xstep = 20, 10, 20
    x0, dx, xstep = 20, 1, 5 # old
    #x0, dx, xstep = 20, 1, 20 # current
    x0, dx, xstep = 20, 1, 20 # new1
    #x0, dx, xstep = 20, 3, 40 # new2
    for x in range(x0, ncols, xstep):
        detectorMask[0:ncols,x:x+dx] = 1

    for i in range(10):
        track = genTrack()
        frameHelper.overlayLine(track)
    image0 = frameHelper.image
    image1 = image0*detectorMask

    plt.imshow(image0*200, cmap='GnBu')
    plt.savefig(f'{figname}_gen.jpg')
    
    plt.imshow(image1*200, cmap='GnBu')
    plt.savefig(f'{figname}_rec.jpg')

    plt.clf()
    plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    ax.imshow(image0)
    ax = fig.add_subplot(1, 2, 2)
    ax.imshow(image1)
    
    plt.show()


def main():
    app()
    
if __name__ == '__main__':
    main()
    
