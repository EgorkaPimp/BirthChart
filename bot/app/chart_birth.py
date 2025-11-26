from models.start_class import RouterStore, CallbackDataFilter
from models.log_class import LogCLassAll
from aiogram import types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from astronomy.city_coordinates import GeoLocator
from astronomy.planetary_data import start

class Data(StatesGroup):
    waiting_city = State()
    waiting_data = State()

@RouterStore.my_router.callback_query(CallbackDataFilter("chart"))
async def chart(callback: types.CallbackQuery, state: FSMContext):
    LogCLassAll().info('Natal chart calculation has begun')
    await callback.answer()
    await callback.message.delete()
    
    await callback.message.answer("*Введите город в котором вы родились*\n Пример: _Москва_",
                                  parse_mode="Markdown")
    
    await state.set_state(Data.waiting_city)
    
@RouterStore.my_router.message(Data.waiting_city)
async def waiting_city(message: types.Message, state: FSMContext):
    LogCLassAll().info(f'The city has been entered {message.text} Start searching for coordinates and timezone')
    locator = GeoLocator()
    city = message.text
    coords = await locator.get_coordinates(city)
    if coords:
        LogCLassAll().info(f'The coordinates found are latitude {coords[0]}, longitude {coords[1]}.')
        time_zone = await locator.get_utc_offset(city)
        if time_zone:
            LogCLassAll().info(f'Time zone for the {city}: {time_zone}')
            await state.update_data(city=city)
            await state.update_data(time_zone=time_zone)
            await state.update_data(coords=coords)
            await message.answer(f"Ваш город {city}: Широта:{coords[0]} Долгота:{coords[1]} Часовой пояс(UTC): {time_zone}\n"
                           "*Введите дату вашего рождения и время как в примере*\n" 
                           "Пример: _14 08 1996 15:30_",
                            parse_mode="Markdown") 
            await state.set_state(Data.waiting_data)     
    else:
        LogCLassAll().info(f"couldn't find the city {city} coordinates")
        await message.answer(f"Не смог найти координаты для {city}, Проверьте название города.")
        
@RouterStore.my_router.message(Data.waiting_data)
async def waiting_data(message: types.Message, state: FSMContext):
    LogCLassAll().info(f'The date {message.text} for the start of the planetary position calculation has been entered.')
    data = message.text.split(" ")
    year = int(data[2])
    month = int(data[1])
    day = int(data[0])
    time = data[3].split(':')
    hour = int(time[0])
    minute = int(time[1])
    data_city = await state.get_data()
    time_zone = int(data_city.get('time_zone'))
    latitude = float(data_city.get('coords')[0])
    longitude = float(data_city.get('coords')[0])
    place = data_city.get('city')
    natal = await start(year=year, month=month, day=day, hour=hour, minute=minute, 
                        timezone=time_zone, latitude=latitude, longitude=longitude, place=place)
    await state.clear()
    
    text_message = ""
    for line in natal:
        text_message += f"{line}\n"
    
    await message.answer(text_message)
    
    
    