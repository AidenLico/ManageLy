### TESTING HOLIDAY BOOKING ###
import warnings

def test_sheets_manager_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/sheets")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Request Timesheet" in responseData

def test_sheets_employee_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    response = client.get("/portal/sheets")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Request Paysheet" in responseData

def test_sheets_owner_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "owner"

    response = client.get("/portal/sheets")

    assert response.status_code == 302
    assert response.headers["Location"] == "/portal"

def test_sheets_managerrequesttimesheet(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    timesheetRequest = {
        "action": "download",
        "employee": "1",
        "month": "1"
    }
    response = client.post("/portal/sheets", data=timesheetRequest, follow_redirects=True)

    assert response.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in response.content_type
    assert "attachment" in response.headers.get("Content-Disposition", "")

def test_sheets_employeerequestpaysheet(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    paysheetRequest = {
        "action": "download",
        "month": "1"
    }
    response = client.post("/portal/sheets", data=paysheetRequest, follow_redirects=True)

    assert response.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in response.content_type
    assert "attachment" in response.headers.get("Content-Disposition", "")