import logging

import allure
import requests

from config import BASE_URL, TIMEOUT

logger = logging.getLogger("api")


class StudentsClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        with allure.step(f"{method} {path}"):
            logger.info("REQUEST: %s %s body=%s", method, url, kwargs.get("json"))
            response = self.session.request(method, url, timeout=TIMEOUT, **kwargs)
            logger.info("RESPONSE: %s %s", response.status_code, response.text)
        return response

    def get_students(self):
        return self._request("GET", "/student")

    def get_student(self, student_id):
        return self._request("GET", f"/student/{student_id}")

    def create_student(self, data):
        return self._request("POST", "/student", json=data)

    def update_student(self, student_id, data):
        return self._request("PUT", f"/student/{student_id}", json=data)

    def delete_student(self, student_id):
        return self._request("DELETE", f"/student/{student_id}")

    def retry(self, method, *args, attempts=20):
        """Повторяет запрос, пока сервер не вернёт status 1."""
        with allure.step(f"Повторять запрос до успеха (до {attempts} раз)"):
            response = None
            for _ in range(attempts):
                response = method(*args)
                if response.json().get("status") == 1:
                    break
        return response

    def delete_everywhere(self, student_id, attempts=15):
        """Удаляет много раз, чтобы задеть все копии сервера."""
        with allure.step(f"Удалить студента {student_id} ({attempts} запросов)"):
            return [self.delete_student(student_id) for _ in range(attempts)]