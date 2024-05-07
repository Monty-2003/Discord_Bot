import json
import requests
import pandas as pd
#from pandas.io.json import json_normalize


def get_api_response(url):
    # Get the response fron the api and handle possible errors
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred: " + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred: " + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred: " + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred: " + repr(err)



    # Get response data
    result = response.json() 
    
    return result



def get_closure_data():
    # get url response and convert data from html into pandas df
    url = "https://gisweb.charlottesville.org/arcgis/rest/services/OpenData_1/MapServer/38/query?where=1%3D1&outFields=PROJECT_TYPE,PROJECT_NAME,CONTRACTOR,DESCRIPTION,PROJECT_STATUS,DEPARTMENT,DATE_COMPLETE,CLOSURE_START_TIME,NUM_PARKING,CLOSURE_END_TIME,CLOSURE_TYPE,PROJECT_NUMBER,LOCATION,DATE_START&returnGeometry=false&outSR=4326&f=json"

    result_json = get_api_response(url) 
    

    if 'features' in result_json:
    # Extract 'features' data
        features = result_json['features']
        
        # This process was edited/aided using ChatGPT v3.5, great for parsing data
        # Extract only the necessary properties from each feature
        data = []
        for feature in features:
            properties = feature.get('attributes', {})
            data.append({
                'PROJECT_TYPE': properties.get('PROJECT_TYPE'),
                'PROJECT_NAME': properties.get('PROJECT_NAME'),
                'CONTRACTOR': properties.get('CONTRACTOR'),
                'DESCRIPTION': properties.get('DESCRIPTION'),
                'PROJECT_STATUS': properties.get('PROJECT_STATUS'),
                'DEPARTMENT': properties.get('DEPARTMENT'),
                'DATE_COMPLETE': properties.get('DATE_COMPLETE'),
                'CLOSURE_START_TIME': properties.get('CLOSURE_START_TIME'),
                'NUM_PARKING': properties.get('NUM_PARKING'),
                'CLOSURE_END_TIME': properties.get('CLOSURE_END_TIME'),
                'CLOSURE_TYPE': properties.get('CLOSURE_TYPE'),
                'PROJECT_NUMBER': properties.get('PROJECT_NUMBER'),
                'LOCATION': properties.get('LOCATION'),
                'DATE_START': properties.get('DATE_START')
            })
        
        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data)

        return df



