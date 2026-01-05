from dataclasses import dataclass
import numpy as np

@dataclass
class Line2D:
    position: np.array
    theta: float

@dataclass
class Arc:
    origin: np.array
    theta: float
    radius: float
    
