"""Creates a STAC catalog with the detected water bodies""" ""
import os
import shutil
import click
import pystac
import rio_stac
from loguru import logger
from stac_geoparquet.arrow import parse_stac_items_to_arrow, to_parquet
from pystac import read_file
from pyarrow.parquet import read_table

@click.command(
    short_help="Creates a STAC catalog",
    help="Creates a STAC catalog with the water bodies",
)
@click.option(
    "--input-item",
    "item_urls",
    help="STAC Item URL",
    required=True,
    multiple=True,
)
@click.option(
    "--water-body",
    "water_bodies",
    help="Water body geotiff",
    required=True,
    multiple=True,
)
def to_stac(item_urls, water_bodies):
    """Creates a STAC catalog with the detected water bodies"""

    logger.info(f"Creating a geoparquet file for {' '.join(water_bodies)}")
    cat = pystac.Catalog(id="catalog", description="water-bodies")

    items_iterable = []

    for index, item_url in enumerate(item_urls):
        if os.path.isdir(item_url):
            catalog = pystac.read_file(os.path.join(item_url, "catalog.json"))
            item = next(catalog.get_items())
        else:
            item = pystac.read_file(item_url)

        logger.info(f"Adding {item.id}")
        items_iterable.append(item)

    record_batch_reader = parse_stac_items_to_arrow(items_iterable)

    table = record_batch_reader.read_all()

    to_parquet(table, "water-bodies.parquet")

    logger.info("Done!")


if __name__ == "__main__":
    to_stac()
