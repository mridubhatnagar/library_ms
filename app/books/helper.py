from flask import current_app as app
import requests 
import json

def query_books_api(request, page):
    query_parameters_string = ""
    for key in request.keys():
        if key != "quantity":
            if len(request[key])>0:
                query_parameters_string += "{}={}&".format(key, request[key])
    if query_parameters_string.endswith("&"):
        query_parameters_string = query_parameters_string[:-1]
    query_parameters_string += f"&page={page}"
    print(app.config['FRAPPE_BASE_API_ENDPOINT'] + query_parameters_string)
    api_endpoint_url = app.config['FRAPPE_BASE_API_ENDPOINT'] + f"{query_parameters_string}"
    response = requests.post(api_endpoint_url)
    if response.status_code == 200:
        return json.loads(response.text) 
    else: 
        return {'error_code': response.status_code} 