import requests
import json
import time


tenant_id = "<>"
client_id = "<>"
client_secret = "<>"
resource = "https://management.azure.com"
subscription_id = "<>"
grant_type = "client_credentials"

aksResourceGroup = "<>"
aksClusterName = "<>"
aksAgentPoolName = "<>"

minNodeCount = 1
maxNodeCount = 1

sleepTimeInSecs = 60
retryCtr = 5


# Function to Fetch AccessToken

def fetchAccessToken(tenant_id, client_id, client_secret, resource, subscription_id, grant_type):

    accessToken = ""

    try: 

        accessTokenURL = "https://login.microsoftonline.com/"+tenant_id+"/oauth2/token"

        accessTokenHeaders = {"Content-Type":"application/x-www-form-urlencoded"}

        accessTokenReqBody = {"tenant_id":tenant_id, "client_id":client_id, "client_secret":client_secret, "resource":resource, "subscription_id":subscription_id, "grant_type":grant_type}

        tokenResponse = requests.post(url=accessTokenURL, data=accessTokenReqBody, headers=accessTokenHeaders)

        tokenResponseJson = json.loads(tokenResponse.text)

        accessToken = tokenResponseJson["access_token"]

#    print(tokenResponse.json())

#    print(tokenResponseJson["access_token"])


    except: 
        print("Error while fetching the access token!")
        return accessToken


    print ("AccessToken fetched!") 

    return accessToken



# Function to Disable AutoScaling

def disableAutoScaling(subscription_id, aksResourceGroup, aksClusterName, aksAgentPoolName, accessToken):

    try: 
       aksNodePoolMgmtURL = "https://management.azure.com/subscriptions/"+subscription_id+"/resourceGroups/"+aksResourceGroup+"/providers/Microsoft.ContainerService/managedClusters/"+aksClusterName+"/agentPools/"+aksAgentPoolName+"?api-version=2020-02-01"

       nodePoolMgmtHeaders = {"Authorization":"Bearer "+accessToken, "Content-Type":"application/json"}

       nodePoolMgmtBodyPy = { "properties": {
                                           "enableAutoScaling": False
                                       } }

       nodePoolMgmtBody = json.dumps(nodePoolMgmtBodyPy)

       nodePoolMgmtResponse = requests.put(url=aksNodePoolMgmtURL, data=nodePoolMgmtBody, headers=nodePoolMgmtHeaders)

#    print(nodePoolMgmtResponse.json())
    except:
       print("Not able to disable autoscaling!")
       return False
       
       
    print("AutoScaling disabled!")

    return True



# Function to Set Node Count

def setNodeCount(sleepInterval, retryCtr, subscription_id, aksResourceGroup, aksClusterName, aksAgentPoolName, accessToken, nodeCount):

    try:

        while retryCtr > 0:
            time.sleep(sleepInterval)

            aksNodePoolMgmtURL = "https://management.azure.com/subscriptions/"+subscription_id+"/resourceGroups/"+aksResourceGroup+"/providers/Microsoft.ContainerService/managedClusters/"+aksClusterName+"/agentPools/"+aksAgentPoolName+"?api-version=2020-02-01"

            nodePoolMgmtHeaders = {"Authorization":"Bearer "+accessToken, "Content-Type":"application/json"}
  

            nodePoolMgmtBodyPy = { "properties": {
                                                "enableAutoScaling": False,
                                                "count" : nodeCount
                                                } }

            nodePoolMgmtBody = json.dumps(nodePoolMgmtBodyPy)
  
            nodePoolMgmtResponse = requests.put(url=aksNodePoolMgmtURL, data=nodePoolMgmtBody, headers=nodePoolMgmtHeaders)

            print(nodePoolMgmtResponse.json())


            nodePoolMgmtResponseJson = json.loads(nodePoolMgmtResponse.text)


            if 'code' not in nodePoolMgmtResponseJson:
#            print(nodePoolMgmtResponse.json())
                print("Node count set successfully!")
                return True
                break

            retryCtr -= 1

    except: 
        print("Error while setting the node count!")


    print("Not able to set the node count ")

    return False   



# Fetch AccessToken

accessToken = fetchAccessToken(tenant_id, client_id, client_secret, resource, subscription_id, grant_type)


# Disable autoscaling 

autoScalingStatus = disableAutoScaling(subscription_id, aksResourceGroup, aksClusterName, aksAgentPoolName, accessToken)


# Set the nodeCount to 1

nodeCountSetStatus = setNodeCount(sleepTimeInSecs, retryCtr, subscription_id, aksResourceGroup, aksClusterName, aksAgentPoolName, accessToken, minNodeCount)



