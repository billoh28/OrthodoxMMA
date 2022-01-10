# Tests for home page endpoint

def test_get_home_page(client):
    # request data from app

    r = client.get("/home")
    assert r.status_code == 302 # Test for when not logged in

    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.get("/home") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check OK
    assert r.status_code == 200

def test_post_home_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.post("/home", data=dict(unused="NotExpectedData")) # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_put_home_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.put("/home") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_delete_home_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.delete("/home") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_head_home_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.head("/home") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check Redirect
    assert r.status_code == 302 # Might need to be a 204
