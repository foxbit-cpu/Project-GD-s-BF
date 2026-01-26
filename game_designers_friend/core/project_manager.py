import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Any
from enum import Enum

class ProjectStatus(Enum):
    SEED = "seed"        # Идея
    SPROUT = "sprout"    # В разработке
    TREE = "tree"        # Завершен
    WILTED = "wilted"    # Заморожен

class ProjectType(Enum):
    GAME = "game"
    APP = "application"
    TOOL = "tool"
    OTHER = "other"

@dataclass
class Project:
    id: str
    name: str
    project_type: ProjectType
    status: ProjectStatus
    created_date: str
    last_modified: str
    
    # Основные части (ствол)
    mechanics: str = ""
    story: str = ""
    description: str = ""
    
    # Техническая часть (корни)
    technology: str = ""
    architecture: str = ""
    dependencies: List[str] = field(default_factory=list)
    
    # Контент (ветви и листья)
    graphics_progress: int = 0
    sound_progress: int = 0
    music_progress: int = 0
    polish_progress: int = 0
    
    # Метаданные
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    collaborators: List[str] = field(default_factory=list)
    share_token: Optional[str] = None
    
    # Новые поля
    engine: str = ""
    programming_language: str = ""
    genre: str = ""
    platform: List[str] = field(default_factory=list)
    team_members: List[Dict[str, str]] = field(default_factory=list)
    deadline: str = ""
    budget: float = 0.0
    
    # Для расширения
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def overall_progress(self) -> int:
        """Общий прогресс проекта"""
        total = (self.graphics_progress + self.sound_progress + 
                self.music_progress + self.polish_progress)
        return total // 4