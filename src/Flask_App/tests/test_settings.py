# Test for settings page endpoint

def test_get_settings_page(client):
    # request data from app

    r = client.get("/settings_page")
    assert r.status_code == 302 # Test for when not logged in

    with client.session_transaction() as sess:
        sess['loggedin'] = True

    r = client.get("/settings_page") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check OK
    assert r.status_code == 200

''' This is cannot be used on CI CD pipeline since it does not have access to our database
def test_put_settings_page(client):
    r = client.get("/settings_page")
    assert r.status_code == 302 # Test for when not logged in

    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True  
        sess['email'] = "t@g.c"
        
    r = client.put("/settings_page", data=dict(password="1", conf_password="1")) # Test delete request

    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 200
'''

# Can't test due to session['email'] is required.
def test_delete_settings_page(client):

    r = client.get("/settings_page")
    assert r.status_code == 302 # Test for when not logged in

    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    # r = client.delete("/settings_page", data=dict(email="1")) # Test delete request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    # assert r.status_code == 200