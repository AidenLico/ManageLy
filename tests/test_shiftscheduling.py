### TESTING SHIFT SCHEDULING ###
import warnings
import datetime

def test_shiftscheduling_manager_render(client):
    # Testing manager shift scheduling page renders successfully #

    with client.session_transaction() as session:
        session["UserID"] = 2
        session["UserType"] = "manager"


    response = client.get("/portal/shiftscheduling")


    assert response.status_code == 200


    responseData = response.get_data(as_text=True)

    assert "Manual Add Shift" in responseData
    assert "Shift Template" in responseData
    assert "Add Shift" in responseData
    assert "Delete Shift" in responseData
    assert "Automatic Schedule Start" in responseData

def test_shiftscheduling_manager_render_as_employee(client):
    # Testing when employee loads shift scheduling, they do not receive #
    # manager speciic page #

    warnings.filterwarnings("ignore", category=DeprecationWarning)


    with client.session_transaction() as session:
        session["UserID"] = 4
        session["UserType"] = "employee"


    response = client.get("/portal/shiftscheduling")


    assert response.status_code == 200


    responseData = response.get_data(as_text=True)

    assert "Manual Add Shift" not in responseData
    assert "Shift Template" not in responseData
    assert "Add Shift" not in responseData
    assert "Delete Shift" not in responseData
    assert "Automatic Schedule Start" not in responseData


def test_shiftscheduling_manager_render_as_owner(client):
    # Testing owner is redirected to the portal #

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "owner"

    response = client.get("/portal/shiftscheduling", follow_redirects=False)

    assert response.status_code == 302

    assert response.headers["Location"] == "/portal"


