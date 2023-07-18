import geopy.geocoders
import pyproj
import time
import math
import random

def get_coordinates_of_address(address, crs):
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

    time.sleep(1.5)

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
    # Convert d from meters to degrees
    r_deg = r / 111320.0

    # Calculate the offsets in x' and y' direction
    dx = r_deg * math.cos(a)
    dy = r_deg * math.sin(a)

    # Apply the offsets to the input coordinates
    x_prime = x + dx
    y_prime = y + dy

    return x_prime, y_prime