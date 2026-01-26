"""
Главный файл приложения - Game Designer's Friend
"""
import tkinter as tk
import os
import sys
from ui.main_window import MainWindow

def setup_directories():
    """Создание необходимых директорий"""
    dirs = [
        "data/projects",
        "data/templates", 
        "data/exports",
        "assets/tree_icons",
        "assets/backgrounds",
        "backups",
        "config"
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Создана директория: {directory}")

def main():
    """Основная функция запуска приложения"""
    try:
        # Настройка директорий
        print("Инициализация приложения...")
        setup_directories()
        
        # Создание главного окна
        root = tk.Tk()
        root.title("🌿 Поляна проектов - Game Designer's Friend")
        root.geometry("1200x700")
        
        # Центрируем окно
        root.update_idletasks()
        width = 1200
        height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Загружаем приложение
        print("Загрузка интерфейса...")
        app = MainWindow(root)
        
        print("✓ Приложение запущено успешно!")
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()