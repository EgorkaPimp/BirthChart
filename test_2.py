from astronomy.city_coordinates import GeoLocator
import asyncio

async def test():
    locator = GeoLocator()
    city = "Дондон"
    coords = await locator.get_coordinates(city)
    time_zona = await locator.get_utc_offset(city_name=city)
    if coords:
        print(coords[0])
        print(coords[1])
        print(time_zona)


if __name__ == "__main__":
    asyncio.run(test())
