import sys
import os
from datetime import datetime

sys.path.append(os.getcwd() + "/../Pose_Estimation")
sys.path.append(os.getcwd() + "/src/Pose_Estimation")

from jab_classifier import jab_classifier

class Controller(object):
    
    def get_feedback_analysis(self, model_location, video_location):

        #video_location = os.path.join(os.getcwd(), "static/tmp_video/", os.listdir("static/tmp_video/")[0])

        PATH = os.getcwd() # Save path for after

        feedback_dictionary = jab_classifier(model_location, video_location)

        #feedback_report = self.convert_dictionary_to_report_jab(feedback_dictionary)

        # Revert back to old path
        os.chdir(PATH)
        
        return feedback_dictionary
    '''
    def save_feedback_report(self, feedback_report):

        feedback_report_directory = "static/feedback_reports/"
        date = datetime.datetime.today().strftime('%d_%m_%y')

        text_file = open(feedback_report_directory + "jab_" + date + ".txt", "w")
        text_file.write(feedback_report)
        text_file.close
    '''
    def get_feedback_reports(self):
        returned_file = ""

        feedback_report_directory = "static/feedback_reports/"

        for feedback_file in os.listdir(os.getcwd() + feedback_report_directory):
            with open(feedback_file) as infile:
                returned_file += infile.read()
            returned_file += "\n"
        
        return returned_file


    def convert_dictionary_to_report_jab(self, feedback_dic, from_database=False):
        
        try:
            if from_database:
                feedback_dic = eval(feedback_dic)
        except SyntaxError:
            return ""
        
        feedback_report = ""
        satisfied_counter = 0 

        feedback_report += "Jab Feedback Report" + "\n"
    

        # Arm protection prediction handling
        if feedback_dic['1'] == 1:
            feedback_report += "Great! Your right hand is protecting your chin.\n"
            satisfied_counter += 1

        elif feedback_dic['1'] == 0:
            feedback_report += "Oh no! Your right hand is not projecting your chin as it should be.\n"

        elif feedback_dic['1'] == 2:
            feedback_report += "Unable to predict if your chin was protected with your right hand, as some body landmarks were out of frame. \n"


        # Chin protection prediction handling
        if feedback_dic['2'] == 1:    
            feedback_report += "Great! Your left shoulder is correctly protecting your chin.\n"
            satisfied_counter += 1

        elif feedback_dic['2'] == 0:
            feedback_report += "Oh no! Your left shoulder is too low and not protecting your chin.\n"

        elif feedback_dic['2'] == 2:
            feedback_report += "Unable to predict if your chin was protected with your left shoulder, as some body landmarks were out of frame. \n"

        
        # Jab elbow prediction handling
        if feedback_dic['3'] == 1:
            feedback_report += "Great! Your elbow is in the correct position while jabbing.\n"
            satisfied_counter += 1

        elif feedback_dic['3'] == 0:
            feedback_report += "Oh no! The elbow of your jabbing arm is sticking outwards when you jab. Try bringing your elbow from under your hang upwards while jabbing, instead of from the side.\n"

        elif feedback_dic['3'] == 2:
            feedback_report += "Unable to predict if your jabbing arm elbow was correctly positioned, as some body landmarks were out of frame. \n"

        
        # Overcommitting prediction handling
        if feedback_dic['4'] == 1:
            feedback_report += "Great! You're not over-committing when jabbing.\n"
            satisfied_counter += 1

        elif feedback_dic['4'] == 0:
            feedback_report += "Oh no! You're leaning too much on your front leg. Try to stay balanced and not overcommit.\n"

        elif feedback_dic['4'] == 2:
            feedback_report += "Unable to predict if you were overcommitting to the jab, as some body landmarks were out of frame. \n"

        
        # Right elbow prediction handling
        if feedback_dic['5'] == 1:
            feedback_report += "Great! You're protecting your body with your right arm.\n"
            satisfied_counter += 1
        
        elif feedback_dic['5'] == 0:
            feedback_report += "Oh no! Your right arm is not covering your body, leaving you vulnerable to body shots.\n"

        elif feedback_dic['5'] == 2:
            feedback_report += "Unable to predict if your body was protected with your right arm, as some body landmarks were out of frame. \n"

        if satisfied_counter == 5:
            feedback_report += "Your form is great! Keep it up!\n"

        return feedback_report