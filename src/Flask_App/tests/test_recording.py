# Test for recording page endpoint

def test_get_recording_page(client):
    # request data from app

    r = client.get("/recording")
    assert r.status_code == 302 # Test for when not logged in

    with client.session_transaction() as sess:
        sess['loggedin'] = True

    r = client.get("/recording") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check OK
    assert r.status_code == 200

# Can only be ran locally. Both have passed hwen ran locally.
def test_good_post_recording_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True

    import os, json

    # Load in preexisting testing video
    with open(os.path.join(".", "tests", "testing_video.mp4"), "rb") as test_file:
        data = test_file.read() # read video data

    r = client.post("/recording", data=data) # Expects byte array

    #print(r.data)

    # Delete generated video
    data_dict = json.loads(r.data)

    # Check response file type
    assert r.headers.get('Content-Type') == "application/json"

    # Check Bad Request
    assert r.status_code == 200

def test_bad_post_recording_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True

    r = client.post("/recording", data="NotAVideoByteArrayAsShouldBe") # Expects byte array

    #print(r.data)

    # Check response file type
    assert r.headers.get('Content-Type') == "application/json"

    # Check Bad Request
    assert r.status_code == 400


def test_put_recording_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.put("/recording") # Test put request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_delete_recording_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.delete("/recording", data=dict(recording="live")) # Test delete request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_head_recording_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.head("/recording") # Test head request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check Redirect
    assert r.status_code == 302

