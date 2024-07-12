# from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request, jsonify
from configApi import *
# import logging
from logger import *
import traceback
from flask_cors import CORS 
from datetime import datetime, timedelta
import pandas as pd 
import time
import os
import pandas as pd
import sys

sys.path.insert(1,'>file_path of main.py folder<')

logging.debug('Hey 1st Call')

try:
    app = Flask(__name__)
    CORS(app)
    logging.debug('CORS Enabled')
    app.config['CORS_HEADERS']='Content-Type'
except:
    logging.debug('Exception', traceback.format_exc())

PREFIX = '/Sample/'

@app.route(PREFIX+"/Check/")
def app_index():
    logging.debug('Flask Py is running fine, your Highness!!')
    return "Flask is running fine, your Highness. Trueeeeeeee"


@app.route(PREFIX+'/chat',methods=['GET','POST'])
def GenerateResponse():
    start_time = time.time()
    logging.debug(request)
    logging.debug('Inside Module of ChatBot')
    try:
        logging.debug(request.args.get('question'))
        # userID= request.get_json().get('userId')
        userQuestion = request.args.get('question')
        from main import generate_response
        response = generate_response(userQuestion)
        end_time = time.time()
        execution_time = end_time-start_time
        logging.debug('Time taken for python processing :::%s',execution_time)
        return response
    except:
        logging.debug(traceback.format_exc())        
        error = traceback.format_exc()
        return error
    
@app.route(PREFIX+'/codeGen',methods=['GET','POST'])
def GenerateCode():
    start_time = time.time()
    logging.debug(request)
    logging.debug('Inside Module of Code Generator')
    try:
        logging.debug(request.args.get('question'))
        # userID= request.get_json().get('userId')
        userQuestion = request.args.get('question')
        from main import generate_code
        response = generate_code(userQuestion)
        end_time = time.time()
        execution_time = end_time-start_time
        logging.debug('Time taken for python processing :::%s',execution_time)
        return response
    except:
        logging.debug(traceback.format_exc())        
        error = traceback.format_exc()
        return error

# @app.route(PREFIX+'/SaveFeedback/',methods=['GET','POST'])
# def savefeedback():
#     logging.debug(request)
#     logging.debug('Inside Module 3')
#     logging.debug(request.get_json())
#     response = {}
#     try:  
#         try:
#             logging.debug("Starting Saving Feedback...")
#             feedback_df = pd.read_csv('.\\Find_my_report\\Feedback.csv')
#             logging.debug('File opened')
#             feedback_dict = {}
#             current_time = es.now()
#             feedback_dict['Timestamp'] = current_time + timedelta(hours=5,minutes=30)
#             feedback_dict['ResponseID'] = request.get_json().get('responseID')
#             feedback_dict['UserID'] = request.get_json().get('userId')
#             feedback_dict['Question'] = request.get_json().get('textInput')
#             feedback_dict['Response'] = request.get_json().get('response')
#             feedback_dict['Feedback'] = request.get_json().get('feedback')
#             feedback_dict['Comments'] = request.get_json().get('comments')
#             logging.debug('feedback_dict : %s',feedback_dict)
#             new_feedback_df = pd.DataFrame([feedback_dict])
#             feedback_df = pd.concat([feedback_df,new_feedback_df])  
#             feedback_df.to_csv('.\\Find_my_report\\Feedback.csv',index=False) 
#             logging.debug("Feedback Saved")       
#             response['data'] = ['Feedback Taken Successfully']
#             response['responseCode']=200
#             logging.debug("Feedback API success response: %s",response)
#             return jsonify(response)
    
#         except Exception as e:
#             logging.debug('Exception: %s',e)
#             response['data'] = ['Feedback Failed to Save!']
#             response['responseCode']=200
#             logging.debug("Feedback API failure response: %s",response)
#             return jsonify(response)   
#     except:
#         logging.debug(traceback.format_exc())        
#         error = traceback.format_exc()
#         return error

if __name__ == '__main__':
    app.debug = True
    logging.basicConfig(level=logging.DEBUG,
                        handlers=[TimedRotatingFileHandler("logs//system", when="midnight"),
                                  logging.StreamHandler()],
                        format='%(asctime)s - %(module)s.%(funcName)s() - %(levelname)s - %(message)s')
    logging.getLogger('urllib3').setLevel(logging.DEBUG)
    
    app.run()
