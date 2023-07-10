from django.conf import settings
from math import sin, cos, acos, asin, atan2, degrees, pi, sqrt
import requests
import json
#from geopy import distance


class GeoInterface:

    EARTH_RADIUS = 6356.7523
    NORTH_RAD = 0
    SOUTH_RAD = pi
    EAST_RAD = pi / 2
    WEST_RAD = 3 * pi / 2

    @classmethod
    def get_coordinators(cls, user_request) -> tuple:
        """ Получить координаты из запроса """
        ip = cls._get_ip(user_request)
        response = requests.get("".join((settings.GEO_API_URL, f"&ip_address={ip}")))
        #response = requests.get(settings.GEO_API_URL)
        content = json.loads(response.content)
        longitude = content.get('longitude')
        latitude = content.get('latitude')
        return longitude, latitude

    @classmethod
    def get_distance(cls, lon_1, lat_1, lon_2, lat_2):
        """ Получить дистанцию между 2мя точками"""
        d_lat = lat_2 - lat_1
        d_lon = lon_2 - lon_1
        distance = 2 * cls.EARTH_RADIUS * asin(sqrt(
            sin(d_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(d_lon / 2) ** 2))

        distance = round(distance/1000, 1)
        return distance

    @classmethod
    def calculate_coordinates_in_directions(cls, latitude, longitude, radius):
        """ Рассчитываем координаты в направлении север, юг, восток и запад """
        north_lat, north_lon = cls._calculate_coordinate(latitude, longitude, radius, cls.NORTH_RAD)
        south_lat, south_lon = cls._calculate_coordinate(latitude, longitude, radius, cls.SOUTH_RAD)
        east_lat, east_lon = cls._calculate_coordinate(latitude, longitude, radius, cls.EAST_RAD)
        west_lat, west_lon = cls._calculate_coordinate(latitude, longitude, radius, cls.WEST_RAD)

        data_cord = {
            "latitude": (north_lat, south_lat),
            "longitude": (east_lon, west_lon)
        }
        return data_cord

    @classmethod
    def _calculate_coordinate(cls, lat_rad, lon_rad, distance, direction_rad):
        """ Получаем координаты точки по сторонам света, которые находятся
            на заданном расстоянии от заданной точки
         """
        distance *= 1000
        direction_lat_rad = asin(sin(lat_rad) * cos(distance / cls.EARTH_RADIUS) +
                                 cos(lat_rad) * sin(distance / cls.EARTH_RADIUS) * cos(direction_rad))

        direction_lon_rad = lon_rad + atan2(sin(direction_rad) * sin(distance / cls.EARTH_RADIUS) * cos(lat_rad),
                                            cos(distance / cls.EARTH_RADIUS) - sin(lat_rad) * sin(direction_lat_rad))
    
        direction_latitude = direction_lat_rad
        direction_longitude = direction_lon_rad
    
        return direction_latitude, direction_longitude
    
    @staticmethod
    def _get_ip(user_request):
        x_forwarded_for = user_request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = user_request.META.get('REMOTE_ADDR')
        return ip
