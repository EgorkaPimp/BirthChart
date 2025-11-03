import requests
from timezonefinder import TimezoneFinder
from datetime import datetime, timezone
import pytz


class GeoLocator:
    def __init__(self, user_agent="GeoLocatorApp"):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {"User-Agent": user_agent}
        self.tzf = TimezoneFinder()


    async def get_coordinates(self, city_name: str) -> list:
        params = {
            "q": city_name,
            "format": "json",
            "limit": 1,
            "accept-language": "ru" 
        }

        response = requests.get(self.base_url, params=params, headers=self.headers)
        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code}")
            return None

        data = response.json()
        if not data:
            print("Город не найден")
            return None

        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    
    async def get_utc_offset(self, city_name: str) -> int: 
        coords = await self.get_coordinates(city_name)
        if not coords:
            return None

        lat, lon = coords
        tz_name = self.tzf.timezone_at(lat=lat, lng=lon)
        if not tz_name:
            return None

        tz = pytz.timezone(tz_name)
        now_utc = datetime.now(timezone.utc)        
        now_local = now_utc.astimezone(tz)           
        offset = now_local.utcoffset()               
        if not offset:
            return None

        total_seconds = offset.total_seconds()
        hours = int(total_seconds // 3600)
        return hours
    
    
