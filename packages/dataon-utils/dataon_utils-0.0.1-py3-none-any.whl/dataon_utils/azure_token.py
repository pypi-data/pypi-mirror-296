def get_access_token(
    tenant_id, client_id, client_secret
):  # function to get token, used to beable to call the ms graph api
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"  # setting the url to auth
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }  # setting the header
    body = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
    }  # setting the body with the requried information

    response = requests.post(
        url, headers=headers, data=body
    )  # call the api to get token
    response.raise_for_status()  # checking the status of the api call
    return response.json().get("access_token")  # return the token