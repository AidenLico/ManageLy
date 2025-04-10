# ### TESTING HOLIDAY BOOKING ###
import warnings
import datetime

def test_sales_manager_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/sales")

    assert response.status_code == 302
    assert response.headers["Location"] == "/portal"

def test_sales_employee_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    response = client.get("/portal/sales")

    assert response.status_code == 302
    assert response.headers["Location"] == "/portal"

def test_holidaybooking_owner_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "owner"

    today = datetime.datetime.now()
    currentPosition = today.weekday()
    startDay = (today - datetime.timedelta(days=currentPosition)).date()

    response = client.get("/portal/sales")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert f"Week Starting {datetime.datetime.strftime(startDay, "%Y-%m-%d")}" in responseData


def test_holidaybooking_ownerprevious(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "owner"

    today = datetime.datetime.now()
    currentPosition = today.weekday()
    startDay = (today - datetime.timedelta(days=currentPosition)).date()
    newStartDay = (startDay - datetime.timedelta(days=7))

    previousRequest = {
        "action": "previous",
        "date": datetime.datetime.strftime(startDay, "%Y-%m-%d")
    }
    response = client.post("/portal/sales", data=previousRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert f"Week Starting {datetime.datetime.strftime(newStartDay, "%Y-%m-%d")}" in responseData

def test_holidaybooking_ownernext(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "owner"

    today = datetime.datetime.now()
    currentPosition = today.weekday()
    startDay = (today - datetime.timedelta(days=currentPosition)).date()
    newStartDay = (startDay + datetime.timedelta(days=7))

    nextRequest = {
        "action": "next",
        "date": datetime.datetime.strftime(startDay, "%Y-%m-%d")
    }
    response = client.post("/portal/sales", data=nextRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert f"Week Starting {datetime.datetime.strftime(newStartDay, "%Y-%m-%d")}" in responseData