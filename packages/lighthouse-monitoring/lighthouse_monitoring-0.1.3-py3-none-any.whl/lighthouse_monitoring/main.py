import inspect
import logging
import requests
import asyncio
from functools import wraps
from lighthouse_monitoring.schemas import (
    MonitoringInputRequest,
    MonitoringOutputRequest,
    MonitoringInputResponse,
    MonitoringOutputResponse,
)


class LightHouseHandler:
    def __init__(
        self,
        user_id_param_name: str,
        input_param_name: str,
        api_key: str,
        address: str,
        reject_msg: str = "В данный момент я не могу ответить на ваш запрос.",
        logger: logging.Logger = None,
    ):
        self.user_id_param_name = user_id_param_name
        self.input_param_name = input_param_name
        self.headers = {"api_key": api_key}
        self.address = address
        self.reject_msg = reject_msg
        self.logger = logger if logger is not None else logging.getLogger(__name__)

    def __call__(self, func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            user_id = kwargs.get(self.user_id_param_name, None)
            user_input = kwargs.get(self.input_param_name, None)
            output_response = None

            input_request = MonitoringInputRequest(
                user_id=user_id, input_text=user_input
            )

            input_response = self.send_data(
                endpoint=f"{self.address}/monitoring/input",
                json=input_request.model_dump(),
            )
            input_response_data = MonitoringInputResponse(**input_response)

            result = func(*args, **kwargs)

            if inspect.iscoroutinefunction(func):
                result = await result

            output_request = MonitoringOutputRequest(
                request_id=input_response_data.request_id, output_text=result
            )

            output_response = self.send_data(
                endpoint=f"{self.address}/monitoring/output",
                json=output_request.model_dump(),
            )

            output_response_data = MonitoringOutputResponse(**output_response)

            if output_response_data and output_response_data.reject_flg == True:
                return self.reject_msg

            return result

        return async_wrapper

    def send_data(self, endpoint: str, json: str):
        try:
            response = requests.post(endpoint, json=json, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.debug(f"Ошибка при отправке данных: {e}")
            return None

    async def send_data_async(self, endpoint: str, json: str):
        """Асинхронная отправка данных на сервер (использует requests в отдельном потоке)."""
        loop = asyncio.get_event_loop()
        try:
            response = await loop.run_in_executor(
                None, lambda: requests.post(endpoint, json=json, headers=self.headers)
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.debug(f"Ошибка при отправке данных: {e}")
            return None
