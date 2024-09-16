```
# Пример использования
envModule = EnvModule('.env')

# Получение переменной окружения
api_key = envModule.get('API_KEY')
debug_mode = envModule.get('DEBUG', 'False')

print(f"API_KEY: {api_key}")
print(f"DEBUG_MODE: {debug_mode}")
```
