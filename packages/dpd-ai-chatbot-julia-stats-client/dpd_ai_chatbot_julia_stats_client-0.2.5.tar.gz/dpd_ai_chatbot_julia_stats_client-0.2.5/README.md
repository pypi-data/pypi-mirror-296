# dpd-ai-chatbot-julia-stats-client

>Ver 0.2.5

## Описание  

Проект клиента для сервиса dpd-ai-chatbot-julia-stats-api.  
Содержит модель для валидации данных при отправке в бэкэнд, а также класс клиента, который осуществляет подключение к API, с помощью метода POST.  

## Установка библиотеки

```sh
pip install dpd-ai-chatbot-julia-stats-client
```

### Зависимости

Зависимости проекта описаны в [pyproject.toml](pyproject.toml).

## Example usage  

### Использование моделей данных

```python
from dpd_ai_chatbot_julia_stats_client.models import OrderState

data = {
        "order_id": "RU12345",
        "ordernum": "123",
        "plan_delivery_moment": "2023-10-15T10:00:00",
        "order_combo_state": "В пути",
        "available_delivery_date": "2023-10-16T10:00:00",
        "parcel_department_id": 12467456,
        "parcel_state": "Доставлено",
        "plan_shipment_end_moment": "2023-10-14T18:00:00",
        "delivery_terminal_code": "Терминал 1",
        "consignee_address": "Улица Примерная, дом 1",
        "order_delivery_to_door": 1,
        "is_carrier_area": True,
        "carrier_track_number": "ABC123456789",
        "business_dict_code": 12,
        "clientnom": 88005553535,
        "brand_client_tts": "Бренд A",
        "client_redelivery_pay": False,
        "reason_code": 82312,
        "consignee": "Иван Иванов",
        "cntmovepddbyerr": 0,
        "consignee_phone": "+70001234567",
        "is_map": True,
        "is_pps": False,
        "current_delivery_attempts": 1,
        "state_name": "Зарег",
        "order_last_state_reason_code": "ЛК123"
    }

model = OrderState(**data)


```

```python
from dpd_ai_chatbot_julia_stats_client.models import Dialog

data = {"SessionId": "RU12345"}

model = Dialog(**data)
```

Класс модели имеет встроенную валидацию типов. А также гарантирует наличие объязательных полей.  

### Главный сценарий использования

```python
import asyncio

from dpd_ai_chatbot_julia_stats_client.models import OrderState
from dpd_ai_chatbot_julia_stats_client.client import Chronicler

data = {
        "order_id": "RU12345",
        "ordernum": "123",
        "plan_delivery_moment": "2023-10-15T10:00:00",
        "order_combo_state": "В пути",
        "available_delivery_date": "2023-10-16T10:00:00",
        "parcel_department_id": 12467456,
        "parcel_state": "Доставлено",
        "plan_shipment_end_moment": "2023-10-14T18:00:00",
        "delivery_terminal_code": "Терминал 1",
        "consignee_address": "Улица Примерная, дом 1",
        "order_delivery_to_door": "1",
        "is_carrier_area": "True",
        "carrier_track_number": "ABC123456789",
        "business_dict_code": 12,
        "clientnom": 88005553535,
        "brand_client_tts": "Бренд A",
        "client_redelivery_pay": False,
        "reason_code": 82312,
        "consignee": "Иван Иванов",
        "cntmovepddbyerr": 0,
        "consignee_phone": "+70001234567",
        "is_map": True,
        "is_pps": False,
        "current_delivery_attempts": 1,
        "state_name": "Зарег",
        "order_last_state_reason_code": "ЛК123"
    }

model = OrderState(**data).model_dump_json()

chronicler = Chronicler(API_LINK)

asyncio.run(chronicler.post(endpoint="some_endpoint", json=model))

```

В случае необходимости можно использовать устаревающий альтернативный способ создания json из модели:  

```python
model = OrderState(**data).json() 
```

## Сборка и публикация библиотеки

Рекомендуется публикация из контейнера с помощью, так уже будет установлен pdm со своими зависимостями.  

### 1. Изменение версии  

Необходимо изменить версию библиотеки на более новую, чтобы избежать конфликтов. Правила версионирования предполагают исподльзование маски версий вида X.YY.ZZZ - где:  
> X - мажорная версия, отражающая глобальные изменения, после которых нарушается обратная совместимость, как правило релизная версия начинается с 1.YY.ZZZ.
>> YY - минорная версия, отражает значительные изменения в рамках одной мажорной версии, может значительно отличаться друг от друга, однако соблюдается принцип обратной совместимости.
>>> ZZZ - микро версия, отражает любые другие изменения или варианты сборки.

Изменение версии производится в данной документации и в файле [pyproject.toml](pyproject.toml).  
E.G.:  

```toml
version = "0.9.2"
```

### 2. Сборка

Сборка библиотеки осуществляется с помощью [PDM](https://pdm-project.org/en/latest/)

```sh
pdm build
```

### 3. Релиз библиотеки в PyPi

### 3.1 Генерация API Token

Для публикации библиотек в [PyPi](https://pypi.org/) необходимо создать аккаунт. После авторизации, проверки email и подключения 2FA, нужно создать API Token он необходим для публикации библиотек с помощью Twine/PDM или других менеджеров. Для публикации из репозитория необходимо, чтобы он был доступен из интернета, инструкция [здесь](https://pypi.org/manage/account/publishing/).  

Создать API Token можно [здесь](https://pypi.org/manage/account/), внизу в соотвествующей графе.  
> Внимание, токен можно посмотреть **ТОЛЬКО** при его создании, далее он будет скрыт

### 3.2 Релиз

Релиз осуществляется с помощью [pdm-publish](https://github.com/branchvincent/pdm-publish).  

```sh
pdm publish --password token
```

Далее по [инструкции](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-your-project-to-pypi) для публикации необходимо использовать API Token, скопируйте его полностью.  

### Тестовый релиз в test.pypi.org

Нужно повторить такой же путь регистрации как на PyPi, только на [TestPyPi](https://test.pypi.org/).  

```sh
pdm publish -r testpypi -u __token__ -P <TEST_API_TOKEN>
```
