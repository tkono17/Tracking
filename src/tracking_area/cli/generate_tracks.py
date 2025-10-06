#!/usr/bin/env python3
import typer
from ..model import Frame

app = typer.Typer()

frame = Frame(p1=(0.0, -0.5), p2=(1.0, 0.5), width=100, height=100)

@app.command('single')
def generate_single_track(theta=None, pt=1.0E+5):
    ptmin = 0.1
    ptmax = 1.0E+6
    thetamin = -0.5
    thetamax = -0.5
    if theta is None:
        theta = random.unifrom(thetamin, thetamax)
    else:
        if theta < thetamin:
            theta = thetamin
        elif theta > thetamax:
            theta = thetamax
    #B = 2.0
    #r = 1/(0.3*B*pt)
    return Line2D(np.array([0.0, 0.0]), theta)
    
def main():
    app()
    
if __name__ == '__main__':
    main()
    
