### TESTING HOLIDAY BOOKING ###
import warnings

def test_stock_manager_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/stock")

    assert response.status_code == 200

def test_stock_employee_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    response = client.get("/portal/stock")

    assert response.status_code == 302
    assert response.headers["Location"] == "/portal"


def test_stock_owner_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "owner"

    response = client.get("/portal/stock")

    assert response.status_code == 302
    assert response.headers["Location"] == "/portal"


def test_stock_managercreatestock(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    createRequest = {
        "action": "createStock",
        "name": "TEST STOCK 12",
        "amount": "10",
        "date": "2025-01-01",
        "minAmount": "5"
    }
    response = client.post("/portal/stock", data=createRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "TEST STOCK 12: 10 <br> Date of Perish: 2025-01-01" in responseData


def test_stock_managercreatestock_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    createRequest = {
        "action": "createStock",
        "name": "",
        "amount": "",
        "date": "",
        "minAmount": ""
    }
    response = client.post("/portal/stock", data=createRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Please Fill All Fields!" in responseData

    createRequest = {
        "action": "createStock",
        "name": "TEST 13",
        "amount": "0",
        "date": "2025-01-01",
        "minAmount": "-10"
    }
    response = client.post("/portal/stock", data=createRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Amounts Should Be Greater than 0!" in responseData


def test_stock_managerincreasestock(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    increaseRequest = {
        "action": "increase",
        "stockID": "5",
        "currentAmount": "10",
        "value": "5"
    }
    response = client.post("/portal/stock", data=increaseRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)
    assert "TEST STOCK 12: 15 <br> Date of Perish: 2025-01-01" in responseData

def test_stock_managerincreasestock_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    increaseRequest = {
        "action": "increase",
        "stockID": "5",
        "currentAmount": "15",
        "value": "-10"
    }
    response = client.post("/portal/stock", data=increaseRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)
    assert "Increase Amount Should Be Greater Than 0!" in responseData


def test_stock_managerdecreasestock(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    decreaseRequest = {
        "action": "decrease",
        "stockID": "5",
        "currentAmount": "15",
        "value": "11"
    }
    response = client.post("/portal/stock", data=decreaseRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "TEST STOCK 12: 4 <br> Date of Perish: 2025-01-01" in responseData

def test_stock_managerdecreasestock_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    decreaseRequest = {
        "action": "decrease",
        "stockID": "5",
        "currentAmount": "10",
        "value": "-10"
    }
    response = client.post("/portal/stock", data=decreaseRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Decrease Amount Should Be Greater Than 0!" in responseData


def test_stock_alertCreated(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/stock")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "TEST STOCK 12 Dropped Below Minimum Amount (5)" in responseData

def test_stock_managerdeletestock(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    deleteRequest = {
        "action": "delete",
        "stockID": "5"
    }

    response = client.post("/portal/stock", data=deleteRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "TEST STOCK 12: 4 <br> Date of Perish: 2025-01-01" not in responseData
