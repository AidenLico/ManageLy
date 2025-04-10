### TESTING CHAT ###
import warnings

def test_chat_manager_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/chat")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

    assert "Direct Message" in responseData
    assert "Employee" in responseData

def test_chat_employee_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    response = client.get("/portal/chat")

    assert response.status_code == 200

    responseData = response.get_data(as_text=True)

def test_chat_owner_render(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "owner"

    response = client.get("/portal/chat")

    assert response.status_code == 302
    assert response.headers["Location"] == "/portal"


def test_chat_groupmessage(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    groupmessageForm = {
        "action": "messageGroup",
        "message": "TEST 12345 *"
    }

    response = client.post("/portal/chat", data=groupmessageForm, follow_redirects=True)

    assert response.status_code == 200
    responseData = response.get_data(as_text=True)
    assert "You: TEST 12345 *" in responseData

def test_chat_groupmessage_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    groupmessageForm = {
        "action": "messageGroup",
        "message": ""
    }

    response = client.post("/portal/chat", data=groupmessageForm, follow_redirects=True)

    assert response.status_code == 200
    responseData = response.get_data(as_text=True)
    assert "Please Enter Message!" in responseData


def test_chat_groupreply(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    groupreplyForm = {
        "action": "replyGroup",
        "reply": "TEST REPLY 12345 *",
        "messageID": "1"
    }

    response = client.post("/portal/chat", data=groupreplyForm, follow_redirects=True)

    assert response.status_code == 200
    responseData = response.get_data(as_text=True)
    assert "Manager 1: TEST 12345 *" in responseData
    assert ">> You: TEST REPLY 12345 *" in responseData

def test_chat_groupreply_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    groupreplyForm = {
        "action": "replyGroup",
        "reply": "",
        "messageID": "1"
    }

    response = client.post("/portal/chat", data=groupreplyForm, follow_redirects=True)

    assert response.status_code == 200
    responseData = response.get_data(as_text=True)
    assert "Please Enter Message!" in responseData



def test_chat_managerdirectmessage(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    directmessageForm = {
        "action": "directSend",
        "directMessage": "TEST DIRECT 12345 *",
        "selectEmployee": "1"
    }

    response = client.post("/portal/chat", data=directmessageForm, follow_redirects=True)

    assert response.status_code == 200
    responseData = response.get_data(as_text=True)
    assert '<div class="whoTo">>> Employee 1</div>' in responseData
    assert "TEST DIRECT 12345 *" in responseData

def test_chat_managerdirectmessage_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    directmessageForm = {
        "action": "directSend",
        "directMessage": "",
        "selectEmployee": "1"
    }

    response = client.post("/portal/chat", data=directmessageForm, follow_redirects=True)

    assert response.status_code == 200
    responseData = response.get_data(as_text=True)
    assert "Please Enter Message!" in responseData

    directmessageForm = {
        "action": "directSend",
        "directMessage": "TEST SHOULD FAIL 12345****",
        "selectEmployee": ""
    }

    response = client.post("/portal/chat", data=directmessageForm, follow_redirects=True)

    assert response.status_code == 200
    responseData = response.get_data(as_text=True)
    assert "Please Enter Message!" in responseData
    assert "TEST SHOULD FAIL 12345****" not in responseData



def test_chat_employeedirectreply(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    directreplyForm = {
        "action": "directEmployeeSend",
        "directEmployeeMessage": "TEST DIRECT REPLY 12345 *",
        "directMessageID": "1"
    }

    response = client.post("/portal/chat", data=directreplyForm, follow_redirects=True)

    assert response.status_code == 200

    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "manager"

    response = client.get("/portal/chat")
    responseData = response.get_data(as_text=True)
    assert "Employee 1: TEST DIRECT REPLY 12345 *" in responseData


def test_chat_employeedirectreply_invalid(client):
    with client.session_transaction() as session:
        session["UserID"] = 1
        session["UserType"] = "employee"

    directreplyForm = {
        "action": "directEmployeeSend",
        "directEmployeeMessage": "",
        "directMessageID": "1"
    }

    response = client.post("/portal/chat", data=directreplyForm, follow_redirects=True)

    assert response.status_code == 200
    responseData = response.get_data(as_text=True)
    assert "Please Enter Message!" in responseData