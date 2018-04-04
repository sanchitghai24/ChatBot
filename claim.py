class ClaimInit:
    def __init__(self,Claim_Number,AdjusterName,DateOfVisit,ContactNumber,Date,Time,Cause,PolicyNumber):
        self.Claim_Number = Claim_Number
        self.AdjusterName = AdjusterName
        self.DateOfVisit = DateOfVisit
        self.ContactNumber = ContactNumber
        self.Date = Date
        self.Time = Time
        self.Cause = Cause
        self.PolicyNumber = PolicyNumber
        
Claim = ClaimInit("Claim_Number","AdjusterName","DateOfVisit","ContactNumber","Date","Time","Cause","PolicyNumber")
Claim_one = ClaimInit("00000000103","Sanchit","30 Feb 2018","9090909090","12 Feb 2018","12:30","fire","BOP100002")
Claim_two = ClaimInit("00000000123","Surya","31 April 2018","0909090909","18 Feb 2018","23:45","fire","BOP100001")
                          
ArrayOfClaims = [Claim,Claim_one,Claim_two] 

#print (ArrayOfQuestions)       