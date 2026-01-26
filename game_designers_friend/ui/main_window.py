"""
Главное окно приложения - Game Designer's Friend
Полная исправленная версия
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import os
import math
from datetime import datetime

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.selected_project = None
        self.projects = []  # Временно для демо
        
        # Инициализируем атрибуты ДО их использования
        self.tree_container = None
        self.meadow_canvas = None
        self.info_panel = None
        self.status_label = None
        
        # Настройка цветовой схемы
        self.setup_colors()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка тестовых проектов
        self.load_demo_projects()
    
    def setup_colors(self):
        """Настройка цветовой схемы"""
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#4CAF50',
            'secondary': '#2196F3',
            'danger': '#f44336',
            'tree_bg': '#2d2d2d',
            'card_bg': '#252525',
            'meadow': '#1B5E20',
            'trunk': '#8B4513',
            'leaves': '#228B22'
        }
        self.root.configure(bg=self.colors['bg'])
    
    def create_widgets(self):
        """Создание всего интерфейса"""
        # Главный контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 1. Панель инструментов (верх)
        self.create_toolbar(main_frame)
        
        # 2. Основная область с двумя колонками
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Левая колонка (70%) - Поляна с деревьями
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        meadow_label = ttk.Label(left_frame, text="🌿 ПОЛЯНА ПРОЕКТОВ", 
                                font=('Arial', 14, 'bold'))
        meadow_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.create_meadow_area(left_frame)
        
        # Правая колонка (30%) - Информация о проекте
        right_frame = ttk.Frame(content_frame, width=400)  # Увеличена ширина до 400
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_frame.pack_propagate(False)  # Фиксируем ширину
        
        info_label = ttk.Label(right_frame, text="📋 ИНФОРМАЦИЯ О ПРОЕКТЕ",
                              font=('Arial', 14, 'bold'))
        info_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.create_info_panel(right_frame)
        
        # 3. Статус бар (низ)
        self.create_statusbar(main_frame)
    
    def create_toolbar(self, parent):
        """Панель инструментов с кнопками"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Основные кнопки
        buttons = [
            ("➕ Новый проект", self.create_new_project, "green"),
            ("✏️ Редактировать", self.edit_selected_project, "blue"),
            ("🗑️ Удалить", self.delete_selected_project, "red"),
            ("⚙️ Настройки", self.open_settings, "gray"),
            ("📊 Статистика", self.show_stats, "orange")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(toolbar, text=text, command=command,
                          bg=self.get_button_color(color),
                          fg='white', font=('Arial', 10),
                          relief=tk.RAISED, bd=2, padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Поиск
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side=tk.RIGHT)
        
        tk.Label(search_frame, text="🔍", font=('Arial', 14)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                              width=25, font=('Arial', 10))
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', self.filter_projects)
    
    def get_button_color(self, color_type):
        """Получение цвета для кнопки"""
        color_map = {
            'green': '#4CAF50',
            'blue': '#2196F3',
            'red': '#f44336',
            'gray': '#757575',
            'orange': '#FF9800'
        }
        return color_map.get(color_type, '#4CAF50')
    
    def create_meadow_area(self, parent):
        """Создание горизонтальной поляны с деревьями"""
        # Контейнер для поляны
        meadow_container = tk.Frame(parent, bg=self.colors['meadow'], 
                                   relief=tk.SUNKEN, bd=2)
        meadow_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas с горизонтальной прокруткой
        canvas_frame = tk.Frame(meadow_container)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas для деревьев
        self.meadow_canvas = tk.Canvas(canvas_frame, 
                                      bg=self.colors['meadow'],
                                      highlightthickness=0)
        
        # Горизонтальный скроллбар
        h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL,
                               command=self.meadow_canvas.xview)
        self.meadow_canvas.configure(xscrollcommand=h_scroll.set)
        
        # Фрейм внутри canvas
        self.tree_container = tk.Frame(self.meadow_canvas, 
                                      bg=self.colors['meadow'])
        self.canvas_window = self.meadow_canvas.create_window(
            (0, 0), window=self.tree_container, anchor=tk.NW
        )
        
        # Размещение
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.meadow_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Бинды
        self.tree_container.bind('<Configure>', self.on_meadow_configure)
        self.meadow_canvas.bind('<Configure>', self.on_meadow_canvas_configure)
        
        # Надпись на земле
        ground_label = tk.Label(meadow_container, 
                               text="← Прокручивайте чтобы увидеть все проекты →",
                               bg=self.colors['meadow'], fg='white',
                               font=('Arial', 10, 'italic'))
        ground_label.pack(side=tk.BOTTOM, pady=5)
    
    def on_meadow_configure(self, event):
        """Обновление scrollregion при изменении поляны"""
        if self.meadow_canvas:
            self.meadow_canvas.configure(scrollregion=self.meadow_canvas.bbox("all"))
    
    def on_meadow_canvas_configure(self, event):
        """Обновление размера окна canvas"""
        if self.meadow_canvas:
            self.meadow_canvas.itemconfig(self.canvas_window, height=event.height)
    
    def create_info_panel(self, parent):
        """Панель информации о проекте (справа)"""
        self.info_panel = tk.Frame(parent, bg=self.colors['card_bg'],
                                  relief=tk.RAISED, bd=2)
        self.info_panel.pack(fill=tk.BOTH, expand=True)
        
        # Изначально показываем заглушку
        self.show_info_placeholder()
    
    def show_info_placeholder(self):
        """Показ заглушки при отсутствии выбранного проекта"""
        if not self.info_panel:
            return
            
        for widget in self.info_panel.winfo_children():
            widget.destroy()
        
        placeholder = tk.Label(self.info_panel,
                             text="👈 Выберите проект\nна поляне",
                             bg=self.colors['card_bg'], fg='white',
                             font=('Arial', 16), pady=50)
        placeholder.pack(expand=True)
    
    def create_statusbar(self, parent):
        """Создание статус бара"""
        statusbar = tk.Frame(parent, bg='#333333', height=30)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        statusbar.pack_propagate(False)
        
        self.status_label = tk.Label(statusbar, text="Готово | Проектов: 0",
                                    bg='#333333', fg='white',
                                    font=('Arial', 10))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Время
        from datetime import datetime
        time_label = tk.Label(statusbar, 
                             text=datetime.now().strftime("%Y-%m-%d %H:%M"),
                             bg='#333333', fg='white',
                             font=('Arial', 10))
        time_label.pack(side=tk.RIGHT, padx=10)
        
        # Обновление времени
        def update_time():
            if time_label.winfo_exists():
                time_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M"))
                self.root.after(60000, update_time)  # Каждую минуту
        
        update_time()
    
    def load_demo_projects(self):
        """Загрузка демонстрационных проектов"""
        self.projects = [
            {
                'id': 1,
                'name': 'Ролевая игра',
                'type': 'game',
                'progress': 75,
                'description': 'Фэнтези RPG с открытым миром и глубоким сюжетом',
                'tech': 'Unity, C#',
                'created': '2024-01-15',
                'language': 'C#',
                'engine': 'Unity',
                'platform': 'PC, Xbox'
            },
            {
                'id': 2,
                'name': 'Мобильное приложение',
                'type': 'app',
                'progress': 30,
                'description': 'Трекер привычек с геймификацией и статистикой',
                'tech': 'React Native, TypeScript',
                'created': '2024-02-10',
                'language': 'TypeScript',
                'engine': 'React Native',
                'platform': 'iOS, Android'
            },
            {
                'id': 3,
                'name': 'Редактор карт',
                'type': 'tool',
                'progress': 90,
                'description': 'Инструмент для создания 2D карт с экспортом в PNG',
                'tech': 'Python, PyQt',
                'created': '2024-01-05',
                'language': 'Python',
                'engine': 'PyQt',
                'platform': 'Windows, Linux, macOS'
            },
            {
                'id': 4,
                'name': 'Визуальная новелла',
                'type': 'game',
                'progress': 50,
                'description': 'Детективная история с выбором пути',
                'tech': 'RenPy, Python',
                'created': '2024-03-01',
                'language': 'Python',
                'engine': 'RenPy',
                'platform': 'PC, Mobile'
            }
        ]
        
        # Безопасная отрисовка деревьев
        self.safe_draw_project_trees()
        if self.status_label:
            self.status_label.config(text=f"Готово | Проектов: {len(self.projects)}")
    
    def safe_draw_project_trees(self):
        """Безопасная отрисовка деревьев проектов"""
        try:
            if hasattr(self, 'tree_container') and self.tree_container and self.tree_container.winfo_exists():
                self.draw_project_trees()
            else:
                # Если контейнер еще не готов, откладываем отрисовку
                self.root.after(100, self.safe_draw_project_trees)
        except Exception as e:
            print(f"Ошибка отрисовки деревьев: {e}")
    
    def draw_project_trees(self):
        """Отрисовка деревьев проектов на поляне"""
        try:
            # Проверяем существование контейнера
            if not hasattr(self, 'tree_container') or not self.tree_container or not self.tree_container.winfo_exists():
                return
                
            # Очищаем контейнер
            for widget in self.tree_container.winfo_children():
                widget.destroy()
            
            # Создаем деревья в ряд
            for i, project in enumerate(self.projects):
                tree_frame = self.create_tree_card(project)
                if tree_frame:
                    tree_frame.pack(side=tk.LEFT, padx=30, pady=20)
                    
        except Exception as e:
            print(f"Ошибка отрисовки деревьев: {e}")
    
    def create_tree_card(self, project):
        """Создание карточки с деревом проекта"""
        try:
            if not hasattr(self, 'tree_container') or not self.tree_container:
                return None
                
            card = tk.Frame(self.tree_container, 
                           bg=self.colors['card_bg'],
                           relief=tk.RAISED, bd=2)
            
            # Canvas для дерева (200x250)
            canvas = tk.Canvas(card, width=200, height=250,
                              bg=self.colors['card_bg'],
                              highlightthickness=0)
            canvas.pack(pady=10)
            
            # Рисуем дерево
            self.draw_tree_on_canvas(canvas, project['progress'])
            
            # Информация о проекте
            info_frame = tk.Frame(card, bg=self.colors['card_bg'])
            info_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Название проекта
            name_label = tk.Label(info_frame, text=project['name'],
                                 bg=self.colors['card_bg'], fg='white',
                                 font=('Arial', 11, 'bold'),
                                 wraplength=180)
            name_label.pack()
            
            # Быстрая информация
            type_icon = "🎮" if project['type'] == 'game' else "📱" if project['type'] == 'app' else "🛠️"
            info_text = f"{type_icon} {project['type']} | 📊 {project['progress']}%"
            info_label = tk.Label(info_frame, text=info_text,
                                 bg=self.colors['card_bg'], fg='#CCCCCC',
                                 font=('Arial', 9))
            info_label.pack()
            
            # Кнопки действий
            btn_frame = tk.Frame(card, bg=self.colors['card_bg'])
            btn_frame.pack(pady=5)
            
            # Кнопка выбора (вход в проект)
            select_btn = tk.Button(btn_frame, text="🌳 Войти",
                                  bg=self.colors['accent'], fg='white',
                                  font=('Arial', 10),
                                  command=lambda p=project: self.enter_project(p),
                                  width=10)
            select_btn.pack(side=tk.LEFT, padx=2)
            
            # Кнопка информации
            info_btn = tk.Button(btn_frame, text="ℹ️",
                                bg='#2196F3', fg='white',
                                command=lambda p=project: self.select_project(p),
                                width=3)
            info_btn.pack(side=tk.LEFT, padx=2)
            
            # Привязываем клик по карточке
            card.bind('<Button-1>', lambda e, p=project: self.select_project(p))
            canvas.bind('<Button-1>', lambda e, p=project: self.select_project(p))
            
            # Эффект наведения
            def on_enter(e):
                if card.winfo_exists():
                    card.configure(relief=tk.SOLID, bd=3)
            
            def on_leave(e):
                if card.winfo_exists() and self.selected_project != project:
                    card.configure(relief=tk.RAISED, bd=2)
            
            card.bind('<Enter>', on_enter)
            card.bind('<Leave>', on_leave)
            canvas.bind('<Enter>', on_enter)
            canvas.bind('<Leave>', on_leave)
            
            return card
            
        except Exception as e:
            print(f"Ошибка создания карточки дерева: {e}")
            return None
    
    def draw_tree_on_canvas(self, canvas, progress):
        """Рисование дерева на canvas"""
        try:
            width = 200
            height = 200
            
            # Определяем размер дерева по прогрессу
            if progress < 25:
                size = 0.6
                leaves_color = '#90EE90'  # Светло-зеленый
            elif progress < 50:
                size = 0.8
                leaves_color = '#7CFC00'  # Зеленоватый
            elif progress < 75:
                size = 1.0
                leaves_color = '#32CD32'  # Лаймовый
            else:
                size = 1.2
                leaves_color = '#228B22'  # Лесной зеленый
            
            # Координаты центра
            center_x = width // 2
            ground_y = height - 20
            
            # Рисуем корни (техническая часть)
            for i in range(3):
                root_x = center_x + (i - 1) * 25
                root_length = 20 + i * 5
                canvas.create_line(root_x, ground_y,
                                 root_x + (i - 1) * 15, ground_y + root_length,
                                 fill='#5D4037', width=10 * size, capstyle=tk.ROUND)
            
            # Рисуем ствол
            trunk_width = 25 * size
            trunk_height = 70 * size
            
            canvas.create_rectangle(center_x - trunk_width//2, ground_y - trunk_height,
                                   center_x + trunk_width//2, ground_y,
                                   fill=self.colors['trunk'], outline='#000000', width=1)
            
            # Рисуем крону
            crown_radius = 50 * size
            crown_y = ground_y - trunk_height - crown_radius//2
            
            canvas.create_oval(center_x - crown_radius, crown_y - crown_radius,
                              center_x + crown_radius, crown_y + crown_radius,
                              fill=leaves_color, outline='#006400', width=2)
            
            # Добавляем листья (количество зависит от прогрессу)
            leaf_count = progress // 10
            for i in range(leaf_count):
                angle = (i / max(leaf_count, 1)) * 360
                rad = math.radians(angle)
                dist = crown_radius * 0.7
                leaf_x = center_x + dist * math.cos(rad)
                leaf_y = crown_y + dist * math.sin(rad)
                
                # Маленькие кружки для листьев
                leaf_size = 5 + (i % 3)
                canvas.create_oval(leaf_x - leaf_size, leaf_y - leaf_size,
                                  leaf_x + leaf_size, leaf_y + leaf_size,
                                  fill='#00FF00', outline='')
            
            # Процент прогресса
            canvas.create_text(center_x, ground_y - 5,
                              text=f"{progress}%",
                              font=('Arial', 12, 'bold'),
                              fill='white')
                              
        except Exception as e:
            print(f"Ошибка рисования дерева: {e}")
    
    def select_project(self, project):
        """Выбор проекта для показа информации"""
        try:
            self.selected_project = project
            self.update_info_panel(project)
            
            # Подсвечиваем выбранную карточку
            if hasattr(self, 'tree_container') and self.tree_container:
                for i, widget in enumerate(self.tree_container.winfo_children()):
                    if widget.winfo_exists():
                        if i == self.projects.index(project):
                            widget.configure(relief=tk.SOLID, bd=3, bg='#3a3a3a')
                        else:
                            widget.configure(relief=tk.RAISED, bd=2, bg=self.colors['card_bg'])
        except Exception as e:
            print(f"Ошибка выбора проекта: {e}")
    
    def update_info_panel(self, project):
        """Обновление информационной панели (ИСПРАВЛЕННЫЕ КНОПКИ)"""
        try:
            if not hasattr(self, 'info_panel') or not self.info_panel:
                return
                
            for widget in self.info_panel.winfo_children():
                widget.destroy()
            
            # Основной контейнер с прокруткой
            main_frame = tk.Frame(self.info_panel, bg=self.colors['card_bg'])
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Canvas для прокрутки
            canvas = tk.Canvas(main_frame, bg=self.colors['card_bg'],
                              highlightthickness=0)
            scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL,
                                    command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Фрейм внутри canvas
            content_frame = tk.Frame(canvas, bg=self.colors['card_bg'])
            
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            canvas.create_window((0, 0), window=content_frame, anchor=tk.NW)
            
            # Функция для обновления scrollregion
            def on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            
            content_frame.bind('<Configure>', on_frame_configure)
            
            # Заголовок
            title_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
            title_frame.pack(fill=tk.X, padx=15, pady=15)
            
            type_icon = "🎮" if project['type'] == 'game' else "📱" if project['type'] == 'app' else "🛠️"
            title_label = tk.Label(title_frame,
                                  text=f"{type_icon} {project['name']}",
                                  bg=self.colors['card_bg'], fg='white',
                                  font=('Arial', 16, 'bold'))
            title_label.pack(anchor=tk.W)
            
            # Статус
            status_text = "🟢 В разработке" if project['progress'] < 100 else "✅ Завершен"
            status_label = tk.Label(title_frame,
                                   text=f"{status_text} | 📅 {project['created']}",
                                   bg=self.colors['card_bg'], fg='#CCCCCC',
                                   font=('Arial', 10))
            status_label.pack(anchor=tk.W, pady=(5, 0))
            
            # Прогресс бар
            progress_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
            progress_frame.pack(fill=tk.X, padx=15, pady=10)
            
            tk.Label(progress_frame, text="Общий прогресс:",
                    bg=self.colors['card_bg'], fg='white').pack(anchor=tk.W)
            
            # Полоса прогресса
            progress_canvas = tk.Canvas(progress_frame, height=20,
                                       bg=self.colors['card_bg'],
                                       highlightthickness=0)
            progress_canvas.pack(fill=tk.X, pady=5)
            
            # Фон прогресс бара
            progress_canvas.create_rectangle(0, 0, 200, 20,
                                            fill='#333333', outline='')
            # Заполнение
            fill_width = int(200 * project['progress'] / 100)
            fill_color = '#4CAF50' if project['progress'] > 50 else '#FF9800'
            progress_canvas.create_rectangle(0, 0, fill_width, 20,
                                            fill=fill_color, outline='')
            # Текст
            progress_canvas.create_text(100, 10,
                                       text=f"{project['progress']}%",
                                       font=('Arial', 10, 'bold'),
                                       fill='white')
            
            # Описание проекта
            desc_frame = tk.LabelFrame(content_frame, text="📝 Описание",
                                      bg=self.colors['card_bg'], fg='white',
                                      font=('Arial', 11, 'bold'),
                                      padx=10, pady=10)
            desc_frame.pack(fill=tk.X, padx=15, pady=10)
            
            desc_text = tk.Text(desc_frame, height=4, wrap=tk.WORD,
                               bg='#333333', fg='white',
                               font=('Arial', 10),
                               relief=tk.FLAT, bd=2)
            desc_text.insert('1.0', project['description'])
            desc_text.configure(state='disabled')
            desc_text.pack(fill=tk.X)
            
            # Технические детали
            tech_frame = tk.LabelFrame(content_frame, text="🛠️ Технические детали",
                                      bg=self.colors['card_bg'], fg='white',
                                      font=('Arial', 11, 'bold'),
                                      padx=10, pady=10)
            tech_frame.pack(fill=tk.X, padx=15, pady=10)
            
            details = [
                ("Тип проекта:", project['type'].capitalize()),
                ("Язык программирования:", project.get('language', 'Не указан')),
                ("Движок/Фреймворк:", project.get('engine', 'Не указан')),
                ("Платформа:", project.get('platform', 'Не указан')),
                ("Технологии:", project['tech'])
            ]
            
            for label, value in details:
                detail_frame = tk.Frame(tech_frame, bg=self.colors['card_bg'])
                detail_frame.pack(fill=tk.X, pady=2)
                
                tk.Label(detail_frame, text=label,
                        bg=self.colors['card_bg'], fg='#CCCCCC',
                        font=('Arial', 9, 'bold'),
                        width=25, anchor=tk.W).pack(side=tk.LEFT)
                
                tk.Label(detail_frame, text=value,
                        bg=self.colors['card_bg'], fg='white',
                        font=('Arial', 9),
                        anchor=tk.W).pack(side=tk.LEFT)
            
            # Кнопки действий - ИСПРАВЛЕНО: ВЕРТИКАЛЬНОЕ РАСПОЛОЖЕНИЕ
            action_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
            action_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
            
            actions = [
                ("🌳 Открыть проект", self.enter_project),
                ("✏️ Редактировать проект", lambda p=project: self.edit_project(p)),
                ("👥 Совместный доступ", lambda p=project: self.share_project(p)),
                ("📁 Открыть папку проекта", lambda p=project: self.open_project_folder(p))
            ]
            
            for text, command in actions:
                btn = tk.Button(action_frame, text=text,
                              bg='#333333', fg='white',
                              font=('Arial', 9),
                              command=lambda c=command, p=project: c(p),
                              height=1,
                              wraplength=250,  # Перенос текста
                              anchor='w',      # Выравнивание по левому краю
                              justify='left')  # Выравнивание текста слева
                btn.pack(fill=tk.X, pady=3, ipady=5)  # Заполнение по ширине
            
            # Добавляем отступ снизу
            tk.Frame(content_frame, height=10, bg=self.colors['card_bg']).pack()
                
        except Exception as e:
            print(f"Ошибка обновления информационной панели: {e}")
    
    def create_new_project(self):
        """Создание нового проекта"""
        # Упрощенная версия для начала
        name = simpledialog.askstring("Новый проект", "Введите название проекта:")
        if name:
            new_project = {
                'id': len(self.projects) + 1,
                'name': name,
                'type': 'game',
                'progress': 0,
                'description': 'Новый проект',
                'tech': 'Python',
                'created': datetime.now().strftime("%Y-%m-%d"),
                'language': 'Python',
                'engine': 'Custom',
                'platform': 'Windows',
                'genre': '',
                'music': 'Не требуется',
                'tags': [],
                'difficulty': 3
            }
            self.projects.append(new_project)
            self.safe_draw_project_trees()
            if self.status_label:
                self.status_label.config(text=f"Создан проект '{name}' | Проектов: {len(self.projects)}")
            messagebox.showinfo("Успех", f"Проект '{name}' создан!")
    
    def enter_project(self, project):
        """Вход в проект"""
        try:
            project_window = tk.Toplevel(self.root)
            project_window.title(f"🌳 {project['name']}")
            project_window.geometry("600x500")
            project_window.configure(bg=self.colors['bg'])
            
            # Центрируем окно
            project_window.update_idletasks()
            width = project_window.winfo_width()
            height = project_window.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            project_window.geometry(f'600x500+{x}+{y}')
            
            # Заголовок
            header = tk.Frame(project_window, bg='#333333', height=50)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            
            back_btn = tk.Button(header, text="← Назад",
                                command=project_window.destroy,
                                bg='#444444', fg='white',
                                font=('Arial', 10))
            back_btn.pack(side=tk.LEFT, padx=10, pady=10)
            
            title_label = tk.Label(header, text=f"Проект: {project['name']}",
                                  bg='#333333', fg='white',
                                  font=('Arial', 14, 'bold'))
            title_label.pack(side=tk.LEFT, padx=20, pady=10)
            
            # Контент
            content = tk.Frame(project_window, bg=self.colors['bg'])
            content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Информация о проекте
            info_text = f"""
            🎯 Название: {project['name']}
            📊 Прогресс: {project['progress']}%
            🛠️ Технологии: {project['tech']}
            📅 Создан: {project['created']}
            
            📝 Описание:
            {project['description']}
            """
            
            info_label = tk.Label(content, text=info_text,
                                 bg=self.colors['bg'], fg='white',
                                 font=('Arial', 11),
                                 justify=tk.LEFT)
            info_label.pack(anchor=tk.W, pady=10)
            
            # Кнопки для частей дерева
            parts_frame = tk.Frame(content, bg=self.colors['bg'])
            parts_frame.pack(fill=tk.X, pady=20)
            
            parts = [
                ("🌱 Корни (Техника)", lambda: self.show_tech_details(project)),
                ("🪵 Ствол (Основа)", lambda: self.show_core_details(project)),
                ("🌿 Ветви (Контент)", lambda: self.show_content_details(project)),
                ("🍃 Листья (Полировка)", lambda: self.show_polish_details(project))
            ]
            
            for text, command in parts:
                btn = tk.Button(parts_frame, text=text,
                              command=command,
                              bg='#333333', fg='white',
                              font=('Arial', 10),
                              width=20, height=2)
                btn.pack(side=tk.LEFT, padx=5, fill=tk.Y, expand=True)
                
        except Exception as e:
            print(f"Ошибка входа в проект: {e}")
            messagebox.showerror("Ошибка", f"Не удалось открыть проект: {e}")
    
    def edit_selected_project(self):
        """Редактирование выбранного проекта"""
        if not self.selected_project:
            messagebox.showwarning("Не выбран проект", "Выберите проект на поляне")
            return
        self.edit_project(self.selected_project)
    
    def edit_project(self, project):
        """Окно редактирования проекта"""
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Редактирование: {project['name']}")
            dialog.geometry("400x400")
            dialog.configure(bg=self.colors['bg'])
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Центрируем
            dialog.update_idletasks()
            width = dialog.winfo_width()
            height = dialog.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            dialog.geometry(f'{width}x{height}+{x}+{y}')
            
            # Заголовок
            title_label = tk.Label(dialog, text=f"Редактирование проекта",
                                  bg=self.colors['bg'], fg='white',
                                  font=('Arial', 14, 'bold'))
            title_label.pack(pady=10)
            
            # Форма
            form_frame = tk.Frame(dialog, bg=self.colors['bg'])
            form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Название
            tk.Label(form_frame, text="Название:",
                    bg=self.colors['bg'], fg='white').pack(anchor=tk.W)
            name_var = tk.StringVar(value=project['name'])
            name_entry = tk.Entry(form_frame, textvariable=name_var,
                                 font=('Arial', 11))
            name_entry.pack(fill=tk.X, pady=(0, 10))
            
            # Описание
            tk.Label(form_frame, text="Описание:",
                    bg=self.colors['bg'], fg='white').pack(anchor=tk.W)
            desc_text = scrolledtext.ScrolledText(form_frame, height=6,
                                                 font=('Arial', 10))
            desc_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            desc_text.insert('1.0', project['description'])
            
            # Прогресс
            tk.Label(form_frame, text="Прогресс (%):",
                    bg=self.colors['bg'], fg='white').pack(anchor=tk.W)
            progress_var = tk.IntVar(value=project['progress'])
            progress_scale = tk.Scale(form_frame, from_=0, to=100,
                                     variable=progress_var,
                                     orient=tk.HORIZONTAL,
                                     bg=self.colors['bg'], fg='white')
            progress_scale.pack(fill=tk.X, pady=(0, 10))
            
            def on_save():
                """Сохранение изменений"""
                project['name'] = name_var.get()
                project['description'] = desc_text.get("1.0", tk.END).strip()
                project['progress'] = progress_var.get()
                
                # Обновляем интерфейс
                self.safe_draw_project_trees()
                if self.selected_project == project:
                    self.update_info_panel(project)
                
                messagebox.showinfo("Сохранено", "Изменения сохранены")
                dialog.destroy()
            
            # Кнопки
            btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
            btn_frame.pack(fill=tk.X, padx=20, pady=10)
            
            cancel_btn = tk.Button(btn_frame, text="Отмена",
                                  command=dialog.destroy,
                                  bg='#666666', fg='white')
            cancel_btn.pack(side=tk.LEFT, padx=5)
            
            save_btn = tk.Button(btn_frame, text="Сохранить",
                                command=on_save,
                                bg=self.colors['accent'], fg='white',
                                font=('Arial', 10, 'bold'))
            save_btn.pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            print(f"Ошибка редактирования проекта: {e}")
            messagebox.showerror("Ошибка", f"Не удалось открыть редактор: {e}")
    
    def delete_selected_project(self):
        """Удаление выбранного проекта"""
        if not self.selected_project:
            messagebox.showwarning("Не выбран проект", "Выберите проект на поляне")
            return
        
        self.delete_project_dialog(self.selected_project)
    
    def delete_project_dialog(self, project):
        """Диалог удаления проекта"""
        response = messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить проект:\n"
            f"\"{project['name']}\"?\n\n"
            f"Это действие нельзя отменить!"
        )
        
        if response:
            # Удаляем проект
            self.projects = [p for p in self.projects if p['id'] != project['id']]
            
            # Сбрасываем выбор
            if self.selected_project == project:
                self.selected_project = None
                self.show_info_placeholder()
            
            # Обновляем интерфейс
            self.safe_draw_project_trees()
            if self.status_label:
                self.status_label.config(text=f"Проект '{project['name']}' удален | Проектов: {len(self.projects)}")
    
    def open_settings(self):
        """Открытие настроек приложения"""
        try:
            settings_window = tk.Toplevel(self.root)
            settings_window.title("Настройки приложения")
            settings_window.geometry("400x300")
            settings_window.configure(bg=self.colors['bg'])
            settings_window.transient(self.root)
            
            # Центрируем
            settings_window.update_idletasks()
            width = settings_window.winfo_width()
            height = settings_window.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            settings_window.geometry(f'{width}x{height}+{x}+{y}')
            
            # Заголовок
            title_label = tk.Label(settings_window, text="⚙️ НАСТРОЙКИ",
                                  bg=self.colors['bg'], fg='white',
                                  font=('Arial', 16, 'bold'))
            title_label.pack(pady=20)
            
            # Содержимое
            content = tk.Frame(settings_window, bg=self.colors['bg'])
            content.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
            
            # Настройки
            tk.Label(content, text="Тема:",
                    bg=self.colors['bg'], fg='white').pack(anchor=tk.W)
            theme_var = tk.StringVar(value="Темная")
            theme_combo = ttk.Combobox(content, textvariable=theme_var,
                                      values=["Темная", "Светлая"])
            theme_combo.pack(fill=tk.X, pady=(0, 10))
            
            # Автосохранение
            autosave_var = tk.BooleanVar(value=True)
            tk.Checkbutton(content, text="Автосохранение",
                          variable=autosave_var,
                          bg=self.colors['bg'], fg='white',
                          selectcolor='#333333').pack(anchor=tk.W, pady=10)
            
            # Кнопки
            btn_frame = tk.Frame(settings_window, bg=self.colors['bg'])
            btn_frame.pack(fill=tk.X, padx=30, pady=20)
            
            cancel_btn = tk.Button(btn_frame, text="Отмена",
                                  command=settings_window.destroy,
                                  bg='#666666', fg='white')
            cancel_btn.pack(side=tk.LEFT, padx=5)
            
            save_btn = tk.Button(btn_frame, text="Сохранить",
                                command=settings_window.destroy,
                                bg=self.colors['accent'], fg='white')
            save_btn.pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            print(f"Ошибка открытия настроек: {e}")
            messagebox.showerror("Ошибка", "Не удалось открыть настройки")
    
    def show_stats(self):
        """Показать статистику"""
        total = len(self.projects)
        in_progress = sum(1 for p in self.projects if p['progress'] < 100)
        completed = sum(1 for p in self.projects if p['progress'] == 100)
        
        stats_text = f"""
        📊 Статистика проектов:
        
        Всего проектов: {total}
        В разработке: {in_progress}
        Завершено: {completed}
        
        Средний прогресс: {sum(p['progress'] for p in self.projects) // max(total, 1)}%
        """
        
        messagebox.showinfo("Статистика", stats_text)
    
    # Методы для частей дерева
    def show_tech_details(self, project):
        """Показать технические детали"""
        messagebox.showinfo("Техническая часть", 
                          f"Технические детали проекта '{project['name']}':\n\n"
                          f"Язык: {project.get('language', 'Не указан')}\n"
                          f"Движок: {project.get('engine', 'Не указан')}\n"
                          f"Платформа: {project.get('platform', 'Не указан')}\n"
                          f"Архитектура: Не указана")
    
    def show_core_details(self, project):
        """Показать основу проекта"""
        messagebox.showinfo("Основа проекта", 
                          f"Основа проекта '{project['name']}':\n\n"
                          f"Тип: {project['type']}\n"
                          f"Жанр: {project.get('genre', 'Не указан')}\n"
                          f"Сложность: {project.get('difficulty', 3)}/5\n"
                          f"Описание: {project['description']}")
    
    def show_content_details(self, project):
        """Показать контент проекта"""
        messagebox.showinfo("Контент проекта", 
                          f"Контент проекта '{project['name']}':\n\n"
                          f"Графика: Не указано\n"
                          f"Звук: {project.get('music', 'Не указано')}\n"
                          f"Теги: {', '.join(project.get('tags', [])) if project.get('tags') else 'Нет'}")
    
    def show_polish_details(self, project):
        """Показать полировку проекта"""
        messagebox.showinfo("Полировка проекта", 
                          f"Полировка проекта '{project['name']}':\n\n"
                          f"Тестирование: Не начато\n"
                          f"Оптимизация: Не начата\n"
                          f"Документация: Не начата\n"
                          f"Балансировка: Не требуется")
    
    # Простые заглушки для остальных методов
    def filter_projects(self, event=None):
        """Фильтрация проектов"""
        search_text = self.search_var.get().lower()
        if self.status_label:
            self.status_label.config(text=f"Поиск: {search_text}")
    
    def share_project(self, project=None):
        """Совместный доступ"""
        if not project and self.selected_project:
            project = self.selected_project
        elif not project:
            messagebox.showwarning("Ошибка", "Выберите проект")
            return
            
        token = project.get('share_token', 'Не создан')
        messagebox.showinfo("Совместный доступ", 
                          f"Токен доступа к проекту '{project['name']}':\n\n"
                          f"{token}\n\n"
                          f"Поделитесь этим токеном для предоставления доступа.")
    
    def open_project_folder(self, project=None):
        """Открыть папку проекта"""
        if not project and self.selected_project:
            project = self.selected_project
        elif not project:
            messagebox.showwarning("Ошибка", "Выберите проект")
            return
            
        # Создаем папку для проекта
        project_dir = f"data/projects/{project['id']}_{project['name']}"
        os.makedirs(project_dir, exist_ok=True)
        
        # Создаем файл с информацией
        info_file = os.path.join(project_dir, "info.txt")
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(f"Проект: {project['name']}\n")
            f.write(f"Тип: {project['type']}\n")
            f.write(f"Описание: {project['description']}\n")
            f.write(f"Технологии: {project['tech']}\n")
            f.write(f"Создан: {project['created']}\n")
        
        messagebox.showinfo("Папка проекта", 
                          f"Папка проекта создана:\n{project_dir}\n\n"
                          f"Файл с информацией сохранен.")