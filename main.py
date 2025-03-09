# import requests
# import json
#
# # --- Настройки ThingsBoard CE (Community Edition)
# CE_URL = "https://demo.thingsboard.io"
# CE_USERNAME = "jibil15557@bnsteps.com"
# CE_PASSWORD = "jibil15557@bnsteps.com"
#
# # --- Настройки ThingsBoard PE (Professional Edition)
# PE_URL = "https://thingsboard.cloud"
# PE_USERNAME = "remlavikni@gufum.com"
# PE_PASSWORD = "remlavikni@gufum.com"
#
# # Функция получения JWT-токена
# def get_jwt_token(url, username, password):
#     headers = {"Content-Type": "application/json"}
#     resp = requests.post(f"{url}/api/auth/login", headers=headers,
#                          json={"username": username, "password": password})
#     if resp.status_code == 200:
#         token = resp.json().get("token")
#         print(f"Получен токен для {url}")
#         return token
#     else:
#         print(f"Ошибка аутентификации ({url}): {resp.text}")
#         return None
#
# # Получаем токены для CE и PE
# ce_token = get_jwt_token(CE_URL, CE_USERNAME, CE_PASSWORD)
# pe_token = get_jwt_token(PE_URL, PE_USERNAME, PE_PASSWORD)
# if not ce_token or not pe_token:
#     print("Не удалось получить токены. Проверьте логины и пароли.")
#     exit()
#
# # Функция для получения списка устройств из CE
# def get_devices(token, url):
#     headers = {"X-Authorization": f"Bearer {token}"}
#     resp = requests.get(f"{url}/api/tenant/devices?pageSize=1000&page=0", headers=headers)
#     if resp.status_code == 200:
#         devices = resp.json().get("data", [])
#         print(f"Получено {len(devices)} устройств из {url}")
#         return devices
#     else:
#         print(f"Ошибка получения устройств: {resp.text}")
#         return []
#
# # Функция создания устройства в PE
# def create_device(token, url, device):
#     headers = {"X-Authorization": f"Bearer {token}", "Content-Type": "application/json"}
#     data = {"name": device["name"], "type": device["type"]}
#     resp = requests.post(f"{url}/api/device", headers=headers, json=data)
#     if resp.status_code == 200:
#         device_id = resp.json().get("id", {}).get("id")
#         print(f"Устройство {device['name']} успешно создано в PE (id: {device_id})")
#         return device_id
#     else:
#         print(f"Ошибка создания устройства {device['name']}: {resp.text}")
#         return None
#
# # Функция получения атрибутов устройства из CE
# def get_device_attributes(token, url, device_id):
#     headers = {"X-Authorization": f"Bearer {token}"}
#     resp = requests.get(f"{url}/api/plugins/telemetry/DEVICE/{device_id}/values/attributes", headers=headers)
#     if resp.status_code == 200:
#         data = resp.json()
#         print(f"Атрибуты для {device_id}: {json.dumps(data, indent=2, ensure_ascii=False)}")
#         # Если CE возвращает список, считаем их принадлежащими Shared.
#         if isinstance(data, list):
#             return {"shared": data}
#         elif isinstance(data, dict):
#             return data
#         else:
#             print("Неизвестный формат атрибутов:", type(data))
#             return {}
#     else:
#         print(f"Ошибка получения атрибутов для устройства {device_id}: {resp.text}")
#         return {}
#
# # Функция загрузки атрибутов в PE по scope
# def upload_attributes_by_scope(token, url, device_id, attributes_dict):
#     headers = {"X-Authorization": f"Bearer {token}", "Content-Type": "application/json"}
#     for scope in ["client", "shared", "server"]:
#         attr_list = attributes_dict.get(scope, [])
#         if not attr_list:
#             print(f"Для {device_id} в scope {scope} атрибутов нет.")
#             continue
#         data = {}
#         for attr in attr_list:
#             key = attr.get("key")
#             value = attr.get("value")
#             # Если scope server и ключ равен "active", пропускаем его (автоматически задаётся)
#             if scope == "server" and key == "active":
#                 continue
#             if key is not None and value is not None:
#                 data[key] = value
#         scope_endpoint = scope.upper() + "_SCOPE"
#         resp = requests.post(f"{url}/api/plugins/telemetry/DEVICE/{device_id}/attributes/{scope_endpoint}",
#                              headers=headers, json=data)
#         if resp.status_code == 200:
#             print(f"✓ Атрибуты ({scope_endpoint}) для {device_id} успешно загружены")
#         else:
#             print(f"✗ Ошибка загрузки атрибутов ({scope_endpoint}) для {device_id}: {resp.text}")
#
# # Функция получения телеметрии из CE
# def get_device_telemetry(token, url, device_id):
#     headers = {"X-Authorization": f"Bearer {token}"}
#     resp = requests.get(f"{url}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries", headers=headers)
#     if resp.status_code == 200:
#         telemetry = resp.json()
#         print(f"Телеметрия для {device_id}: {json.dumps(telemetry, indent=2, ensure_ascii=False)}")
#         return telemetry
#     else:
#         print(f"Ошибка получения телеметрии для {device_id}: {resp.text}")
#         return {}
#
# # Функция, которая для каждого ключа выбирает последнюю точку (наибольший ts)
# def extract_latest_telemetry(telemetry):
#     latest = {}
#     for key, points in telemetry.items():
#         if points:
#             point = max(points, key=lambda x: x.get("ts", 0))
#             try:
#                 value = float(point.get("value"))
#             except (ValueError, TypeError):
#                 value = point.get("value")
#             latest[key] = value
#     return latest
#
# # Функция получения учётных данных устройства из PE
# def get_device_credentials(token, url, device_id):
#     headers = {"X-Authorization": f"Bearer {token}"}
#     resp = requests.get(f"{url}/api/device/{device_id}/credentials", headers=headers)
#     if resp.status_code == 200:
#         creds = resp.json()
#         print(f"Учётные данные для {device_id}: {json.dumps(creds, indent=2, ensure_ascii=False)}")
#         return creds
#     else:
#         print(f"Ошибка получения учётных данных для {device_id}: {resp.text}")
#         return None
#
# # Функция отправки телеметрии через устройство API PE
# def send_device_telemetry(access_token, url, telemetry_data):
#     headers = {"Content-Type": "application/json"}
#     endpoint = f"{url}/api/v1/{access_token}/telemetry"
#     resp = requests.post(endpoint, headers=headers, json=telemetry_data)
#     if resp.status_code == 200:
#         print("Телеметрия успешно отправлена через устройство API")
#     else:
#         print(f"Ошибка отправки телеметрии через устройство API: {resp.text}")
#
# # ------------------------------------
# # Основной блок переноса
# # ------------------------------------
# ce_devices = get_devices(ce_token, CE_URL)
# print(f"Найдено {len(ce_devices)} устройств в CE.")
#
# for device in ce_devices:
#     ce_device_id = device["id"]["id"]
#     pe_device_id = create_device(pe_token, PE_URL, device)
#     if not pe_device_id:
#         continue
#
#     # 1. Перенос атрибутов: получаем атрибуты из CE и загружаем их в PE по scope
#     ce_attrs = get_device_attributes(ce_token, CE_URL, ce_device_id)
#     if ce_attrs:
#         upload_attributes_by_scope(pe_token, PE_URL, pe_device_id, ce_attrs)
#
#     # 2. Перенос телеметрии:
#     ce_telemetry = get_device_telemetry(ce_token, CE_URL, ce_device_id)
#     if ce_telemetry:
#         # Из телеметрии выбираем для каждого ключа последнюю точку,
#         # чтобы получить простой словарь (например, {"temperature":25})
#         latest_telemetry = extract_latest_telemetry(ce_telemetry)
#         # Получаем учётные данные нового устройства из PE
#         pe_creds = get_device_credentials(pe_token, PE_URL, pe_device_id)
#         if pe_creds and pe_creds.get("credentialsId"):
#             access_token = pe_creds["credentialsId"]
#             send_device_telemetry(access_token, PE_URL, latest_telemetry)
#         else:
#             print(f"Учётные данные для устройства {pe_device_id} не получены, телеметрия не отправлена.")
#
# print("Перенос устройств, атрибутов и телеметрии завершён!")


