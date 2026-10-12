"""Creates a STAC catalog with the detected water bodies""" ""

import os
import shutil

import click
import pystac
import rio_stac
from loguru import logger


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

    logger.info(f"Creating a STAC Catalog for {' '.join(water_bodies)}")
    cat = pystac.Catalog(id="catalog", description="water-bodies")

    for index, item_url in enumerate(item_urls):
        item = read_item(item_url)

        water_body = water_bodies[index]

        os.makedirs(item.id, exist_ok=True)
        shutil.copy(water_body, item.id)

        out_item = rio_stac.stac.create_stac_item(
            source=water_body,
            input_datetime=item.datetime,
            id=item.id,
            asset_roles=["data", "visual"],
            asset_href=os.path.basename(water_body),
            asset_name="data",
            with_proj=True,
            with_raster=True,
        )

        cat.add_items([out_item])

    cat.normalize_and_save(root_href="./", catalog_type=pystac.CatalogType.SELF_CONTAINED)
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
