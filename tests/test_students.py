import allure


@allure.title("GET /student возвращает список студентов")
def test_get_students(client):
    response = client.get_students()

    with allure.step("Проверить код ответа 200"):
        assert response.status_code == 200

    with allure.step("Проверить, что в ответе есть список students"):
        body = response.json()
        assert body["status"] == 1
        assert isinstance(body["students"], list)