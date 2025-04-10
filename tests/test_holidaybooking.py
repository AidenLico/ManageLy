### TESTING HOLIDAY BOOKING ###
import warnings
import datetime

def test_holidaybooking_manager_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/holidaybooking")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Add Holiday" in responseData
    assert "Holiday Requests" in responseData

def test_holidaybooking_employee_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    response = client.get("/portal/holidaybooking")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Add Holiday" not in responseData
    assert "Holiday Requests" not in responseData

def test_holidaybooking_owner_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "owner"

    response = client.get("/portal/holidaybooking")

    assert response.status_code == 302
    assert response.headers["Location"] == "/portal"


def test_holidaybooking_employeemakerequest(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    today = datetime.datetime.now().date()
    requestForm = {
        "action": "submitRequest",
        "startdate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "enddate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "reason": "TEST REQUEST 123 1"
    }
    response = client.post("/portal/holidaybooking", data=requestForm, follow_redirects=True)

    assert response.status_code == 200

    requestForm = {
        "action": "submitRequest",
        "startdate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "enddate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "reason": "TEST REQUEST 123 2"
    }
    response = client.post("/portal/holidaybooking", data=requestForm, follow_redirects=True)

    assert response.status_code == 200

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/holidaybooking")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Employee 1: Holiday Request" in responseData
    assert "Reason: TEST REQUEST 123 1" in responseData
    assert "Reason: TEST REQUEST 123 2" in responseData


def test_holidaybooking_employeemakerequest_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    today = datetime.datetime.now().date()
    requestForm = {
        "action": "submitRequest",
        "startdate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "enddate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "reason": ""
    }
    response = client.post("/portal/holidaybooking", data=requestForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Please Fill All Fields!" in responseData

    requestForm = {
        "action": "submitRequest",
        "startdate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "enddate": "2025-01-01",
        "reason": "TEST REQUEST 123 3"
    }
    response = client.post("/portal/holidaybooking", data=requestForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "End date must be equal or after start date!" in responseData

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/holidaybooking")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Reason: TEST REQUEST 123 3" not in responseData

def test_holidaybooking_manageracceptrequest(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    acceptForm = {
        "action": "approveRequest",
        "requestID": "1"
    }
    response = client.post("/portal/holidaybooking", data=acceptForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Reason: TEST REQUEST 123 1" not in responseData

def test_holidaybooking_managerdenyrequest(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    denyForm = {
        "action": "denyRequest",
        "requestID": "2"
    }
    response = client.post("/portal/holidaybooking", data=denyForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Reason: TEST REQUEST 123 2" not in responseData


def test_holidaybooking_manageraddholiday(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"
    today = datetime.datetime.now().date()

    addHolidayForm = {
        "action": "addHoliday",
        "employee": "1",
        "addStartdate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "addEnddate": datetime.datetime.strftime(today, "%Y-%m-%d")
    }

    response = client.post("/portal/holidaybooking", data=addHolidayForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Please Fill All Fields!" not in responseData
    assert "End date must be equal or after start date!" not in responseData

def test_holidaybooking_manageraddholiday_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"
    today = datetime.datetime.now().date()

    addHolidayForm = {
        "action": "addHoliday",
        "employee": "",
        "addStartdate": "",
        "addEnddate": ""
    }

    response = client.post("/portal/holidaybooking", data=addHolidayForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Please Fill All Fields!" in responseData

    addHolidayForm = {
        "action": "addHoliday",
        "employee": "1",
        "addStartdate": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "addEnddate": "2025-01-01"
    }

    response = client.post("/portal/holidaybooking", data=addHolidayForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "End date must be equal or after start date!" in responseData