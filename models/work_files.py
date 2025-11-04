from pathlib import Path
from aiogram.types import FSInputFile


class Images:
    _base_path = Path("bot/images")
    _cache = {}

    @classmethod
    def get(cls, filename: str) -> FSInputFile:
        if filename not in cls._cache:
            path = cls._base_path / filename
            cls._cache[filename] = FSInputFile(path=str(path))
        return cls._cache[filename]

    @classmethod
    def test_image(cls) -> FSInputFile:
        return cls.get("test.jpg")

    