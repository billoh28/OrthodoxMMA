#!flask/bin/python
from flask import Flask, request, jsonify, Response, render_template, redirect, session, url_for, send_from_directory
import json, time

# Networking requirements
import socket
import time
import os
import sys
import requests
import yaml

from werkzeug.security import generate_password_hash, check_password_hash

# Video handling libraries
import cv2

# Logging imports
import logging

#Controller function
from Controller.feedback_controller import Controller

def create_app():
    # Creates a flask app
    app = Flask(__name__)

    # Check file extension
    def allowed_ext(filename):
        if not "." in filename:
            return False

        # Ensures that the file extension is in the list that we allow
        if filename.rsplit(".", 1)[1].upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return True
        else:
            return False

    #################### Routing ####################

    # For requests library (API)
    def _url(path):
        return "http://localhost:8080/user-api" + path

    #For now we can just call this function to ensure the username or email is the correct credentials.
    def GetUserByEmail(email):
        return requests.get(_url('/user/{:s}'.format(email)))

    def RegisterUser(email, pw):
        return requests.post(_url('/user'), json={"Email": email,
                                                "Encrypt_pasword":pw})

    def UpdatePassword(email, pw):
        return requests.put(_url('/user/{:s}'.format(email)), json={"Email": email,
                                                "Encrypt_pasword":pw})
    
    def DeleteUser(email):
        return requests.delete(_url('/user/{:s}'.format(email)))

    def SendFeedback(email, feedback):
        return requests.post(_url('-feedback/user/'), json={"Email": email,
                                                            "Feedback": feedback})

    def GetAllFeedbacks(email):
        return requests.get(_url('-feedback/user/{}'.format(email)))

    # ERROR PAGE ROUTING
    @app.errorhandler(401) # BadRequest Error Code
    def bad_request_page(e):
        return render_template("401.html"), 401

    @app.errorhandler(404) # FileNotFound Error Code
    def file_not_found_page(e):
        return render_template("404.html"), 404

    @app.errorhandler(405) # MethodNotAllowed Error Code e.g. DELETE request on home page
    def method_not_allowed_page(e):
        return Response("<h2>405: The method attempted is not allowed for this endpoint. Please use an OPTIONS request to determine options for a given endpoint</h2>", 405, mimetype="text/html")

    # APP PAGE ROUTING

    # Routing a call to path "/" to this method (root endpoint)
    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")

        elif request.method == "POST":
            email = request.form["email"]
            pw = request.form["password"]

            # Once we have the email, must send it to the database to check if it's a reqistered user
            # Currently dont have password implemented
            response = GetUserByEmail(email)
            if response.status_code == 200 and email != "" and check_password_hash(response.json()["Encrypt_pasword"], pw):
                # registered_user = True

                # Set up session key
                session['loggedin'] = True
                session['email'] = email

                return render_template("home.html")
            else:
                msg = "Incorrect email address and / or password."
                return render_template("login.html", msg=msg), 401

    @app.route("/logout")
    def logout():
        session.pop('loggedin', None)
        session.pop('email', None)

        return redirect(url_for("login"))

    # Register Page
    @app.route("/register", methods=["GET", "POST"])
    def register_page():
        if request.method == "GET":
            return render_template("register.html"), 200

        elif request.method == "POST":
            email = request.form["email"] # Should check if either are empty
            pw = request.form["password"]
            pw = generate_password_hash(pw)

            # Check if username is already registered
            response = GetUserByEmail(email)

            if response.status_code == 200: # User already exists
                msg = "This username is already taken"
                return render_template("register.html", msg=msg), 302

            if len(pw) == 0:
                msg = "Please provide a password"
                return render_template("register.html", msg=msg), 400

            response = RegisterUser(email, pw) # Attempt to register user

            if response.status_code == 200:
                # Set up session key
                session['loggedin'] = True
                session['email'] = email

                return render_template("home.html"), 200

            else:
                # Add error to error logger file
                error_file = open("register_error.log", "a")
                error_file.write("[{:}] : A {:} error occurred when calling the API".format(time.ctime(), str(response.status_code)))
                error_file.write("\n")
                error_file.close()

                msg = "An error occurred. Please try again"
                return render_template("register.html", msg=msg), 500

    # Home Page
    @app.route("/home", methods=["GET"])
    def home(): 
        if 'loggedin' in session:
            if request.method == "GET":
                return render_template("home.html")
        return redirect(url_for('login'))

    @app.route("/training_page", methods=["GET"])
    def training_page():
        if 'loggedin' in session:
            if request.method == "GET":
                # Check if a choice has been selected
                if request.args.get("choice"):
                    # Get chosen choice, but ensure it is an anticipated choice
                    poss_choices = {"jab", "straight", "hook"}
                    choice = request.args.get("choice")
                    # Checker
                    if choice in poss_choices:
                        # Return video stream
                        return render_template("choice.html", choice=choice), 200

                    # If choice given is wrong
                    return render_template("training_page.html", bad_request="The choice provided was unsupported. Please choose from the list above."), 400
                return render_template("training_page.html"), 200 # Page reload or initial get
            
        return redirect(url_for('login'))

    # Page for user to decide between live recording or prerecording
    @app.route("/choice", methods=["GET"])
    def choice_page():
        if 'loggedin' in session:
            if request.method == "GET":
                # Get choice and return page based on choice
                if request.args.get("choice") == "live":
                    return render_template("live_feed.html")

                elif request.args.get("choice") == "upload":
                    return render_template("upload_video.html"), 200

                elif request.args.get("choice"): # Choice provided but just not one of the above
                    # Return training_page.html as choice should only be accessible through that endpoint
                    return render_template("training_page.html", bad_request="The choice provided was unsupported. Please choose from the list above."), 400

                # Return training_page.html as choice should only be accessible through that endpoint
                return render_template("training_page.html"), 302

        return redirect(url_for('login'))

    # Live recording page
    @app.route("/recording", methods=["GET", "POST"])
    def recording_page():
        if 'loggedin' in session:
            if request.method == "GET":
                # Render live recording page
                return render_template("live_feed.html"), 200

            elif request.method == "POST":
                # Make a unique file name based on time for concurrency
                unique_fn = "temp" + str(int(time.time() * 1000000)) + ".mp4"

                # Make file PATH object
                video_path = os.path.join(app.config["VIDEO_UPLOAD_FOLDER"], unique_fn)

                # Extract data
                video_data = request.data
                
                try:
                    # Save data
                    f = open(video_path, "wb")
                    f.write(video_data) # write data
                    f.close()


                    # this is required to prevent malicious POST requests to this endpoint containing data other than .mp4 data
                    # Check if data provided is indeed a video
                    cap = cv2.VideoCapture(video_path)

                    if not cap.isOpened():
                        os.remove(video_path)
                        raise cv2.error
                    
                    if app.config['TESTING']:
                        # Generated video must be removed
                        os.remove(video_path)

                    # Reset
                    cap = None

                    return Response(json.dumps({'success':True, 'data':unique_fn}), 200, mimetype='application/json') # Send the unique temp video file name back to javascript
                
                except TypeError: # Should be a byte array
                    return Response(json.dumps({'success':False, 'data':"The data received from the recording page was of the wrong type or corrupted. Please try again"}), 400, mimetype='application/json')

                except cv2.error: # Byte array was not a video
                    return Response(json.dumps({'success':False, 'data':"The data received from the recording page was of the wrong type or corrupted. Please try again"}), 400, mimetype='application/json')

        return redirect(url_for('login'))

    # Feedback report generation from recorded video stream
    @app.route("/recording_results", methods=["GET"])
    def recording_results_page():
        if 'loggedin' in session:
            if request.method == "GET":
                video_name = request.args['video'].strip('"').strip("'")

                try:
                    video_path = os.path.join(app.config["VIDEO_UPLOAD_FOLDER"], video_name)

                    #print(video_path.split("\\\\"))
                    feedback_dictionary = ""
                    feedback_report = ""

                    if not app.config['TESTING']: # Don't run models in testing as gitlab doesn't have models on it, as they are too large :'(
                        # Do some analysis and return the feedback to feedback_report.html while saving to /feedback_report.
                        feedback_dictionary = app_controller.get_feedback_analysis(app.config['MODELS_LOCATION'], video_path)

                        feedback_report = app_controller.convert_dictionary_to_report_jab(feedback_dictionary)

                    # Now attempt to remove temp video
                
                    os.remove(video_path) # Attempt to remove generated video

                    return render_template("feedback_report.html", feedback = feedback_report, feedback_dic = feedback_report), 200

                except OSError:
                    # Video not found
                    return render_template("404.html"), 404
                
            else:
                # Error Handling   
                return render_template("404.html"), 404

            return render_template("upload_video.html")
        return redirect(url_for('login'))
            

    # Used for manually uploading videos
    @app.route("/uploader", methods = ["POST"]) 
    def upload_video():
        if 'loggedin' in session:
            if request.method == "POST":
                video = request.files['video_upload']
                # We now want to save this video in temporpary memory
                # print(video)
                # print(video.filename)

                if allowed_ext(video.filename):
                    # We should look into saving this to cache
                    # For now we can save a video to this location and once our analysis is complete we can 
                    # delete everything from the directory

                    try:
                        # Make a unique file name based on time for concurrency
                        unique_fn = "temp" + str(int(time.time() * 1000000)) + ".mp4"

                        # This is the location where the video will be save in tmp
                        video.save(os.path.join(app.config["VIDEO_UPLOAD_FOLDER"], unique_fn))

                        video_path = os.path.join(app.config["VIDEO_UPLOAD_FOLDER"], unique_fn)

                        feedback_dictionary = ""
                        feedback_report = ""

                        if not app.config['TESTING']:
                            # Do some analysis and return the feedback to feedback_report.html while saving to /feedback_report.
                            feedback_dictionary = app_controller.get_feedback_analysis(app.config['MODELS_LOCATION'], os.path.join(os.getcwd(), "static", "tmp_video", unique_fn))

                            feedback_report = app_controller.convert_dictionary_to_report_jab(feedback_dictionary)
                        
                        os.remove(video_path) # Attempt to remove generated video

                        return render_template("feedback_report.html", feedback = feedback_report, feedback_dictionary = feedback_dictionary)

                    except OSError: # If something goes wrong when deleting or accessing video
                        # Video not found
                        return render_template("404.html"), 404
                    
                else:
                    # Error Handling   
                    return Response("<h1>404</h1><p>Video not found.</p>", 404, mimetype="text/html")

                return render_template("upload_video.html")

        return redirect(url_for('login'))

    # Endpoint for saving feedback reports. Should only accept post requests
    @app.route("/save_feedback", methods=["POST"])
    def save_feedback_page():
        if 'loggedin' in session:
            if request.method == "POST":
                # Extract data
                request_data = request.get_json()
                feedback_report = str(request_data['data'])

                # Must assert this feedback is off a certain form

                # Send feedback report to API given email.
                SendFeedback(session['email'], feedback_report)

                # Return success and redirect to home page
                return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

        return redirect(url_for('login'))
    
    @app.route("/settings_page", methods=["GET", "PUT", "DELETE"])
    def set_page():
        returned_msg = ""
        if 'loggedin' in session:
            if request.method == "PUT":
                if "password" in request.form:

                    # Check if both passwords entered are the same
                    pw = request.form["password"]
                    pwconfirm = request.form["conf_password"]
                    if pw == pwconfirm and len(pw) != 0:
                        # Hash new password
                        hashedpw = generate_password_hash(pw)
                        # Send new password to database
                        response = UpdatePassword(session["email"], hashedpw)

                        if response.status_code == 200:
                            returned_msg = "Successfully changed password."
                            return render_template("settings_page.html", msg=returned_msg), 200

                        else:
                            returned_msg = "An error has occured when updating your password."
                            
                            return render_template("settings_page.html", msg=returned_msg), 500 # Server Error
                    
                    else:
                        returned_msg = "Passwords are not matching or no password was given."
                        return render_template("settings_page.html", msg=returned_msg), 400 # Bad request

                else:
                    return redirect(url_for("set_page"))
                
            elif request.method == "DELETE":
                response = DeleteUser(session["email"])
                # If the deletion is successful, return back tot the login page
                # with confirmation that the account has been deleted
                if response.status_code == 200:
                    return "", 204

                else:
                    returned_msg = "An errored when deleting your account."
                    return render_template("settings_page.html", msg=returned_msg), 500
            
            elif request.method == "GET":
                return render_template("settings_page.html"), 200

        return redirect(url_for('login'))

    @app.route("/feedback_page", methods=["GET"])
    def feedback_page():
        if 'loggedin' in session:
            reports_from_db = GetAllFeedbacks(session['email'])
            reports = ""
            for dic in reports_from_db.json():
                report = app_controller.convert_dictionary_to_report_jab(dic["Feedback"], from_database=True)
                reports += report + '\n\n'

            return render_template("feedback.html", reports = reports)
        return redirect(url_for('login'))

    @app.route("/about_page", methods=["GET"])
    def about_page():
        if 'loggedin' in session:
            return render_template("about.html")
        return redirect(url_for('login'))

    # Browser Icon
    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static', 'styles', 'images'), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')
    
    #################### Setting Up ####################

    # run on ip address of machine
    # print ip address to terminal
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = "0.0.0.0"
        try:
            s.connect(("10.255.255.255", 1))  # try to connect to bogon ip to get ip of machine
            ip = s.getsockname()[0]  # returns ip address of server on local network
        except:
            pass
        finally:
            s.close()
        return ip

    return app, get_ip()

