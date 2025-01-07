import asyncio
import json
import os
from typing import Optional

from .logging import local_logger


class KVStore:
    def __init__(self, filename: str = "kv_store.json"):
        self.filename = os.path.join(os.path.dirname(__file__), "..", "..", filename)
        self.store: dict[str, str] = {}
        self.lock = asyncio.Lock()
        # Загружаем хранилище синхронно при инициализации
        self._load_store_sync()

    def _load_store_sync(self) -> None:
        """Синхронно загружает хранилище из файла, если файл существует, иначе создает новое хранилище."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.store = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                # Обработка ошибок загрузки файла
                local_logger.exception(f"Ошибка загрузки хранилища: {e}")
                self.store = {}
        else:
            self.store = {}

    async def _save_store_async(self) -> None:
        """Асинхронно сохраняет текущее состояние хранилища в файл."""
        async with self.lock:
            # Используем run_in_executor для выполнения блокирующих операций в отдельном потоке
            loop = asyncio.get_event_loop()
            temp_filename = f"{self.filename}.tmp"
            await loop.run_in_executor(None, self._write_json, temp_filename)
            # Переименовываем временный файл в основной (атомарная операция)
            await loop.run_in_executor(None, os.replace, temp_filename, self.filename)

    def _write_json(self, temp_filename: str) -> None:
        """Синхронно записывает данные в временный файл."""
        try:
            with open(temp_filename, "w", encoding="utf-8") as f:
                json.dump(self.store, f, ensure_ascii=False, indent=4)
        except IOError as e:
            local_logger.exception(f"Ошибка сохранения хранилища: {e}")
            raise

    async def get(self, key: str) -> Optional[str]:
        """Асинхронно возвращает значение по заданному ключу."""
        return self.store.get(key)

    async def set(self, key: str, value: str) -> None:
        """Асинхронно сохраняет значение по заданному ключу и обновляет файл хранилища."""
        self.store[key] = value
        await self._save_store_async()
