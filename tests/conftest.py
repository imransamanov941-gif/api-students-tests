import logging
import re
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