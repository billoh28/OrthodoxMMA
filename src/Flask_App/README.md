## Running the Flask App locally for testing:

1. Locate this current directory
2. Run: `python app.py`
3. Runs on localhost on port 8888 `http://localhost:8888/`

## To ssh into AWS ec2 instance:

1. Make sure you have access to .pem file. You may need to change permissions of the pem. `chmod 400`
2. ssh -i "OrthodoxKeyPair.pem" ec2-user@ec2-54-170-50-59.eu-west-1.compute.amazonaws.com
3. Enter password.