# Tests for login page endpoint

def test_get_login_page(client):
    # request data from app
    r = client.get("/")
    
    # Check response file type
    assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

    # Check OK
    assert r.status_code == 200

"""
# API cannot be called on gitlab, as it is not running. This test passes locally when API is also being ran locally.
def test_post_bad_login_page(client):
	# Send post request to server
	r = client.post("/", data=dict(email="NotAnActualUser", password="Testing123"))

	# Check response header
	assert r.headers.get('Content-Type') == "text/html; charset=utf-8"

	# Check status code is for 401 - Unauthorised
	assert r.status_code == 401
"""