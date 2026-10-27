import logging
import re
import uuid
from pathlib import Path

import allure
import pytest

from api.client import StudentsClient

LOG_DIR = Path("logs")


@pytest.fixture(autouse=True)
def test_log(request):
    LOG_DIR.mkdir(exist_ok=True)
    name = re.sub(r"[^\w\-]+", "_", request.node.name)
    log_path = LOG_DIR / f"{name}.log"

    handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger = logging.getLogger("api")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    yield

    logger.removeHandler(handler)
    handler.close()
    allure.attach.file(str(log_path), name="Лог теста",
                       attachment_type=allure.attachment_type.TEXT)


@pytest.fixture
def client():
    return StudentsClient()


@pytest.fixture
def student_data():
    suffix = uuid.uuid4().hex[:8]
    return {
        "name": f"Test {suffix}",
        "email": f"test_{suffix}@example.com",
        "phone_no": "+79990001122",
        "gender": "male",
        "status": 1,
    }


@pytest.fixture
def student(client, student_data):
    with allure.step("Подготовка: создать студента"):
        response = client.create_student(student_data)
        student_id = response.json()["student"]["id"]
    yield {"id": student_id, "data": student_data}
    with allure.step("Очистка: удалить студента"):
        client.delete_student(student_id)