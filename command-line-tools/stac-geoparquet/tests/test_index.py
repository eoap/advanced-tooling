"""Index the supplied acquisition metadata; this legacy tool does not publish masks."""

from datetime import UTC, datetime

import pystac
from click.testing import CliRunner
from pyarrow.parquet import read_table

from eoap_advanced_stac_geoparquet.main import to_stac


def test_index_preserves_input_acquisition_metadata(tmp_path):
    item = pystac.Item(
        "fixture",
        {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
        [0, 0, 1, 1],
        datetime(2021, 1, 1, tzinfo=UTC),
        {},
    )
    item.add_asset("green", pystac.Asset("https://example.com/fixture-green.tif", roles=["data"]))
    path = tmp_path / "item.json"
    item.save_object(dest_href=str(path))
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(
            to_stac, ["--input-item", str(path), "--water-body", "legacy-unused-mask.tif"]
        )
        assert result.exit_code == 0, result.exception
        table = read_table("water-bodies.parquet")
        assert table.num_rows == 1
        assert table.column("id").to_pylist() == ["fixture"]
