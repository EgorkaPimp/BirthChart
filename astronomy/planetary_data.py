import swisseph as swe
from city_coordinates import GeoLocator
import asyncio

ZODIAC_SIGNS = ["Овен", "Телец", "Близнецы", "Рак",
                "Лев", "Дева", "Весы", "Скорпион",
                "Стрелец", "Козерог", "Водолей", "Рыбы"]

NAME_PLANET = {
        'Sun': 'Солнце',
        'Moon': 'Луна',
        'Mercury': 'Меркурий',
        'Venus': 'Венера',
        'Mars': 'Марс',
        'Jupiter': 'Юпитер',
        'Saturn': 'Сатурн',
        'Uranus': 'Уран',
        'Neptune': 'Нептун',
        'Pluto': 'Плутон',
        'ascendant': 'Асцендент',
        'midheaven': 'Середина небы'
    }

async def julian_day(year, month, day, hour, minute, timezone) -> float:
    return swe.julday(year, month, day, hour + minute/60 - timezone)

async def degree_to_sign(degree) -> list:
    sign_index = int(degree // 30)
    deg_in_sign = degree % 30
    return ZODIAC_SIGNS[sign_index], deg_in_sign


async def natal_chart(year: int, month: int, day: int, hour: int, minute: int, 
                      latitude: float, longitude: float, timezone: int) -> dict:
    jd = await julian_day(year, month, day, hour, minute, timezone)
    
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mercury': swe.MERCURY,
        'Venus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO
    }
    
    chart = {}
    for name, code in planets.items():
        lon_lat_dist, ret_flag = swe.calc_ut(jd, code)
        zodiac_sign, deg_in_sign = await degree_to_sign(lon_lat_dist[0])
        chart[name] = {
            'longitude': lon_lat_dist[0],
            'latitude': lon_lat_dist[1],
            'distance_au': lon_lat_dist[2],
            'sign': zodiac_sign,
            'deg_in_sign': deg_in_sign
        }
    
    houses, ascmc = swe.houses(jd, latitude, longitude, b'P')
    chart['houses'] = houses
    asc_sign, asc_deg = await degree_to_sign(ascmc[0])
    mc_sign, mc_deg = await degree_to_sign(ascmc[1])
    chart['ascendant'] = {'longitude': ascmc[0], 'sign': asc_sign, 'deg_in_sign': asc_deg}
    chart['midheaven'] = {'longitude': ascmc[1], 'sign': mc_sign, 'deg_in_sign': mc_deg}
    
    return chart

async def report_chart(chart: dict):
    for key, value in chart.items():
        if key == 'houses':
            for i, cusp in enumerate(value, start=1):
                sign, deg = await degree_to_sign(cusp)
                print(f"Дом {i}: {cusp:.6f}° ({deg:.2f}° {sign})")
        elif key in ['ascendant', 'midheaven']:
            print(f"{NAME_PLANET[key]}: {value['longitude']:.6f}° "
                  f"({value['deg_in_sign']:.2f}° {value['sign']})")
        else:
            print(f"{NAME_PLANET[key]}: {value['longitude']:.6f}° ({value['deg_in_sign']:.2f}° {value['sign']}), "
                  f"Lat={value['latitude']:.6f}°, Dist={value['distance_au']:.6f} AU")
    


async def test(city:str, data_birth:str, time_birth: str):
    locator = GeoLocator()
    coords = await locator.get_coordinates(city)
    data = data_birth.split(" ")
    time = time_birth.split(" ")
    
    hour = int(time[0])
    minute = int(time[1])
    
    timezone = await locator.get_utc_offset(city_name=city)
    
    year = int(data[2])
    month = int(data[1])
    day = int(data[0])
    
    latitude = coords[0]
    longitude = coords[1]
    
    chart = await natal_chart(year, month, day, hour, minute, latitude, longitude, timezone)
    await report_chart(chart=chart)
    
    
 
if __name__ == "__main__":
    city = "Пенза"
    data_birth = "14 8 1996"
    time_birth = "15 30"
    asyncio.run(test(city=city, 
                     data_birth=data_birth, 
                     time_birth=time_birth))