import requests
import json

# --- Настройки ThingsBoard CE (Community Edition)
CE_URL = "https://demo.thingsboard.io"
CE_USERNAME = "jibil15557@bnsteps.com"
CE_PASSWORD = "jibil15557@bnsteps.com"

# --- Настройки ThingsBoard PE (Professional Edition)
PE_URL = "https://thingsboard.cloud"
PE_USERNAME = "remlavikni@gufum.com"
PE_PASSWORD = "remlavikni@gufum.com"

def get_jwt_token(url, username, password):
    headers = {"Content-Type": "application/json"}
    resp = requests.post(f"{url}/api/auth/login", headers=headers,
                         json={"username": username, "password": password})
    if resp.status_code == 200:
        token = resp.json().get("token")
        print(f"Получен токен для {url}")
        return token
    else:
        print(f"Ошибка аутентификации ({url}): {resp.text}")
        return None

ce_token = get_jwt_token(CE_URL, CE_USERNAME, CE_PASSWORD)
pe_token = get_jwt_token(PE_URL, PE_USERNAME, PE_PASSWORD)
if not ce_token or not pe_token:
    print("Не удалось получить токены. Проверьте логины и пароли.")
    exit()

def get_devices(token, url):
    headers = {"X-Authorization": f"Bearer {token}"}
    resp = requests.get(f"{url}/api/tenant/devices?pageSize=1000&page=0", headers=headers)
    if resp.status_code == 200:
        devices = resp.json().get("data", [])
        print(f"Получено {len(devices)} устройств из {url}")
        return devices
    else:
        print(f"Ошибка получения устройств: {resp.text}")
        return []

