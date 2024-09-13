# lighthouse-monitoring
Python package with simple to use decorator for llm monitoring

`pip install lighthouse-monitoring`

Перед применением: 
1. Поднять основной сервис lighthouse-server
2. Добавить в него анализаторы `admin/add_analyzer/`
3. Создать продукт для конкретной модели `admin/add_product/`
4. Для каждого анализатора добавить Vault `vault/add/`. Для каждого анализатора можно получить пример структуры его вольта `vault/example/`.
5. Затем использовать декоратор из данной модели 

## Пример использования
```
from lighthouse-monitoring import LightHouseHandler

@LightHouseHandler(
    input_param_name="user_input",
    api_key="****",
    address="http://example.ru:8080",
)
async def llm_process(user_id: str, user_input: str) -> str:
    output = await model(user_input)
    return output
```