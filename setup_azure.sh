#!/bin/bash  
AZURE_SUBSCRIPTION_ID=YOUR_SUBSCRIPTION_ID
az ad sp create-for-rbac --name "CICD" --role contributor --scopes /subscriptions/$AZURE_SUBSCRIPTION_ID --sdk-auth