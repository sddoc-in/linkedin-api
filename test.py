def step1 (accountData, stepsDetails):
    if (stepsDetails["msg"]):
        # print ("send reqquest with note") 
        return {"connection_request_sent": True, "message":"the message that has been sent","key":"send_connection_request"}
    else:
        # print ("connection req sent") 
        return {"connection_request_sent":True,"key":"send_connection_request"}
        
def step2(accountData, stepsDetails):
    # send message code 
    return {"message_sent": True, "message":"the message that has been sent","key":"send_message"}

def step3(accountData, stepsDetails):
    # send message code 
    return {"message_sent": True, "message":"the message that has been sent","key":"send_inmail"}


# type 1
#a = { "campaign_id": "b9efd92c-6181-4ff2-b111-fdde9c79723e", "name": "For Deepak 1", "searchItems": [{"query": "https://www.linkedin.com/search/results/people/?keywords=react&origin=SWITCH_SEARCH_VERTICAL&sid=Hqb", "filter": "54", "type":"seach_url"}
#], "steps": [], "selectedLinkedinAccount": "c4a6b075-a5d8-4d70-8e9f-be0688c1dd8c", "workspace_id": "89a2208d-aa45-491e-aed7-9da1a283afbe", "uid": "e53550d3-b6b6-49cd-aa32-6f6eaa421360", "campType": "2", "extras": {"premiumAccountOnly": False, "linkTracking": False, "emailOnly": False, "moveProspects": False, "includeProspects": False}, "status": "error", "progress":0
#}

# type 2
# a = {  "campaign_id": "d7c5deba-bd68-4ca4-850a-4987df60ba9c", "name": "For Deepak 2", "searchItems": [{"query": "https://www.linkedin.com/search/results/people/?keywords=react&origin=SWITCH_SEARCH_VERTICAL&sid=Hqb", "filter": "50", "type":"seach_url"}
# ], "steps": [{"name": "Send Connection Request", "msg": "", "waitDays": {"$numberInt": "0"}, "waitHours": {"$numberInt": "0"}, "key":"send_connection_request"}
# ], "selectedLinkedinAccount": "c4a6b075-a5d8-4d70-8e9f-be0688c1dd8c", "workspace_id": "89a2208d-aa45-491e-aed7-9da1a283afbe", "uid": "e53550d3-b6b6-49cd-aa32-6f6eaa421360", "campType": "1", "extras": {"premiumAccountOnly": False, "linkTracking": False, "emailOnly": False, "moveProspects": False, "includeProspects": False}, "status": "error", "progress": 0
# }

# type 3
a = {"campaign_id":"2796f466-6773-4e3a-8cfd-18da0d8cdce2","name":"For Deepak 5","searchItems":
    [{"query":"https://www.linkedin.com/sales/search/people?query=(spellCorrectionEnabled%3ATrue%2Ckeywords%3Ad365)&sessionId=pS1bJR0bSGOOuY5xXVSAAg%3D%3D",
    "filter":"10","type":"navigator_list_url"}],
    "steps":[{"name":"Send Connection Request","msg":"","waitDays":0,"waitHours":0,"key":"send_connection_request"},{"name":"Send Message","msg":"{last_name}","waitDays":0,"waitHours":0,"key":"send_message"},{"name":"Send InMail","subject":"Hii","msg":"This and This","allowCredits":True,"waitDays":0,"waitHours":0,"key":"send_inmail"}],"selectedLinkedinAccount":"c4a6b075-a5d8-4d70-8e9f-be0688c1dd8c","workspace_id":"89a2208d-aa45-491e-aed7-9da1a283afbe","uid":"e53550d3-b6b6-49cd-aa32-6f6eaa421360","campType":"1","extras":{"premiumAccountOnly":False,"linkTracking":False,"emailOnly":False,"moveProspects":False,"includeProspects":False},"status":"error","progress":0}

results =[]

if (len (a["searchItems"]) <= 0):
  print ("No search Items")
    #return response({message:"No search Items")
for i in a["searchItems"]:
    #get data of 1st page
    
    users = [{"name":"any"},{"name":"any"}]
    
    for j in users:
        searchData = j
        
        stepsResults = []
    
        if (len(a["steps"]) <= 0):
            results.append("data") 
            continue
        else:
            for k in a["steps"]:
                if k["key"] == "send_connection_request":
                    data = step1 ("account data", k)
                    stepsResults.append(data)
                
                if k["key"] == "send_message":
                    data = step2 ("account data", k)
                    stepsResults.append(data)
                    
                if k["key"] == "send_inmail":
                    data = step3 ("account data", k)
                    stepsResults.append(data)
            
            searchData["steps"] = stepsResults
            results.append(searchData)
       
print(results)
