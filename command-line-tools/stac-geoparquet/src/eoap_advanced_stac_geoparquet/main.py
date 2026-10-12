"""Creates a STAC catalog with the detected water bodies""" ""

import os

import click
import pystac
from loguru import logger
from stac_geoparquet.arrow import parse_stac_items_to_arrow, to_parquet


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
def to_stac(item_urls: tuple[str, ...], water_bodies: tuple[str, ...]) -> None:
    """Creates a STAC catalog with the detected water bodies"""

    logger.info(f"Creating a geoparquet file for {' '.join(water_bodies)}")

    items_iterable = []

    for item_url in item_urls:
        item = read_item(item_url)

        logger.info(f"Adding {item.id}")
        items_iterable.append(item)

    record_batch_reader = parse_stac_items_to_arrow(items_iterable)

    table = record_batch_reader.read_all()

    to_parquet(table, "water-bodies.parquet")

    logger.info("Done!")


def read_item(href: str) -> pystac.Item:
    source = os.path.join(href, "catalog.json") if os.path.isdir(href) else href
    document = pystac.read_file(source)
    if isinstance(document, pystac.Item):
        return document
    if isinstance(document, pystac.Catalog):
        item = next(document.get_all_items(), None)
        if item is not None:
            return item
    raise ValueError("Input must contain a STAC Item")


if __name__ == "__main__":
    to_stac()
