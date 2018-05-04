# # Library of Congress Collections & the Zooniverse Project Builder
# 
# #### Zooniverse Hackday - April 12th 2018
# 
# ## Goals
# 
# Given a url to a collection in the Library of Congress's digital collections, this script will request the collection in json format. With this information, the script will make additional calls to request the url of the item images and metadata associated with each item in a collection. For each image and it's associated metadata, the script will create a new Project Build (i.e., Panoptes) subject and attach the subject to an existing subject set.
# 
# ## Script Inputs
# - URL to a Library of Congress digital collection (e.g., https://www.loc.gov/collections/anna-maria-brodeau-thornton-papers)
# - Zooniverse subject set id
# - Zooniverse account

import requests
import time
import json
import pdb
from panoptes_client import Panoptes

# Panoptes.connect(username=%env PANOPTES_USERNAME, password=%env PANOPTES_USERNAME)

# Based on the method from 
# https://github.com/LibraryOfCongress/data-exploration/blob/master/Accessing%20images%20for%20analysis.ipynb
# The documentation for https://libraryofcongress.github.io/data-exploration/requests.html#format
# I thought we could get the segments faster using the item, but can't figure out how to do so for this collection.
def get_image_urls(url, items=[]):
    '''
    Retrieves the image URLs and metadata for items that have public URLs available. 
    Skips over items that are for the colletion as a whole or web pages about the collection.
    '''
    # request pages of 100 results at a time
    params = {"fo": "json", "c": 100, "at": "results,pagination"}
    call = requests.get(url, params=params)
    data = call.json()
    results = data['results']
    # Selecting the 4th item in the collection.
    # Can we request the item directly?
    result = results[4]
    
    # don't try to get images from the collection-level result
    if "collection" not in result.get("original_format") and "web page" not in result.get("original_format"):
        # take the last URL listed in the image_url array
        segmentBaseUrl = result['segments'][0]['url']
        segmentCount = result['segments'][0]['count']
        
        for spNum in range(1, segmentCount):
            subject = {}
            
            segmentUrl = segmentBaseUrl + '?sp='+ str(spNum) + '&fo=json'
            
            segCall = requests.get(segmentUrl, {"fo": "json"})
            time.sleep(1)
            segData = segCall.json()
            rawSegLocation = segData['segments'][0]['image_url'][-1]
            segLocation = 'https://' + rawSegLocation[2:-1]

            subject['location'] = segLocation
            subject['metadata'] = {'cite_this': segData['cite_this']['apa'], 'contributor': segData['segments'][0]['contributor'][0], 'date': segData['segments'][0]['date']}
            
            items.append(subject)
            
    return items

images = get_image_urls('https://www.loc.gov/collections/anna-maria-brodeau-thornton-papers', items = [])
for image in itemImages:
    print(image)