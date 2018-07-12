import requests
import json
import os
from panoptes_client import Panoptes, Project, SubjectSet, Subject

LIBRARY_OF_CONGRESS_ITEM_ID = 'mss5186201' # item ID, set to 'mss5186201' for demonstration purposes, see README

USERNAME = os.getenv('PANOPTES_USERNAME') # your Zooniverse username, set via environment variable by default, or feel free to hardcode
PASSWORD = os.getenv('PANOPTES_PASSWORD') # your Zooniverse password, set via environment variable by default, or feel free to hardcode
PROJECT = '1234' # your Zooniverse project ID
ENDPOINT = 'https://panoptes.zooniverse.org' # production = 'https://panoptes.zooniverse.org', staging = 'https://panoptes-staging.zooniverse.org'

def transform_item_segments(url, segments = []):
    print("Begin transforming item segements...")
    params = {"fo": "json"}
    call = requests.get(url, params=params)
    data = call.json()

    FILE_INDEX = 5 # see README
    
    # BEGIN DEFINE METADATA FROM ITEM, edit/add/delete the following based on your item and desired uses, update DEFINE ZOONIVERSE SUBJECT METADATA below accordingly
    
    apa_citation = data['cite_this']['apa']
    item_date = data['item']['date']
    loc_id = data['item']['id']
    source_collection = data['item']['source_collection']
    item_title = data['item']['title']
    
    # END DEFINE METADATA FROM ITEM

    for resource in data['resources']:
        for file in resource['files']:
            segment = {}
            
            url = file[FILE_INDEX]['url']
            mimetype = file[FILE_INDEX]['mimetype']
            segment['location'] = {}
            segment['location'][mimetype] = url
            
            # DEFINE ZOONIVERSE SUBJECT METADATA, corresponds to METADATA FROM ITEM above, update both accordingly
            segment['metadata'] = {
                'APA Citation': apa_citation,
                'Date': item_date,
                'Library Of Congress Item ID': loc_id,
                'Source Collection': source_collection,
                'Title': item_title
            }

            segments.append(segment)
    print('Item segments transformation complete.')
    return segments

segments = transform_item_segments('https://www.loc.gov/item/' + LIBRARY_OF_CONGRESS_ITEM_ID)

Panoptes.connect(username=USERNAME, password=PASSWORD, endpoint=ENDPOINT)

project = Project.find(PROJECT)

subject_set = SubjectSet()
subject_set.links.project = project
subject_set.display_name = segments[0]['metadata']['Title'] # uses item Title as default subject set name, or feel free to hardcode
subject_set.save()

print('Begin Zooniverse subject upload...')
for segment in segments:
    subject = Subject()

    subject.links.project = project
    subject.add_location(segment['location'])

    subject.metadata.update(segment['metadata'])

    subject.save()
    subject_set.add(subject)

print("Zooniverse subject upload complete.")
