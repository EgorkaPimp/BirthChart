import datetime

import yaml

ZODIAC_SIGNS = ["Овен", "Телец", "Близнецы", "Рак",
                "Лев", "Дева", "Весы", "Скорпион",
                "Стрелец", "Козерог", "Водолей", "Рыбы"]


async def degree_to_sign(degree) -> list:
    sign_index = int(degree // 30)
    deg_in_sign = degree % 30
    return ZODIAC_SIGNS[sign_index], deg_in_sign


async def create_yaml(chart: dict, year: int, month:int, day:int,
                      hour:int, minute:int, place: str) -> str:
    with open('yaml/prompt_base.yaml', 'r', encoding="utf-8") as f:
        templates = yaml.safe_load(f)
    
    templates['user_input_template']['birth_data']["date"] = f"{day}/{month}/{year}"
    templates['user_input_template']['birth_data']["time"] = f"{hour}:{minute}"
    templates['user_input_template']['birth_data']["place"] = place
        
    for key, value in chart.items():
        if key == 'houses':
            for i, cusp in enumerate(value, start=1):
                sign, deg = await degree_to_sign(cusp)
                templates['user_input_template']['houses'][f"house_{i}"] = f"{cusp:.6f}° ({deg:.2f}° {sign})"
        elif key in ['ascendant', 'midheaven']:
            templates['user_input_template']['manifestation'][key] = f"{value['longitude']:.6f}° "
            f"({value['deg_in_sign']:.2f}° {value['sign']})"
        else:
            templates['user_input_template']['planets'][key] = f"{value['longitude']:.6f}° ({value['deg_in_sign']:.2f}° {value['sign']}), "
            f"Lat={value['latitude']:.6f}°, Dist={value['distance_au']:.6f} AU"
        
    yaml_name = f'config_{place}_{day}{month}{year}_{hour}{minute}.yaml'

    with open(f"yaml/{yaml_name}", "w", encoding="utf-8") as f:
        yaml.safe_dump(templates, f, allow_unicode=True, sort_keys=False)

    return yaml_name