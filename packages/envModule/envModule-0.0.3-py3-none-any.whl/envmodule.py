import os

class EnvModule:
    def __init__(self, env_file='.env'):
        self.env_file = env_file
        self.variables = {}
        self._load_env()

    def _find_env_file(self, current_directory):
        """Рекурсивно ищет файл .env в текущей директории и выше"""
        potential_path = os.path.join(current_directory, self.env_file)

        if os.path.exists(potential_path):
            return potential_path

        # Если достигли корневой директории, прекращаем поиск
        parent_directory = os.path.dirname(current_directory)
        if current_directory == parent_directory:
            return None

        # Продолжаем искать в родительской директории
        return self._find_env_file(parent_directory)

    def _load_env(self):
        """Чтение файла .env и сохранение переменных в словарь"""
        current_directory = os.getcwd()  # Текущая рабочая директория
        env_path = self._find_env_file(current_directory)

        if env_path is None:
            raise FileNotFoundError(f"Файл {self.env_file} не найден в текущей или родительских директориях.")
        
        with open(env_path, 'r') as file:
            for line in file:
                line = line.strip()
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                self.variables[key.strip()] = value.strip()

    def get(self, key, default=None):
        """Возвращает значение переменной по ключу"""
        return self.variables.get(key, default)

# Пример использования
envModule = EnvModule('.env')
api_key = envModule.get('API_KEY')
print(api_key)

# # Пример использования
# envModule = EnvModule('.env')

# # Получение переменной окружения
# api_key = envModule.get('API_KEY')
# debug_mode = envModule.get('DEBUG', 'False')

# print(f"API_KEY: {api_key}")
# print(f"DEBUG_MODE: {debug_mode}")
