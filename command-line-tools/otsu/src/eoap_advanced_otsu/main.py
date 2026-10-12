"""Command line tool to apply the Otsu threshold to a raster"""

import click
import numpy as np
import rasterio
from loguru import logger
from numpy.typing import NDArray
from skimage.filters import threshold_otsu


def threshold(data: NDArray[np.float32]) -> NDArray[np.bool_]:
    """Returns the Otsu threshold of a numpy array"""
    finite = data[np.isfinite(data)]
    if not finite.size:
        raise ValueError("Otsu threshold requires finite pixels")
    return np.asarray(data > threshold_otsu(finite), dtype=np.bool_)


@click.command(
    short_help="Otsu threshoold",
    help="Applies the Otsu threshold",
)
@click.argument("raster", nargs=1)
def otsu(raster: str) -> None:
    """Applies the Otsu threshold"""

    with rasterio.open(raster) as ds:
        array = np.asarray(ds.read(1), dtype=np.float32)
        out_meta = ds.meta.copy()

    out_meta.update(
        {
            "dtype": "uint8",
            "nodata": None,
            "driver": "COG",
            "tiled": True,
            "compress": "lzw",
            "blockxsize": 256,
            "blockysize": 256,
        }
    )

    logger.info(f"Applying the Otsu threshold to {raster}")

    with rasterio.open("otsu.tif", "w", **out_meta) as dst_dataset:
        logger.info("Write otsu.tif")
        dst_dataset.write(threshold(array), indexes=1)

    logger.info("Done!")


if __name__ == "__main__":
    otsu()