def test_manager_add_shifttemplate(client):
    # Testing when an add shift template form post request made #

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 2
        session["UserType"] = "manager"

    # Simulated form request #
    templateAddForm = {
        "action": "add",
        "day": "0",
        "starttime": "09:12",
        "endtime": "10:13",
        "employee": "1"
    }

    response = client.post("/portal/shiftscheduling", data=templateAddForm)

    templateAddForm = {
        "action": "add",
        "day": "1",
        "starttime": "07:03",
        "endtime": "12:19",
        "employee": "1"
    }

    response = client.post("/portal/shiftscheduling", data=templateAddForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Monday: 09:12 - 10:13" in responseData
    assert "Tuesday: 07:03 - 12:19" in responseData

def test_manager_add_shifttemplate_invalid(client):
    # Testing when a post request made with no data #

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 2
        session["UserType"] = "manager"

    # Simulated form request #
    templateAddForm = {
        "action": "add",
        "day": "",
        "starttime": "",
        "endtime": "",
        "employee": ""
    }

    response = client.post("/portal/shiftscheduling", data=templateAddForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Please Fill All Action Fields!" in responseData

    # Testing if endtime less than start time #
    templateAddForm = {
        "action": "add",
        "day": "2",
        "starttime": "12:00",
        "endtime": "11:00",
        "employee": "1"
    }

    response = client.post("/portal/shiftscheduling", data=templateAddForm, follow_redirects=True)

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Wednesday: 12:00 - 11:00" not in responseData
    assert "End Time Should Be After Start Time!" in responseData



## FOR DELETE TESTING, YOU WILL NEED TO FETCH AN ID or IDs FROM DB ##
def test_manager_delete_shifttemplate(client):
    # Testing when an add shift template form post request made #

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 2
        session["UserType"] = "manager"
    # Simulated form request #
    templateDeleteForm = {
        "action": "delete",
        "shift": 0
    }

    response = client.post("/portal/shiftscheduling", data=templateDeleteForm, follow_redirects=True)
    assert response.status_code == 200

    templateDeleteForm = {
        "action": "delete",
        "shift": 2
    }

    response = client.post("/portal/shiftscheduling", data=templateDeleteForm, follow_redirects=True)
    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert '<option value="15">Tuesday: 07:03 - 12:19</option>' not in responseData

def test_manager_auto_schedule(client):
    # Testing when an add shift template form post request made #

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 2
        session["UserType"] = "manager"

    # Simulated form request #
    autoScheduleForm = {
        "action": "auto"
    }

    response = client.post("/portal/shiftscheduling", data=autoScheduleForm, follow_redirects=True)
    assert response.status_code == 200

    ## WE CAN VERIFY THE SHIFT WAS SCHEDULED ON EMPLOYEE PAGE ##

def test_manager_manual_shift_add(client):
    with client.session_transaction() as session:
        session["UserID"] = 2
        session["UserType"] = "manager"

    today = datetime.datetime.now().date()
    manualAddForm = {
        "action": "manualAdd",
        "date": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "manualStarttime": "11:52",
        "manualEndtime": "16:09",
        "manualEmployee": "1"
    }

    response = client.post("/portal/shiftscheduling", data=manualAddForm, follow_redirects=True)
    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Employee 1: 11:52 - 16:09" in responseData

def test_manager_manual_shift_add_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 2
        session["UserType"] = "manager"

    manualAddForm = {
        "action": "manualAdd",
        "date": "",
        "manualStarttime": "",
        "manualEndtime": "",
        "manualEmployee": ""
    }

    response = client.post("/portal/shiftscheduling", data=manualAddForm, follow_redirects=True)
    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Please Fill All Fields!" in responseData

    today = datetime.datetime.now().date()
    manualAddForm = {
        "action": "manualAdd",
        "date": datetime.datetime.strftime(today, "%Y-%m-%d"),
        "manualStarttime": "12:00",
        "manualEndtime": "11:00",
        "manualEmployee": "1"
    }

    response = client.post("/portal/shiftscheduling", data=manualAddForm, follow_redirects=True)
    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Employee 1: 12:00 - 11:00" not in responseData
    assert "End Time Should Be After Start Time!" in responseData


## AGAIN FIND A SHIFT TO DELETE, YOU CAN FIND THE SHIFT CREATED ABOVE! ##
def test_manager_manual_shift_delete(client):
    with client.session_transaction() as session:
        session["UserID"] = 2
        session["UserType"] = "manager"

    manualDeleteForm = {
        "action": "actualDelete",
        "shiftID": "3"
    }

    response = client.post("/portal/shiftscheduling", data=manualDeleteForm, follow_redirects=True)
    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert '<input type="hidden" name="shiftID" value="3">' not in responseData


#####################################################################
### Employee Testing ###


def test_shiftscheduling_employee_render(client):
    # Testing manager shift scheduling page renders successfully #
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"


    response = client.get("/portal/shiftscheduling")


    assert response.status_code == 200


    responseData = response.get_data(as_text=True)
    assert "Requested Shifts" in responseData
    assert "11:52 - 16:09" in responseData


def test_shiftscheduling_employee_accept(client):
    # Testing manager shift scheduling page renders successfully #
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    acceptForm = {
        "requestedShiftAction": "accept",
        "shiftID": "2"
    }

    response = client.post("/portal/shiftscheduling", data=acceptForm, follow_redirects=True)


    assert response.status_code == 200

    responseData = response.get_data(as_text=True)
    assert '<input type="hidden" name="shiftID" value="2">' not in responseData

def test_shiftscheduling_employee_accept(client):
    # Testing manager shift scheduling page renders successfully #
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    acceptForm = {
        "requestedShiftAction": "decline",
        "shiftID": "1"
    }

    response = client.post("/portal/shiftscheduling", data=acceptForm, follow_redirects=True)
    assert response.status_code == 200

    responseData = response.get_data(as_text=True)
    assert '<input type="hidden" name="shiftID" value="1">' not in responseData

    with client.session_transaction() as session:
        session["UserID"] = 2
        session["UserType"] = "employee"

    response = client.get("/portal/shiftscheduling")
    responseData = response.get_data(as_text=True)
    assert '<input type="hidden" name="shiftID" value="1">' in responseData


