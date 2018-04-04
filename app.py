from flask import Flask, render_template
appy = Flask(__name__,static_url_path="/static")
from flask import jsonify
import os.path
import sys
import json
from flask import request
import pandas as pd
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
#import pyopenssl    
import requests
import memcache
import time
import csv
from chat import UnQstn, ArrayOfQuestions

UQ = UnQstn("","")

mc = memcache.Client(['127.0.0.1:11211'], debug=0)


@appy.route("/")
def template_test():
#return("hello")
    return render_template('in.html')

@appy.route("/update_memcache/")
def agent_mem():
    answer = request.args.get('ans')
    timestamp = time.strftime("%H:%M:%S")
    mc_value = mc.get("sanchit")
    value = mc_value[-1]
    mc_value[-1] = {"query":value['query'],"response":answer,"timestamp":timestamp,"person":"Human", "speach_status":True}
    mc.set("sanchit",mc_value)
    print(mc.get("sanchit"))
    UQ.question = value['query']
    print(UQ.question)
    UQ.answer = answer
    print(UQ.answer)
    with open('sanchit.csv', 'a') as Ques_Ans:
            writer = csv.writer(Ques_Ans)
            writer.writerow([UQ.question, UQ.answer]) 
            print("appended")
    return "Success"

@appy.route("/CustomerAgent")
def api_call():
    # q = request.args.get('q')
    # resp = api_main(q)
    # print (resp)
    # mc.set("sanchit",[{q,resp}])
    value = mc.get("sanchit")
    print(value)
#    val = json.dumps(value)
    return jsonify({"speech":value})


if __name__ == '__main__':
    # app.run(ssl_context='adhoc')
    appy.run(debug=True, host='127.0.0.1', port=8004)
