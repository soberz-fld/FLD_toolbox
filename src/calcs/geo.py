import geopy.geocoders
import pyproj
import time
import math
import os
from ..connectors import sqlite_connector

_cache_path = os.path.expandvars(r'%appdata%\FLD-VT\fld_toolbox\cache.db')
os.makedirs(os.path.dirname(_cache_path), exist_ok=True)
_sql_creator = 'CREATE TABLE coord_of_addr (addr VARCHAR(100) PRIMARY KEY, x FLOAT, y FLOAT);'
_db: sqlite_connector.SqliteConnector  # Must be initialized in same thread

def get_coordinates_of_address(address, crs):

    _db = sqlite_connector.SqliteConnector(_cache_path, create_new_if_not_existing=True, sql_script_if_creating_new=_sql_creator)
    cached = _db.exe_sql('SELECT x, y FROM coord_of_addr WHERE addr = "' + address + '";')

    if cached:

        return cached[0]

    else:

        # Geocoder-Objekt erstellen
        geolocator = geopy.geocoders.Nominatim(user_agent="my_geocoder")

        # Adresse in Koordinaten umwandeln
        location = geolocator.geocode(address)

        # CRS-Objekte erstellen
        crs_source = pyproj.CRS.from_epsg(4326)  # CRS 4326 (WGS84) für Längen- und Breitengrad
        crs_target = pyproj.CRS.from_epsg(crs)  # CRS 25832 (ETRS89 / UTM Zone 32N) für Koordinaten in Deutschland

        # Transformer-Objekt erstellen
        transformer = pyproj.Transformer.from_crs(crs_source, crs_target, always_xy=True)

        # Koordinaten umwandeln
        x, y = transformer.transform(location.longitude, location.latitude)

        # Time between requests!
        time.sleep(1.5)

        # Write to cache
        _db.exe_sql('INSERT INTO coord_of_addr VALUES (?,?,?);', (address, x, y))

        return x, y

def get_25832_coordinates_of_address(address):
    return get_coordinates_of_address(address, 25832)

def get_4647_coordinates_of_address(address):
    return get_coordinates_of_address(address, 4647)

def convert_from_25832_to_gps(x,y):
    crs = pyproj.CRS.from_epsg(25832)
    wgs84 = pyproj.CRS.from_epsg(4326)

    transformer = pyproj.Transformer.from_crs(crs, wgs84, always_xy=True)
    lon, lat = transformer.transform(x, y)

    return lat, lon

def offset_25832_coordinates(x, y, r, a = 1.5 * math.pi):
    # Calculate the offsets in x' and y' direction
    dx = r * math.cos(a)
    dy = r * math.sin(a)

    # Apply the offsets to the input coordinates
    x_prime = x + dx
    y_prime = y + dy

    return x_prime, y_prime