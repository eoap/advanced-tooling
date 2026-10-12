"""Normalized difference"""

import click
import numpy as np
import rasterio
from loguru import logger

np.seterr(divide="ignore", invalid="ignore")


@click.command(
    short_help="Normalized difference",
    help="Performs a normalized difference",
)
@click.argument("rasters", nargs=2)
def normalized_difference(rasters: tuple[str, str]) -> None:
    """Performs a normalized difference"""

    logger.info(f"Processing the normalized image with {rasters[0]} and {rasters[1]}")

    with rasterio.open(rasters[0]) as ds1:
        array1 = ds1.read(1, masked=True).astype(np.float32).filled(np.nan)
        out_meta = ds1.meta.copy()

    with rasterio.open(rasters[1]) as ds2:
        array2 = ds2.read(1, masked=True).astype(np.float32).filled(np.nan)

    out_meta.update(
        {
            "dtype": "float32",
            "nodata": np.nan,
            "driver": "COG",
            "tiled": True,
            "compress": "lzw",
            "blockxsize": 256,
            "blockysize": 256,
        }
    )

    with rasterio.open("norm_diff.tif", "w", **out_meta) as dst_dataset:
        logger.info("Write norm_diff.tif")
        dst_dataset.write((array1 - array2) / (array1 + array2), 1)

    logger.info("Done!")


if __name__ == "__main__":
    normalized_difference()
