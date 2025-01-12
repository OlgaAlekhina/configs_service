from typing import Optional, List
import requests
from django.conf import settings
from requests import HTTPError, RequestException


registry_url = settings.REGISTRY_URL
registry_port = settings.REGISTRY_PORT


def get_configs(project_id: str, account_id: Optional[str], configs: List[str]) -> tuple[dict, int]:
    """ Получить из реестра значения конфигов типа config для данных project_id и account_id """
    object_types = ','.join(configs)
    base_url = f"{registry_url}:{registry_port}/api/configs"
    if account_id:
        url = f"{base_url}/?project_id={project_id}&account_id={account_id}&object_type={object_types}"
    else:
        url = f"{base_url}/?project_id={project_id}&object_type={object_types}"
    try:
        # делаем запрос в апи реестра конфигов
        response = requests.get(url)
        response.raise_for_status()
        response_data = response.json()
        results = {}
        for result in response_data:
            results.update({
                result.get('object_type'): result.get('data')
            })
        return {'data': results}, 200
    except HTTPError as err:
        return {'code': 'HTTP_ERROR', 'message': str(err)}, err.response.status_code
    except RequestException as err:
        return {'code': 'REQUEST_ERROR', 'message': str(err)}, err.response.status_code if err.response else 500


def create_config(config_data: dict) -> tuple[dict, int]:
    url = f"{registry_url}:{registry_port}/api/config/"
    try:
        # посылаем данные в апи реестра конфигов
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
    except HTTPError as err:
        return {'detail': {'code': 'ENTITY_EXISTS', 'message': 'Идентификатор такого типа уже существует'}}, 400
    except RequestException as err:
        return {'detail': {'code': 'REQUEST_ERROR', 'message': str(err)}}, err.response.status_code if err.response else 500

