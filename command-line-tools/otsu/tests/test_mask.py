"""Explicit unit fixtures; real EO acceptance is run separately on Kubernetes."""

from pathlib import Path

import numpy as np
import pytest
import rasterio
from click.testing import CliRunner
from rasterio.transform import from_origin

from eoap_advanced_otsu.main import otsu, threshold


def write_raster(path: Path, pixels, nodata=None):
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=pixels.shape[0],
        width=pixels.shape[1],
        count=1,
        dtype=pixels.dtype,
        crs="EPSG:4326",
        transform=from_origin(0, pixels.shape[0], 1, 1),
        nodata=nodata,
    ) as raster:
        raster.write(pixels, 1)


def test_binary_mask_keeps_zero_land_valid(tmp_path):
    pixels = np.ones((16, 16), dtype=np.float32)
    pixels[:8] = -1
    pixels[0, 0] = np.nan
    source = tmp_path / "ndwi.tif"
    write_raster(source, pixels, np.nan)
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(otsu, [str(source)])
        assert result.exit_code == 0, result.exception
        with rasterio.open("otsu.tif") as raster:
            assert raster.nodata is None
            assert set(np.unique(raster.read(1))) == {0, 1}
            assert raster.read_masks(1).min() == 255


def test_otsu_rejects_all_invalid_pixels():
    with pytest.raises(ValueError, match="finite"):
        threshold(np.full((2, 2), np.nan, dtype=np.float32))
