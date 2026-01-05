#!/usr/bin/env python3
import typer
from typing import Optional
import matplotlib.pyplot as plt
import math
import numpy as np
import logging
import random

from ..model import Frame, FrameHelper, Line2D, Arc

log = logging.getLogger(__name__)

app = typer.Typer()

nrows, ncols = 200, 200
frame = Frame(p1=(0.0, -0.5), p2=(1.0, 0.5), width=ncols, height=nrows)


def genTrack():
    ptmin = 0.1
    ptmax = 1.0e6
    thetamin = -0.5
    thetamax = 0.5
    theta = random.uniform(thetamin, thetamax)
    y0 = random.uniform(-0.2, 0.2)
    #
    track = Line2D(np.array([0.0, y0]), theta)
    return track

def makeDetectorMask(frame, x0, dx, xstep):
    ncols = frame.shape[1]
    for x in range(x0, ncols, xstep):
        frame[0:ncols, x : x + dx] = 1
    return frame

@app.command("single")
def generate_single_track(
    theta: Optional[float] = None, y0: Optional[float] = None, figname: str = "image"
):
    frameHelper = FrameHelper(frame)
    frameHelper.createImage()
    detectorMask = frameHelper.image.copy()

    x0 = int(ncols / 10)
    dx = int(ncols / 50)
    dx = 10
    # x0, dx, xstep = 20, 10, 20
    x0, dx, xstep = 20, 1, 5  # old
    # x0, dx, xstep = 20, 1, 20 # current
    x0, dx, xstep = 20, 1, 20  # new1
    # x0, dx, xstep = 20, 3, 40 # new2
    detectorMask = makeDetectorMask(detectorMask, x0, dx, xstep)

    for i in range(10):
        track = genTrack()
        frameHelper.overlayLine(track)
    image0 = frameHelper.image
    image1 = image0 * detectorMask

    plt.imshow(image0 * 200, cmap="GnBu")
    plt.savefig(f"{figname}_gen.jpg")

    plt.imshow(image1 * 200, cmap="GnBu")
    plt.savefig(f"{figname}_rec.jpg")

    plt.clf()
    plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    ax.imshow(image0)
    ax = fig.add_subplot(1, 2, 2)
    ax.imshow(image1)

    plt.show()


def genTrackInB(B: float = 2.0):
    ptmin, ptmax = 0.05, 1.0E+3
    y0min, y0max = -0.1, 0.1
    thetamin, thetamax = -0.5, 0.5

    pt = random.uniform(math.log(ptmin), math.log(ptmax))
    pt = math.exp(pt)
    y0 = random.uniform(y0min, y0max)
    theta = random.uniform(thetamin, thetamax)
    charge = random.choice([1.0, -1.0])
    
    r = pt*charge/(0.3*B)
    track = Arc(np.array([0.0, y0]), theta, r)
    return track

@app.command("tracks_in_B")
def generate_tracks_in_B(ntracks: int=1, B: float=2.0, figname: str='tracksInB'):
    log.info("Generate multiple tracks in B-field")
    frameHelper = FrameHelper(frame)
    frameHelper.createImage()
    detectorMask = frameHelper.image.copy()

    x0 = int(ncols / 10)
    dx = int(ncols / 50)
    dx = 10
    x0, dx, xstep = 20, 1, 20  # new1
    detectorMask = makeDetectorMask(detectorMask, x0, dx, xstep)

    deg = 180.0/math.pi
    for i in range(ntracks):
        track = genTrackInB(B)
        log.info(f'Track pt={0.3*track.radius:3.1f} [GeV], y0={track.origin[1]:4.2f} [m], theta={track.theta*deg:3.2f} [deg]')
        frameHelper.overlayArc(track)

    image0 = frameHelper.image
    image1 = image0 * detectorMask

    plt.imshow(image0 * 200, cmap="GnBu")
    plt.savefig(f"{figname}_gen.jpg")

    plt.imshow(image1 * 200, cmap="GnBu")
    plt.savefig(f"{figname}_rec.jpg")

    plt.clf()
    plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    ax.imshow(image0)
    ax = fig.add_subplot(1, 2, 2)
    ax.imshow(image1)

    plt.show()


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(name)-20s %(levelname)-8s %(message)s"
    )
    random.seed()
    app()


if __name__ == "__main__":
    main()
