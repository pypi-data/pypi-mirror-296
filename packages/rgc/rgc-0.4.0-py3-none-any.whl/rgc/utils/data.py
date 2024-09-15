"""
A collection of utility functions for data manipulation.

This module contains a collection of utility functions for astronomical data
manipulation.
"""

__author__ = "Mir Sazzat Hossain"


from pathlib import Path
from typing import cast

import pandas as pd
from astroquery.skyview import SkyView
from astroquery.vizier import Vizier


def catalog_quest(name: str, service: str = "Vizier") -> pd.DataFrame:
    """
    Fetch a catalog from a given astronomical service e.g. VizieR, Simbad.

    :param name: The name of the catalog to be fetched.
    :type name: str

    :param service: The name of the astronomical service to be used.
    :type service: str

    :return: A pandas DataFrame containing the fetched catalog.
    :rtype: pd.DataFrame
    """
    if service == "Vizier":
        Vizier.ROW_LIMIT = -1
        catalog = Vizier.get_catalogs(name)
        return cast(pd.DataFrame, catalog[0].to_pandas())
    else:
        raise _UnsupportedServiceError()


class _UnsupportedServiceError(Exception):
    """
    An exception to be raised when an unsupported service is provided.
    """

    def __init__(self) -> None:
        super().__init__("Unsupported service provided. Only 'Vizier' is supported.")


def celestial_capture(survey: str, ra: float, dec: float, filename: str) -> None:
    """
    Capture a celestial image using the SkyView service.

    :param survey: The name of the survey to be used e.g. 'VLA FIRST (1.4 GHz)'.
    :type survey: str

    :param ra: The right ascension of the celestial object.
    :type ra: float

    :param dec: The declination of the celestial object.
    :type dec: float

    :param filename: The name of the file to save the image.
    :type filename: str
    """
    image = SkyView.get_images(position=f"{ra}, {dec}", survey=survey, coordinates="J2000", pixels=(150, 150))[0]

    comment = str(image[0].header["COMMENT"])
    comment = comment.replace("\n", " ")
    comment = comment.replace("\t", " ")

    image[0].header.remove("comment", comment, True)
    image[0].header.add_comment(comment)

    folder_path = Path(filename).parent
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    image.writeto(filename, overwrite=True)


def celestial_tag(entry: pd.Series) -> str:
    """
    Generate a name tag for a celestial object based on its coordinates.

    :param entry: A pandas Series entry of the catalog.
    :type entry: pd.Series

    :return: A string containing the name tag.
    :rtype: str
    """

    def format_dec(dec: str) -> str:
        sign = "+" if float(dec.replace(" ", "")) > 0 else ""
        return f"{sign}{dec}"

    if {"RAJ2000", "DEJ2000"}.issubset(entry.index):
        ra, dec = entry["RAJ2000"], entry["DEJ2000"]
    elif {"RA", "DEC"}.issubset(entry.index):
        ra, dec = entry["RA"], entry["DEC"]
    elif "filename" in entry.index:
        return f"{entry['filename']}"
    elif "FCG" in entry.index:
        return f"{entry['FCG']}"
    else:
        raise _NoValidCelestialCoordinatesError()

    return f"{ra}{format_dec(dec)}"


class _NoValidCelestialCoordinatesError(Exception):
    """
    An exception to be raised when no valid celestial coordinates are found in the entry.
    """

    def __init__(self) -> None:
        super().__init__("No valid celestial coordinates found in the entry to generate a tag.")
