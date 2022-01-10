# Tests for training page endpoint

def test_get_training_page(client):
    # request data from app

    r = client.get("/training_page")
    assert r.status_code == 302 # Test for when not logged in

    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.get("/training_page") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check OK
    assert r.status_code == 200

def test_post_training_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.post("/training_page", data=dict(unused="NotExpectedData")) # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_put_training_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.put("/training_page") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_delete_training_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.delete("/training_page") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_head_training_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.head("/training_page") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check Redirect
    assert r.status_code == 302

def test_good_choice_training_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.get("/training_page?choice=jab") # Test supported choice i.e. jab, straight, hook
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check OK
    assert r.status_code == 200

def test_bad_choice_training_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.get("/training_page?choice=unsupported") # Test unsupported choice
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check BadRequest
    assert r.status_code == 400