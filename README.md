# AKSNodePoolScaling
Python based scripts to set the scaling rules for an AKS node pool

## Need
On the Dev/Test environments for AKS where we dont need the node pools to be running a high number of nodes all the time, it is desired that the node pools should be scaled down at the end of the business day .. and to be scaled up during start of the business day. The Python scripts **nodescaledown.py** and **nodescaleup.py** can be used for the same. These scripts can be run at the desired time using Azure Automation or Crontab.

## Working 
There are two Python scripts present as follows: <br />
**nodescaledown.py:** Python script for scaling doen the AKS node pool <br />
**nodescaleup.py:** Python script for scaling doen the AKS node pool <br />

Both the Python scripts need an Azure Active Directory service principal to be created -- https://docs.microsoft.com/en-us/cli/azure/ad/sp?view=azure-cli-latest#az-ad-sp-create-for-rbac . <br />
The default command for the same is: <br />
az ad sp create-for-rbac -n "<sp_name>"

The above command gives the below output: <br />
{ "appId": "", "displayName": "<sp_name>", "name": "http://<sp_name>", "password": "<sp_password>", "tenant": "<tenant_id>" }

In both the scripts the service principal details (obtained in the above step) and the AKS cluster and node pool details need to be entered. <br />
Using the service principal details, the both the scripts fetch the Access Token. Using this Access Token, the Azure Management APIs for AKS are used to scale up or scale down the NodePool size. 

## nodescaledown.py
After the Access Token is fetched, the autoscaling is disabled and the node count is set to minNodeCount. 

## nodescaleup.py
After the Access Token is fetched, the autoscaling is enabled and the scaling rules are set as per the values defined for minNodeCount and maxNodeCount.   