def create_device(token, url, device):
    headers = {"X-Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"name": device["name"], "type": device["type"]}
    resp = requests.post(f"{url}/api/device", headers=headers, json=data)
    if resp.status_code == 200:
        device_id = resp.json().get("id", {}).get("id")
        print(f"Устройство {device['name']} успешно создано в PE (id: {device_id})")
        return device_id
    else:
        print(f"Ошибка создания устройства {device['name']}: {resp.text}")
        return None

def get_shared_attributes(token, url, device_id):
    """
    Явно запрашиваем Shared-атрибуты из CE:
      GET /api/plugins/telemetry/DEVICE/{device_id}/values/attributes?scope=SHARED_SCOPE
    Ожидаем список вида:
      [ { "lastUpdateTs":..., "key":"...", "value":... }, ... ]
    """
    headers = {"X-Authorization": f"Bearer {token}"}
    endpoint = f"{url}/api/plugins/telemetry/DEVICE/{device_id}/values/attributes?scope=SHARED_SCOPE"
    resp = requests.get(endpoint, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(f"Shared атрибуты для {device_id}: {json.dumps(data, indent=2, ensure_ascii=False)}")
        if isinstance(data, list):
            return data
        else:
            return []
    else:
        print(f"Ошибка получения Shared-атрибутов для {device_id}: {resp.text}")
        return []

def upload_shared_attributes(token, url, device_id, shared_attrs):
    """
    Отправляем список Shared-атрибутов в PE.
    Фильтруем лишние ключи, если нужно (например, "active", "inactivityAlarmTime").
    """
    if not shared_attrs:
        print(f"Нет Shared атрибутов для {device_id}, пропускаем.")
        return

    # Фильтруем те ключи, которые не хотим переносить:
    # (Например, "active", "inactivityAlarmTime". Или убираем всё, кроме "qwww".)
    filtered_list = []
    for attr in shared_attrs:
        k = attr.get("key")
        v = attr.get("value")
        # Допустим, переносим все кроме "active" / "inactivityAlarmTime"
        # if k in ["active", "inactivityAlarmTime"]:
        #     continue
        # Или переносим только qwww
        # if k != "qwww":
        #     continue
        if k is not None and v is not None:
            filtered_list.append(attr)

    # Преобразуем список [{key, value}, ...] -> {key: value}
    data = {}
    for attr in filtered_list:
        data[attr["key"]] = attr["value"]

    if not data:
        print(f"После фильтрации ничего не осталось, пропускаем {device_id}.")
        return

    headers = {"X-Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    endpoint = f"{url}/api/plugins/telemetry/DEVICE/{device_id}/attributes/SHARED_SCOPE"
    resp = requests.post(endpoint, headers=headers, json=data)
    if resp.status_code == 200:
        print(f"✓ Shared атрибуты для {device_id} успешно загружены")
    else:
        print(f"✗ Ошибка загрузки Shared атрибутов для {device_id}: {resp.text}")

def get_device_telemetry(token, url, device_id):
    """
    Получаем телеметрию из CE:
      GET /api/plugins/telemetry/DEVICE/{device_id}/values/timeseries
    Возвращается словарь вида:
      { "temperature": [ {"ts":..., "value": "25"}, ... ], ... }
    """
    headers = {"X-Authorization": f"Bearer {token}"}
    endpoint = f"{url}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
    resp = requests.get(endpoint, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(f"Телеметрия для {device_id}: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return data
    else:
        print(f"Ошибка получения телеметрии для {device_id}: {resp.text}")
        return {}

def extract_latest_telemetry(telemetry):
    """
    Из каждой группы телеметрии берём последнюю точку (max ts) и формируем словарь:
      { "temperature": 25, "humidity": 50, ... }
    """
    latest = {}
    for key, points in telemetry.items():
        if points:
            point = max(points, key=lambda x: x.get("ts", 0))
            try:
                val = float(point["value"])
            except (ValueError, TypeError):
                val = point["value"]
            latest[key] = val
    return latest

def get_device_credentials(token, url, device_id):
    """
    Получаем учётные данные устройства (access token) из PE,
    чтобы отправлять телеметрию через устройство API.
    """
    headers = {"X-Authorization": f"Bearer {token}"}
    endpoint = f"{url}/api/device/{device_id}/credentials"
    resp = requests.get(endpoint, headers=headers)
    if resp.status_code == 200:
        creds = resp.json()
        print(f"Учётные данные для {device_id}: {json.dumps(creds, indent=2, ensure_ascii=False)}")
        return creds
    else:
        print(f"Ошибка получения учётных данных для {device_id}: {resp.text}")
        return None

def send_device_telemetry(access_token, url, telemetry_data):
    """
    Отправляем телеметрию через устройство API PE,
    чтобы в UI она отображалась как простое key-value (например, {"temperature":25}).
    """
    headers = {"Content-Type": "application/json"}
    endpoint = f"{url}/api/v1/{access_token}/telemetry"
    resp = requests.post(endpoint, headers=headers, json=telemetry_data)
    if resp.status_code == 200:
        print("Телеметрия успешно отправлена через устройство API")
    else:
        print(f"Ошибка отправки телеметрии через устройство API: {resp.text}")

# ------------------------------------
# Основной блок переноса
# ------------------------------------
ce_devices = get_devices(ce_token, CE_URL)
print(f"Найдено {len(ce_devices)} устройств в CE.")

for device in ce_devices:
    ce_device_id = device["id"]["id"]
    pe_device_id = create_device(pe_token, PE_URL, device)
    if not pe_device_id:
        continue

    # 1. Получаем из CE только Shared атрибуты, фильтруем и заливаем в PE
    ce_shared = get_shared_attributes(ce_token, CE_URL, ce_device_id)
    if ce_shared:
        upload_shared_attributes(pe_token, PE_URL, pe_device_id, ce_shared)

    # 2. Получаем телеметрию из CE, берём последнее значение каждого ключа и отправляем через устройство API
    ce_telemetry = get_device_telemetry(ce_token, CE_URL, ce_device_id)
    if ce_telemetry:
        latest_data = extract_latest_telemetry(ce_telemetry)
        pe_creds = get_device_credentials(pe_token, PE_URL, pe_device_id)
        if pe_creds and pe_creds.get("credentialsId"):
            access_token = pe_creds["credentialsId"]
            send_device_telemetry(access_token, PE_URL, latest_data)
        else:
            print(f"Учётные данные для {pe_device_id} не получены, телеметрия не отправлена.")

print("Перенос устройств, атрибутов и телеметрии завершён!")

