"""
Менеджер настроек приложения
"""
import json
import os
from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass
class Settings:
    # Общие настройки
    project_path: str = "data/projects"
    autosave: bool = True
    autosave_interval: int = 5  # минут
    backup_on_start: bool = True
    
    # Внешний вид
    theme: str = "dark"
    font_size: int = 10
    opacity: float = 1.0
    compact_view: bool = False
    show_progress: bool = True
    
    # Проекты по умолчанию
    default_language: str = "Python"
    default_type: str = "game"
    default_engine: str = ""
    default_platform: str = "Windows"
    
    # Совместная работа
    enable_sharing: bool = True
    share_by_default: bool = False
    
    # Расширенные настройки
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SettingsManager:
    """Класс для управления настройками приложения"""
    
    def __init__(self, config_file: str = "config/settings.json"):
        self.config_file = config_file
        self.settings = self.load_settings()
    
    def load_settings(self) -> Settings:
        """Загрузка настроек из файла"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return Settings(**data)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        
        # Возвращаем настройки по умолчанию
        return Settings()
    
    def save_settings(self) -> bool:
        """Сохранение настроек в файл"""
        try:
            # Создаем директорию если не существует
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            return False
    
    def get(self, key: str, default=None) -> Any:
        """Получение значения настройки"""
        return getattr(self.settings, key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Установка значения настройки"""
        try:
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
                self.save_settings()
                return True
            return False
        except Exception as e:
            print(f"Ошибка установки настройки: {e}")
            return False
    
    def update(self, **kwargs) -> bool:
        """Обновление нескольких настроек"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.settings, key):
                    setattr(self.settings, key, value)
            self.save_settings()
            return True
        except Exception as e:
            print(f"Ошибка обновления настроек: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Сброс настроек к значениям по умолчанию"""
        self.settings = Settings()
        return self.save_settings()
    
    def get_all_settings(self) -> dict:
        """Получение всех настроек в виде словаря"""
        return asdict(self.settings)


# Для быстрого доступа можно создать глобальный экземпляр
_default_settings_manager = None

def get_settings_manager(config_file: str = "config/settings.json") -> SettingsManager:
    """Получение глобального менеджера настроек"""
    global _default_settings_manager
    if _default_settings_manager is None:
        _default_settings_manager = SettingsManager(config_file)
    return _default_settings_manager