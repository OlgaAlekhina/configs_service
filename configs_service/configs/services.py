from typing import Optional, List, Dict
import requests
from requests import HTTPError, RequestException


def get_configs(project_id: str, account_id: Optional[str], configs: List[str]) -> Optional[Dict]:
    """
    Получить из реестра значения конфигов типа config для данных project_id и account_id
    """
    object_types = ','.join(configs)
    beginning_url = "http://127.0.0.1:8002/api/configs"
    if account_id:
        url = f"{beginning_url}/?project_id={project_id}&account_id={account_id}&object_type={object_types}"
    else:
        url = f"{beginning_url}/?project_id={project_id}&object_type={object_types}"
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
    url = "http://127.0.0.1:8002/api/config/"
    try:
        response = requests.post(url, json=config_data)
        response.raise_for_status()
        response_data = response.json()
        result_data = {"detail": {
            "code": "OK",
            "message": "Идентификатор успешно создан."
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