# Function necessary for facilitating testing
def load_configs(app):
    # Load configurations for app
    from platform import system

    # Check which platform the app is run on to determine whether to load windows or linux config
    plf = system() # Either windows or Linux

    if plf == "Windows":
        yaml_loc = open("Config/windows_config.yaml") # For Windows
        configs = yaml.load(yaml_loc, Loader=yaml.FullLoader)

    else:
        yaml_loc = open("Config/ec2_config.yaml") # For Linux
        configs = yaml.load(yaml_loc, Loader=yaml.FullLoader)

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    
    UPLOAD_FOLDER = os.path.join(APP_ROOT, configs["upload_location"])
    FEEDBACK_FOLDER = os.path.join(APP_ROOT, configs["feedback_location"])
    MODEL_FOLDER = configs["model_location"]

    app.config["ALLOWED_IMAGE_EXTENSIONS"] = [configs["allowed_extentions"]]
    app.config['VIDEO_UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['FEEDBACK_FOLDER'] = FEEDBACK_FOLDER
    app.config['MODELS_LOCATION'] = MODEL_FOLDER
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['PATH'] = os.getcwd()

    return app

# IF API is created from this program (Could be run elsewhere for testing etc.)

# create API
app, IP = create_app()

configured_app = load_configs(app)

# Assign Controller 
app_controller = Controller()

'''
# Set up logging
logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('logs.txt')

logger.addHandler(handler)
app.logger.addHandler(handler)
'''

if __name__ == '__main__':
    app.run(port=8888, debug=True) # run app
