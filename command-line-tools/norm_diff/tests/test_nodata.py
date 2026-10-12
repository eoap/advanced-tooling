"""Explicit unit fixtures; real EO acceptance is run separately on Kubernetes."""

from pathlib import Path

import numpy as np
import rasterio
from click.testing import CliRunner
from rasterio.transform import from_origin

from eoap_advanced_norm_diff.main import normalized_difference


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


def test_normalized_difference_keeps_valid_zero_and_masks_source_nodata(tmp_path):
    green = np.full((16, 16), 2, dtype=np.uint16)
    nir = np.full((16, 16), 1, dtype=np.uint16)
    green[0, 0] = nir[0, 0] = 0
    green[0, 1] = nir[0, 1] = 1
    a = tmp_path / "green.tif"
    b = tmp_path / "nir.tif"
    write_raster(a, green, 0)
    write_raster(b, nir, 0)
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(normalized_difference, [str(a), str(b)])
        assert result.exit_code == 0, result.exception
        with rasterio.open("norm_diff.tif") as raster:
            pixels = raster.read(1, masked=True)
            assert pixels.mask[0, 0]
            assert not pixels.mask[0, 1] and pixels[0, 1] == 0
            np.testing.assert_allclose(pixels[1:, :], np.float32(1 / 3))
