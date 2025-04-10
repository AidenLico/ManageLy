### TESTING HOLIDAY BOOKING ###
import warnings
import datetime

def test_calendar_manager_render(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/calendar")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Add Event" in responseData

def test_calendar_employee_render(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    response = client.get("/portal/calendar")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Add Event" not in responseData


def test_calendar_owner_render(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "owner"

    response = client.get("/portal/calendar")

    assert response.status_code == 302
    assert response.headers["Location"] == "/portal"

def test_calendar_previous(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    today = (datetime.datetime.now()).date()
    newStartDate = today - datetime.timedelta(days=3)
    previousRequest = {
        "action": "previous",
        "currentdate": datetime.datetime.strftime(today, "%Y-%m-%d")
    }

    response = client.post("/portal/calendar", data=previousRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert f"{datetime.datetime.strftime(newStartDate, "%Y-%m-%d")}" in responseData


def test_calendar_next(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    today = (datetime.datetime.now()).date()
    newStartDate = today + datetime.timedelta(days=5)
    nextRequest = {
        "action": "next",
        "currentdate": datetime.datetime.strftime(today, "%Y-%m-%d")
    }

    response = client.post("/portal/calendar", data=nextRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert f"{datetime.datetime.strftime(newStartDate, "%Y-%m-%d")}" in responseData


def test_calendar_manageraddevent(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    today = (datetime.datetime.now()).date()
    addRequest = {
        "action": "addEvent",
        "eventName": "TEST EVENT 12 1",
        "startdate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "enddate": datetime.datetime.strftime(today, "%Y-%m-%d")
    }

    response = client.post("/portal/calendar", data=addRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "TEST EVENT 12 1" in responseData


def test_calendar_manageraddevent_invalid(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    addRequest = {
        "action": "addEvent",
        "eventName": "",
        "startdate": "",
        "enddate": ""
    }

    response = client.post("/portal/calendar", data=addRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Please Fill All Event Fields!" in responseData


def test_calendar_managerdeleteevent(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    deleteRequest = {
        "action": "deleteEvent",
        "eventID": "1"
    }

    response = client.post("/portal/calendar", data=deleteRequest, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "TEST EVENT 12 1" not in responseData