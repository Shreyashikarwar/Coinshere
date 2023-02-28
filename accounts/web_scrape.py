import requests

# Executed only one time for fetching organization data

def fetch_organization_data(organization_id):
    payload={"organization_id":organization_id}
    
    response=requests.get("https://www.organization.com",params=payload)
    
    res=response.json()
    return res


def fetch_organization_performance_data(organization_id):
    payload={"organization_id":organization_id}
    
    response=requests.get("https://www.organization.com",params=payload)
    
    res=response.json()
    return res

