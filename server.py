from flask import Flask, render_template
app = Flask(__name__,static_url_path="/static")
from flask import jsonify
import os.path
import sys
import json
import time
import pandas as pd
from flask import request
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
import random    
import requests
import memcache
import csv
from claim import ClaimInit, ArrayOfClaims
from datetime import datetime , timedelta
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob



UQ = ClaimInit("","","","","","","","")
Adjuster=["Sanchit Ghai","Surya Balakrishnan","Amarjeet Kumar","R Ragunath"]
Number=["+91 8283080897","+91 9313761818","+91 7087292847","+91 7000754321"]
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
#mc.set("sanchit",[])

@app.route("/")
def template_test():
    print("hello")
    mc.set("sanchit", [])
    return render_template('initial.html')



@app.route("/Agent")
def Api_Call():
    value = mc.get("sanchit")
    print(value)
    return jsonify({"speech":value})



@app.route("/rest/api/")
def api_call():
    q = request.args.get('q')
    timestamp = time.strftime("%H:%M:%S")
    print(time)
    resp = api_main(q)
    print (resp)
    speach_status = True
    person = "Bot"
    if (not resp):
        speach_status = False
        resp = ""
        person = "Human"
    if (isinstance(resp, str)):
        mc_value = mc.get("sanchit")
		#print ({"query":q,"response":resp,"timestamp":timestamp,"person":person, "speach_status":speach_status})
        mc_value.append({"query":q,"response":resp,"timestamp":timestamp,"person":person, "speach_status":speach_status})
        mc.set("sanchit",mc_value)
        return jsonify({"speech":resp,"Person":"Human", "speach_status":speach_status,"responseObj":resp})
    else:
        mc_value = mc.get("sanchit")
		#print ({"query":q,"response":resp,"timestamp":timestamp,"person":person, "speach_status":speach_status})
        mc_value.append({"query":q,"response":resp['result']['fulfillment']['speech'],"timestamp":timestamp,"person":person, "speach_status":speach_status})
        mc.set("sanchit",mc_value)
        return jsonify({"speech":resp['result']['fulfillment']['speech'],"Person":"Human", "speach_status":speach_status,"responseObj":resp})




CLIENT_ACCESS_TOKEN = '4f138e28b6bf465895f5cdc36a3a840f'

    

def PolicyAmount(UserPolicyNumber):
   csv_file = csv.reader(open('policy.csv'), delimiter=",")
   pol_num = UserPolicyNumber
   for row in csv_file:
       if pol_num == row[0]:
           CA1 = "<span class='coverageBullets'>"+(str(row[1]) + " coverage amounts for <span style='color: #14b14b;font-weight: bold;'>$" + str(row[3])+"</span></span>")
           CA2 = "<span class='coverageBullets'>"+(str(row[2]) + " coverage amounts for <span style='color: #14b14b;font-weight: bold;'>$" + str(row[4])+"</span></span>")
           CA = str(CA1) + str(CA2)                         
           return(CA)
    
        
def AfterClaim(UserClaimNumber):
    csv_file = csv.reader(open('claim.csv'), delimiter=",")
    clm_num = UserClaimNumber
    for row in csv_file:
        if clm_num == row[0]:
            clm_adj = ("As per our records "+ row[1] +" your assigned claim adjuster would be visiting your property on "+ str(row[2])+". Your adjuster will guide you about the next step.")
            return (clm_adj)
   # print(Details)
    

def ClaimAdjuster(UserClaimNumber):
    csv_file = csv.reader(open('claim.csv'), delimiter=",")
    clm_num = UserClaimNumber
    for row in csv_file:
        if clm_num == row[0]:
            clm_adj_details = ("Your claim has been assigned to our claim adjuster "+row[1]+". You can reach out to the adjuster through phone on number - "+str(row[3]))
            return(clm_adj_details)

def PropertyDamage(UserPolicyNumber):
    csv_file = csv.reader(open('policy.csv'), delimiter=",")
    pol_num = UserPolicyNumber
    for row in csv_file:
        if pol_num == row[0]:
            PD1 = ("<span class='coverageBullets'>"+ row[1]+" ( " + row[5] + " ).</span>")
            PD2 = ("<span class='coverageBullets'>"+ row[2]+" ( " + row[6] + " ).</span>")
            PD = PD1 + PD2
            return(PD)
   # for number in coverages:

def Random():
    a = random.randint(00000000001,00000010000)
    csv_file = csv.reader(open('claim.csv'), delimiter=",")
    for row in csv_file:
        if a == row[0]:
            Random()
        else:
            a = "%011d" %(a,)
            return(a)

def classifier(something):
    speech = something


    train = []
    test = []
    
    with open("training.csv") as csvfile:
        reader = csv.reader(csvfile) # change contents to floats
        for row in reader: # each row is a list
            train.append(row)
            
        with open("test.csv") as csvfile:
            reader = csv.reader(csvfile) # change contents to floats
            for row in reader: # each row is a list
                test.append(row)
        
    
    cl = NaiveBayesClassifier(train)
    cl.classify("This is an amazing library!")
    prob_dist = cl.prob_classify("This one's a doozy.")
    prob_dist.max()
    round(prob_dist.prob("machine"), 2)
    round(prob_dist.prob("no machine"), 2)
    blob = TextBlob(speech, classifier=cl)
    blob.classify()
    for s in blob.sentences:
        print("\n\n\n" + str(s))
        print("\n" + str(s.classify()))
        return(s.classify())
        #print("\n" + str(cl.accuracy(test)))

    
    
