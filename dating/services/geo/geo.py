from django.conf import settings
from math import sin, cos, asin, atan2, pi, sqrt, radians
import requests
import json


class GeoInterface:

    EARTH_RADIUS = 6356.7523
    NORTH_RAD = 0
    SOUTH_RAD = pi
    EAST_RAD = pi / 2
    WEST_RAD = 3 * pi / 2

    @classmethod
    def get_coordinators(cls, user_request) -> tuple:
        """ Получить координаты из запроса """

        if settings.DEBUG:
            response = requests.get(settings.GEO_API_URL)
        else:
            ip = cls._get_ip(user_request)
            response = requests.get("".join((settings.GEO_API_URL, ip)))
        content = json.loads(response.content)

        longitude = radians(content.get('longitude'))
        latitude = radians(content.get('latitude'))
        return longitude, latitude

    @classmethod
    def get_distance(cls, lon_1, lat_1, lon_2, lat_2):
        """ Получить дистанцию между 2мя точками"""

        d_lat = lat_2 - lat_1
        d_lon = lon_2 - lon_1

        a = sin(d_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(d_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = cls.EARTH_RADIUS * c

        distance = round(distance, 1)
        return distance

    @classmethod
    def calculate_coordinates_in_directions(cls, latitude, longitude, radius):
        """ Рассчитываем координаты в направлении север, юг, восток и запад """

        distance = radius / cls.EARTH_RADIUS

        if radius <= 100:
            data_cord = cls._short_range(latitude, longitude, distance)
            return data_cord

        data_cord = cls._long_distance(latitude, longitude, distance)

        return data_cord

    @staticmethod
    def _short_range(latitude, longitude, distance):
        """ Функция рассчитывающая координаты для поиска в ближнем диапазоне"""

        east_lon = longitude + distance / cos(latitude)
        west_lon = longitude - distance / cos(latitude)
        north_lat = latitude + distance
        south_lat = latitude - distance

        data_cord = {
            "latitude": (north_lat, south_lat),
            "longitude": (east_lon, west_lon)
        }

        return data_cord

    @classmethod
    def _long_distance(cls, latitude, longitude, distance):
        north_lat, north_lon = cls._calculate_coordinate(latitude, longitude, distance, cls.NORTH_RAD)
        south_lat, south_lon = cls._calculate_coordinate(latitude, longitude, distance, cls.SOUTH_RAD)
        east_lat, east_lon = cls._calculate_coordinate(latitude, longitude, distance, cls.EAST_RAD)
        west_lat, west_lon = cls._calculate_coordinate(latitude, longitude, distance, cls.WEST_RAD)

        data_cord = {
            "latitude": (north_lat, south_lat),
            "longitude": (east_lon, west_lon)
        }

        return data_cord

    @staticmethod
    def _calculate_coordinate(lat_rad, lon_rad, distance, direction_rad):
        """ Получаем координаты точки по сторонам света, которые находятся
            на заданном расстоянии от заданной точки
         """

        direction_lat_rad = asin(sin(lat_rad) * cos(distance) +
                                 cos(lat_rad) * sin(distance) * cos(direction_rad))

        direction_lon_rad = lon_rad + atan2(sin(direction_rad) * sin(distance) * cos(lat_rad),
                                            cos(distance) - sin(lat_rad) * sin(direction_lat_rad))
    
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
