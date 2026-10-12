"""Explicit unit fixtures; real EO acceptance is run separately on Kubernetes."""

from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pystac
import rasterio
from click.testing import CliRunner
from rasterio.transform import from_origin

from eoap_advanced_stac.main import to_stac


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


def test_catalog_uses_actual_mask_and_original_acquisition(tmp_path):
    item = pystac.Item("fixture", None, None, datetime(2021, 1, 1, tzinfo=UTC), {})
    source = tmp_path / "item.json"
    item.save_object(dest_href=str(source))
    mask = tmp_path / "mask.tif"
    write_raster(mask, np.zeros((16, 16), dtype=np.uint8))
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(to_stac, ["--input-item", str(source), "--water-body", str(mask)])
        assert result.exit_code == 0, result.exception
        output = next(pystac.Catalog.from_file("catalog.json").get_all_items())
        output.make_asset_hrefs_absolute()
        assert output.datetime == item.datetime
        with rasterio.open(output.assets["data"].href) as raster:
            assert raster.crs.to_epsg() == 4326
            assert raster.shape == (16, 16)
