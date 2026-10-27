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


@allure.title("Созданный студент есть в общем списке")
def test_created_student_in_list(client, student):
    response = client.get_students()

    with allure.step("Найти студента по id в списке"):
        ids = [s["id"] for s in response.json()["students"]]
        assert student["id"] in ids


@allure.title("GET /student/{id} возвращает данные студента")
def test_get_student_by_id(client, student):
    response = client.get_student(student["id"])

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

        with allure.step("Проверить, что в ответе вернулись отправленные данные"):
            created = body["student"]
            assert isinstance(created["id"], int)
            assert created["name"] == student_data["name"]
            assert created["email"] == student_data["email"]
            assert created["phone_no"] == student_data["phone_no"]
            assert created["gender"] == student_data["gender"]
            assert created["status"] == student_data["status"]
    finally:
        if student_id is not None:
            with allure.step("Очистка: удалить студента"):
                client.delete_student(student_id)