#!/usr/bin/env python3
"""
Минимальный скрипт для генерации натальных карт через локальную LLM
"""

import yaml
import requests
import json
from pathlib import Path
import sys


class NatalChartGenerator:
    def __init__(self, config_path="config/settings.yaml"):
        # Загружаем конфигурацию
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # Настройки Ollama
        self.ollama_host = self.config['ollama']['host']
        self.model = self.config['ollama']['model']

        # Создаем папки если их нет
        Path("data/charts").mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(parents=True, exist_ok=True)

    def load_natal_data(self, yaml_file):
        """Загружает данные о планетах из YAML файла"""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        print(f"📊 Загружены данные для: {data.get('name', 'Неизвестный')}")
        print(f"   Дата рождения: {data.get('birth_date', 'Не указана')}")

        return data

    def create_prompt(self, natal_data):
        """Создает промпт для LLM на основе данных"""

        # Базовый шаблон промпта
        prompt_template = """
Ты - опытный астролог с 20-летним стажем. Проанализируй натальную карту и предоставь подробную интерпретацию.

ДАННЫЕ КЛИЕНТА:
Имя: {name}
Дата рождения: {birth_date}
Место рождения: {birth_place}
Время рождения: {birth_time}

ПОЛОЖЕНИЯ ПЛАНЕТ:
{planets}

АСПЕКТЫ:
{aspects}

ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:
{additional_info}

ИНСТРУКЦИИ:
1. Проанализируй влияние каждой планеты в знаке и доме
2. Рассмотри основные аспекты между планетами
3. Опиши характер и потенциал личности
4. Укажите сильные и слабые стороны
5. Дай рекомендации по развитию
6. Будь конкретным, но тактичным

Формат ответа:
# Натальная карта для {name}

## 1. Общая характеристика
[Твой анализ]

## 2. Анализ планет
[По планете]

## 3. Ключевые аспекты
[По аспектам]

## 4. Рекомендации
[Твои рекомендации]

Будь профессиональным и точным в интерпретациях.
"""

        # Форматируем данные планет
        planets_text = ""
        for planet, position in natal_data.get('planets', {}).items():
            planets_text += f"- {planet.capitalize()}: {position}\n"

        # Форматируем аспекты
        aspects_text = ""
        for aspect in natal_data.get('aspects', []):
            aspects_text += f"- {aspect}\n"

        # Заполняем шаблон
        prompt = prompt_template.format(
            name=natal_data.get('name', 'Клиент'),
            birth_date=natal_data.get('birth_date', 'Не указано'),
            birth_place=natal_data.get('birth_place', 'Не указано'),
            birth_time=natal_data.get('birth_time', 'Не указано'),
            planets=planets_text,
            aspects=aspects_text,
            additional_info=natal_data.get('notes', 'Нет дополнительной информации')
        )

        return prompt

    def generate_chart(self, prompt):
        """Отправляет промпт в LLM и получает ответ"""
        print("🧠 Генерирую натальную карту...")

        url = f"{self.ollama_host}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config['generation']['temperature'],
                "num_predict": self.config['generation']['max_tokens']
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=self.config['ollama']['timeout'])
            response.raise_for_status()

            result = response.json()
            return result['response']

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при запросе к LLM: {e}")
            return None

    def save_chart(self, chart_text, filename):
        """Сохраняет сгенерированную карту в файл"""
        chart_path = Path("data/charts") / f"{filename}.md"

        with open(chart_path, 'w', encoding='utf-8') as f:
            f.write(chart_text)

        print(f"💾 Натальная карта сохранена: {chart_path}")
        return chart_path

    def run(self, input_yaml):
        """Основной метод запуска"""
        print("=" * 50)
        print("🪐 ГЕНЕРАТОР НАТАЛЬНЫХ КАРТ")
        print("=" * 50)

        # 1. Загружаем данные
        natal_data = self.load_natal_data(input_yaml)

        # 2. Создаем промпт
        prompt = self.create_prompt(natal_data)

        # 3. Генерируем карту
        chart_text = self.generate_chart(prompt)

        if chart_text:
            # 4. Сохраняем результат
            filename = f"{natal_data.get('name', 'chart').replace(' ', '_')}_{natal_data.get('birth_date', 'unknown')}"
            self.save_chart(chart_text, filename)

            # 5. Показываем результат
            print("\n" + "=" * 50)
            print("✨ СГЕНЕРИРОВАННАЯ НАТАЛЬНАЯ КАРТА:")
            print("=" * 50)
            print(chart_text[:500] + "..." if len(chart_text) > 500 else chart_text)
            print("=" * 50)
        else:
            print("❌ Не удалось сгенерировать натальную карту")


def main():
    """Точка входа"""

    # Проверяем аргументы командной строки
    if len(sys.argv) < 2:
        print("Использование: python main.py <путь_к_yaml_файлу>")
        print("Пример: python main.py data/input/example.yaml")
        sys.exit(1)

    input_file = sys.argv[1]

    # Проверяем существование файла
    if not Path(input_file).exists():
        print(f"❌ Файл не найден: {input_file}")
        sys.exit(1)

    # Создаем генератор и запускаем
    generator = NatalChartGenerator()
    generator.run(input_file)


if __name__ == "__main__":
    main()