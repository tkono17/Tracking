#!/usr/bin/env python3
import typer
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
import random
from ..model import Frame, FrameHelper, Line2D

app = typer.Typer()

frame = Frame(p1=(0.0, -0.5), p2=(1.0, 0.5), width=100, height=100)

@app.command('single')
def generate_single_track(theta: Optional[float] = None,
                          y0: Optional[float] = None, 
                          figname: str = 'image'):
    ptmin = 0.1
    ptmax = 1.0E+6
    thetamin = -0.5
    thetamax = -0.5
    if theta is None:
        theta = random.uniform(thetamin, thetamax)
    if y0 is None:
        y0 = random.uniform(-0.2, 0.2)
    #
    track = Line2D(np.array([0.0, y0]), theta)

    print(f'Frame = {frame}')
    print(f'track = {track}')
    
    frameHelper = FrameHelper(frame)
    frameHelper.createImage()
    detectorMask = frameHelper.image.copy()

    for x in range(10, 100, 10):
        detectorMask[0:100,x:x+2] = 1.0
    
    frameHelper.overlayLine(track)
    image0 = frameHelper.image
    image1 = image0*detectorMask

    plt.imshow(image0)
    plt.savefig(f'{figname}_gen.jpg')
    
    plt.imshow(image1)
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
    
