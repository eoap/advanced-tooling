import numpy as np
from numpy.typing import NDArray

# Public threshold API used with finite float32 raster values.
def threshold_otsu(image: NDArray[np.float32]) -> float: ...
