import requests
import json

def get_device_attributes(token, url, device_id):
    """
    Возвращает структуру вида:
    {
      "client": [...],
      "shared": [...],
      "server": [...]
    }
    """
    headers = {"X-Authorization": f"Bearer {token}"}
    resp = requests.get(f"{url}/api/plugins/telemetry/DEVICE/{device_id}/values/attributes", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(f"Атрибуты для {device_id}: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return data
    else:
        print(f"Ошибка получения атрибутов для устройства {device_id}: {resp.text}")
        return {}

def upload_attributes(token, url, device_id, attributes_by_scope):
    """
    Принимает атрибуты по каждому scope и заливает в PE в тот же scope.
    Пример структуры attributes_by_scope:
    {
      "client": [ { "key": "...", "value": ... }, ... ],
      "shared": [ ... ],
      "server": [ ... ]
    }
    """
    headers = {
        "X-Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # Пробегаемся по всем scope (client/shared/server)
    for scope_name, attr_list in attributes_by_scope.items():
        if not attr_list:
            continue  # Пустой список — пропускаем
        # Преобразуем список в dict {ключ: значение}
        formatted = {attr["key"]: attr["value"] for attr in attr_list if "key" in attr and "value" in attr}

        # В ThingsBoard API scope нужно передавать в верхнем регистре + "_SCOPE"
        scope_str = scope_name.upper() + "_SCOPE"

        resp = requests.post(
            f"{url}/api/plugins/telemetry/DEVICE/{device_id}/attributes/{scope_str}",
            headers=headers,
            json=formatted
        )
        if resp.status_code == 200:
            print(f"✓ Атрибуты ({scope_str}) для {device_id} успешно загружены")
        else:
            print(f"✗ Ошибка загрузки атрибутов ({scope_str}) для {device_id}: {resp.text}")
