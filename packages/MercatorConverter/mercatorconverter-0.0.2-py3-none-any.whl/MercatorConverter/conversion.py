import math


def mercator_to_coord(lat, lon):
    """
    Converts a Mercator latitude and longitude given in decimal degrees to a geographical projection latitude and longitude
    :param lat:
    :param lon:
    :return:
    """
    r_major = 6378137.000
    x = r_major * math.radians(lon)
    scale = x / lon
    y = 180.0 / math.pi * math.log(math.tan(math.pi / 4.0 + lat * (math.pi / 180.0) / 2.0)) * scale
    return x, y


def coord_to_mercator(x, y):
    """
    Converts a geographical projection latitude and longitude given in decimal degrees to a Mercator latitude and longitude
    :param x:
    :param y:
    :return:
    """
    r_major = 6378137.000
    lon = math.degrees(x / r_major)
    scale = x / lon
    lat = (math.atan(math.exp(math.pi * y / (180 * scale))) - math.pi / 4) * 360 / math.pi
    return lat, lon
