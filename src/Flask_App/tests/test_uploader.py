# Test for upload page endpoint
# Should only accept POST requests

# Cannot get test working as should be
def test_good_post_uploader_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True

    import os, io

    # Load in preexisting testing video
    data = open(os.path.join(".", "tests", "testing_video.mp4"), "rb")
    fileStream = io.BytesIO(data.read())

    dict_data = {}
    dict_data["video_upload"] = (fileStream, "testing_video.mp4")

    print(dict_data)

    r = client.post("/uploader", data=dict_data, content_type="multipart/form-data") # Expects byte array

    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8" or "text/html"

    # Check Bad Request
    assert r.status_code == 200

def test_bad_post_uploader_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True

    r = client.post("/uploader", data=b"NotAVideoByteArrayAsShouldBe") # Expects byte array

    #print(r.data)

    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8" or "text/html"

    # Check Bad Request
    assert r.status_code == 400

def test_put_uploader_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.put("/uploader") # Test put request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_delete_uploader_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.delete("/uploader") # Test delete request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_head_uploader_page(client):
    # request data from app
    with client.session_transaction() as sess:
        sess['loggedin'] = True
    
    r = client.head("/uploader") # Test head request
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405

def test_get_uploader_page(client):
    # request data from app

    with client.session_transaction() as sess:
        sess['loggedin'] = True

    r = client.get("/uploader") # Test for when logged in
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check MethodNotAllowed
    assert r.status_code == 405