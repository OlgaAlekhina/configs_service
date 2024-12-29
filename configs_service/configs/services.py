from typing import Optional, List, Dict
import requests
from django.conf import settings
from requests import HTTPError, RequestException


registry_url = settings.REGISTRY_URL
registry_port = settings.REGISTRY_PORT


def get_configs(project_id: str, account_id: Optional[str], configs: List[str]) -> Optional[Dict]:
    """
    Получить из реестра значения конфигов типа config для данных project_id и account_id
    """
    object_types = ','.join(configs)
    base_url = f"{registry_url}:{registry_port}/api/configs"
    if account_id:
        url = f"{base_url}/?project_id={project_id}&account_id={account_id}&object_type={object_types}"
    else:
        url = f"{base_url}/?project_id={project_id}&object_type={object_types}"
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()
        results = {}
        for result in response_data:
            results.update({
                result.get('object_type'): result.get('data')
            })
        return {'data': results}
    return None


def create_config(config_data):
    url = f"{registry_url}:{registry_port}/api/config/"
    try:
        response = requests.post(url, json=config_data)
        response.raise_for_status()
        response_data = response.json()
        result_data = {"detail": {
            "code": "OK",
            "message": "Конфиги добавлены в реестр."
        },
            "data": response_data
        }
        return result_data, 201

    except HTTPError as http_err:
        result_data = {
            "detail": {
                "code": "BAD_REQUEST",
                "message": "Идентификатор такого типа уже существует"
            }
        }
        return result_data, response.status_code

    except RequestException as err:
        result_data = {
            "detail": {
                "code": f"REQUEST_ERROR - {response.status_code}",
                "message": str(err)
            }
        }
        return result_data, response.status_code
