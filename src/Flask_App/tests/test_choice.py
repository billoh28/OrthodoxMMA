# Test for recording page endpoint

def test_get_choice_page(client):
    # request data from app

    r = client.get("/choice")
    assert r.status_code == 302 # Test for when not logged in

    with client.session_transaction() as sess:
        sess['loggedin'] = True

    r = client.get("/choice") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check Redirect
    # This is a redirect as choice should only be accessible through training_page.html, meaning a choice has to be provided
    assert r.status_code == 302

def test_good_get_choice_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True

    r = client.get("/choice?choice=upload") # Test upload
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check OK
    assert r.status_code == 200

    r = client.get("/choice?choice=live") # Test live
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check OK
    assert r.status_code == 200

def test_bad_get_choice_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True

    r = client.get("/choice?choice=test") # Test unsupported choice
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check OK
    assert r.status_code == 400

def test_post_choice_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.post("/choice", data=dict(unused="NotExpectedData")) # Test post request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_put_choice_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.put("/choice") # Test put request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_delete_choice_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.delete("/choice", data=dict(choice="live")) # Test delete request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_head_choice_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.head("/choice") # Test head request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check Redirect
    assert r.status_code == 302
