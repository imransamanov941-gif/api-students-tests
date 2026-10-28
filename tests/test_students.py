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


@allure.title("GET /student/{id} возвращает данные студента")
def test_get_student_by_id(client, student):
    response = client.retry(client.get_student, student["id"])

    with allure.step("Проверить код ответа и статус"):
        assert response.status_code == 200
        assert response.json()["status"] == 1

    with allure.step("Проверить, что данные совпадают с созданными"):
        got = response.json()["student"]
        assert got["id"] == student["id"]
        assert got["name"] == student["data"]["name"]
        assert got["email"] == student["data"]["email"]
        assert got["phone_no"] == student["data"]["phone_no"]
        assert got["gender"] == student["data"]["gender"]
        assert got["status"] == student["data"]["status"]


@allure.title("GET несуществующего студента возвращает status 0")
def test_get_nonexistent_student(client):
    response = client.get_student(999999)

    with allure.step("Проверить, что сервер сообщает об ошибке"):
        body = response.json()
        assert body["status"] == 0
        assert body["message"] == "Student not found"


@allure.title("BUG: созданный студент стабильно доступен по id")
def test_created_student_is_stable(client, student):
    with allure.step("Запросить студента по id 10 раз подряд"):
        statuses = [client.get_student(student["id"]).json()["status"]
                    for _ in range(10)]

    with allure.step("Проверить, что студент найден во всех запросах"):
        assert all(s == 1 for s in statuses), f"Найден не всегда, статусы: {statuses}"


@allure.title("POST /student создаёт студента")
def test_create_student(client, student_data):
    response = client.create_student(student_data)
    student_id = None
    try:
        with allure.step("Проверить код ответа и сообщение"):
            body = response.json()
            assert response.status_code == 200
            assert body["status"] == 1
            assert body["message"] == "Student created successfully"
            student_id = body["student"]["id"]

        with allure.step("Проверить, что вернулись отправленные данные"):
            created = body["student"]
            assert isinstance(created["id"], int)
            assert created["name"] == student_data["name"]
            assert created["email"] == student_data["email"]
            assert created["phone_no"] == student_data["phone_no"]
            assert created["gender"] == student_data["gender"]
            assert created["status"] == student_data["status"]
    finally:
        if student_id is not None:
            client.delete_everywhere(student_id)


@allure.title("PUT /student/{id} обновляет данные студента")
def test_update_student(client, student):
    new_data = {
        "name": "Updated Name",
        "email": f"updated_{student['id']}@example.com",
        "gender": "female",
        "status": 0,
    }
    response = client.retry(client.update_student, student["id"], new_data)

    with allure.step("Проверить ответ на обновление"):
        body = response.json()
        assert response.status_code == 200
        assert body["status"] == 1
        assert body["message"] == "Student updated successfully"

    with allure.step("Проверить, что в ответе новые данные, а телефон прежний"):
        updated = body["student"]
        assert updated["name"] == new_data["name"]
        assert updated["email"] == new_data["email"]
        assert updated["gender"] == new_data["gender"]
        assert int(updated["status"]) == new_data["status"]
        assert updated["phone_no"] == student["data"]["phone_no"]
        

@allure.title("BUG: PUT возвращает status студента строкой, а не числом")
def test_update_returns_status_as_integer(client, student):
    new_data = {
        "name": "Updated Name",
        "email": f"updated_{student['id']}@example.com",
        "gender": "male",
        "status": 1,
    }
    response = client.retry(client.update_student, student["id"], new_data)

    with allure.step("Проверить, что status в ответе имеет тип int"):
        status = response.json()["student"]["status"]
        assert isinstance(status, int), f"status вернулся как {type(status).__name__}: {status!r}"


@allure.title("DELETE /student/{id} удаляет студента")
def test_delete_student(client, student):
    responses = client.delete_everywhere(student["id"])

    with allure.step("Проверить, что хотя бы один DELETE вернул успех"):
        bodies = [r.json() for r in responses]
        assert any(b["status"] == 1 and b["message"] == "Student deleted successfully"
                   for b in bodies)

    with allure.step("Проверить, что студент больше не находится"):
        for _ in range(10):
            body = client.get_student(student["id"]).json()
            assert body["status"] == 0


@allure.title("BUG: DELETE несуществующего студента не должен возвращать успех")
def test_delete_nonexistent_student(client):
    response = client.delete_student(999999)

    with allure.step("Проверить, что сервер сообщает об ошибке"):
        body = response.json()
        assert body["status"] == 0