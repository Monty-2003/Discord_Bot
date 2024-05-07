import json
import requests
import pandas as pd
from bs4 import BeautifulSoup # used to parse data returned from api request in html format


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
    result_html = response.text # API response happens to be in html -__-

    return result_html



def convert_to_df(html_data):
    # Parse the HTML data
    soup = BeautifulSoup(html_data, 'html.parser')

    # Find all <i> tags
    i_tags = soup.find_all('i')

    # There are 9 variables, so 9 <i> tags for each observatio
    all_data = []

    # Iterate through every 9 <i> tags
    for i in range(0, len(i_tags), 9):
        # Initialize data dictionary for each observation
        data = {}
        # Iterate through each <i> tag
        for j in range(9):
            idx = i + j
            if idx < len(i_tags):
                key = i_tags[idx].text.strip().replace(':', '')
                # Check if there's a next sibling element
                next_sibling = i_tags[idx].find_next_sibling(text=True)
                value = None
                if next_sibling:
                    value = next_sibling.strip()
                else:
                    data[key] = None

                # Special handling for RecordID because it is nested <a>
                if key == 'RecordID':
                    a_tag = i_tags[idx].find_next_sibling('a')
                    if a_tag and 'href' in a_tag.attrs:
                        value = a_tag['href'].split('/')[-1]  # Extract the number from the href attribute

                data[key] = value
        # Append data for each observation to the list
        all_data.append(data)

    # Convert data list into a pandas DataFrame
    df = pd.DataFrame(all_data)

    return df



def get_crime_data():
    # get url response and convert data from html into pandas df
    url = "https://gisweb.charlottesville.org/arcgis/rest/services/OpenData_2/MapServer/6/query?outFields=*&where=1%3D1"

    result_html = get_api_response(url) 
    result_df = convert_to_df(result_html)

    # return data in df to be handled in db_ingestion
    return result_df