def api_main(Querry):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID>"

    request.query = Querry

    response = request.getresponse()
    
   # print (response.read())
    
    JsonData = response.read()
    
    JsonToPython = json.loads(JsonData)
    print(JsonToPython['result'])
    
    ActionName = JsonToPython['result']['action'] 
    ActionIncomplete = JsonToPython['result']['actionIncomplete']
    
    if ActionName == 'input.Claim_Initiated' and ActionIncomplete == False :
        UserClaimNumber = JsonToPython['result']['contexts'][0]['parameters']['Claim-Number'][0]['number.original']
        print(UserClaimNumber)
        aftr_clm = AfterClaim(UserClaimNumber)
        return(aftr_clm)
       # print (UserClaimNumber)
        
    elif ActionName == 'input.Coverage_Amount' and ActionIncomplete == False:
        UserPolicyNumber = JsonToPython['result']['contexts'][0]['parameters']['Policy_Number']
        init_stat = ("<span style='color: #666766;font-weight: 500;'>Coverage Details</span><span class='list-card-description'>Cool. You're all set. You are covered for </span>")
        CA = PolicyAmount(UserPolicyNumber)
        final_statement = init_stat + str(CA)
        return(final_statement)

        
    elif ActionName == 'input.PropertyDamage' :
        UserPolicyNumber = JsonToPython['result']['contexts'][0]['parameters']['Policy_Number']
        ini_stat = ("<span style='color: #666766;font-weight: 500;'>Property Damage</span><span style='display:block;'><img src='static/images/propertyDamage.jpg' style='height: 100%;width: 100%;'></span><span class='list-card-description'>You are covered for damage to </span>")
        prop_dmg = PropertyDamage(UserPolicyNumber)
        close_stat = ("<span style='display:block'>Is their any other information I can help you with ?</span>")
        fl_stat = ini_stat + str(prop_dmg) + close_stat
        return(fl_stat)                        


        
    elif ActionName == 'input.ClaimAdjuster' :
        UserClaimNumber = JsonToPython['result']['contexts'][0]['parameters']['Claim-Number'][0]['number.original']
        print(UserClaimNumber)
        fnl_statement = ClaimAdjuster(UserClaimNumber)
        return(fnl_statement)
    
    elif ActionName == 'input.Link_Not_Working' :
        UserPolicyNumber = JsonToPython['result']['contexts'][0]['parameters']['Policy_Number']
        
        Cause = JsonToPython['result']['contexts'][0]['parameters']['Accident.original']
        TIME = JsonToPython['result']['contexts'][0]['parameters']['time']
        DATE = JsonToPython['result']['contexts'][0]['parameters']['date'][0]
        print (DATE)
        TimeStamp = str(DATE)+"T"+str(TIME)+"Z"
        UQ.Claim_Number = Random()
        UQ.AdjusterName = Adjuster[random.randint(0,3)]
        import datetime
        mylist = []
        b = datetime.date.today()
        a = b + timedelta(days=5)
        mylist.append(a)
        UQ.DateOfVisit = mylist[0]
        UQ.ContactNumber = Number[random.randint(0,3)]
        UQ.Date = DATE
        UQ.Time = TIME
        UQ.Cause = Cause
        UQ.PolicyNumber = UserPolicyNumber
        with open('claim.csv', 'a') as Ques_Ans:
            writer = csv.writer(Ques_Ans)
            writer.writerow([UQ.Claim_Number,UQ.AdjusterName,UQ.DateOfVisit,UQ.ContactNumber,UQ.Date,UQ.Time,UQ.Cause,UQ.PolicyNumber])

        final = ("<span style='color: #666766;font-weight: 500;margin-bottom: 2px;'>Claim Registration</span><span class='list-card-description'>Your Claim has been initiated and your claim registration number is <span style='color: #f9eeaa;font-weight: bold;'>"+str(UQ.Claim_Number)+".</span></span><span style='display: block;margin-bottom: 20px;'> You will shortly recieve a call from our Claims Team who will assist you further</span> <span style='display:block;margin-bottom: 2px;'> Is there anything else that I may help you with ?</span><div class='quick-replies-buttons'><button type='button' class='btn pmd-btn-outline pmd-ripple-effect btn-info .pmd-btn-fab apiQuickreplybtnPayload' data-apiquickrepliespayload='Yes, Please'>Yes, Please</button><button type='button' class='btn pmd-btn-outline pmd-ripple-effect btn-info .pmd-btn-fab apiQuickreplybtnPayload' data-apiquickrepliespayload='No, Thanks'>No, Thanks</button></div>")
        print (final)
        return (final)
    
    elif ActionName == 'input.unknown' :
        
        a = classifier(Querry)
        if a == 'machine':
            flag = 0
            csv_file = csv.reader(open('sanchit.csv'), delimiter=",")
            qstn = Querry
            for row in csv_file:
                print("checking...")
                if qstn == row[0]:
                    return(row[1])
                    flag = flag +1
                    
            if(flag==0):        
                return(False)
        elif a == 'no machine':
            return("I am not trained for this scope..")
    
    else:    
        return (JsonToPython)

	
if __name__ == '__main__':
    app.run(ssl_context='adhoc')
    #app.run(ssl_context='adhoc', host='0.0.0.0', port=7000)
