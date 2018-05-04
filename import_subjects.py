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
import os
from panoptes_client import Panoptes, Project, SubjectSet, Subject

Panoptes.connect(username=os.getenv('PANOPTES_USERNAME'), password=os.getenv('PANOPTES_PASSWORD'), endpoint='https://panoptes-staging.zooniverse.org')

# Based on the method from
# https://github.com/LibraryOfCongress/data-exploration/blob/master/Accessing%20images%20for%20analysis.ipynb
# The documentation for https://libraryofcongress.github.io/data-exploration/requests.html#format
# I thought we could get the segments faster using the item, but can't figure out how to do so for this collection.
def transform_item_segments(url, subjects = []):
    print("Begin transforming item segements...")
    params = {"fo": "json"}
    call = requests.get(url, params=params)
    data = call.json()
    # The following data will used as metadata for each panoptes subject
    cite_this = data['cite_this']['apa']
    item_date = data['item']['date']
    loc_id = data['item']['id']
    source_collection = data['item']['source_collection']
    item_title = data['item']['title']

    # TODO: We want to note that resources should
    # probably be iterated through? But we are not sure.
    for resource in data['resources'][0]['files']:
        subject = {}
        # From looking at this resource, we know the 5th url
        # is what we would like to use for the project builder subject
        # However, we are not sure if this a good approach for all items.
        url = resource[5]['url']
        mimetype = resource[5]['mimetype']
        subject['location'] = {}
        subject['location'][mimetype] = url
        subject['metadata'] = {
            'APA Citation': cite_this,
            'Date': item_date,
            'Library Of Congress Item Id': loc_id,
            'Source Collection': source_collection,
            'Title': item_title
        }

        subjects.append(subject)
    return subjects

subjects = transform_item_segments('https://www.loc.gov/item/mss5186201')

project = Project.find("1841")

subject_set = SubjectSet()
subject_set.links.project = project
subject_set.display_name = subjects[0]['metadata']['Title']
subject_set.save()

for subject in subjects:
    # We want to create and save a new Panoptes subject.
    # We will have to know the Project ID and the Subject Set ID

    new_subject = Subject()

    new_subject.links.project = project
    new_subject.add_location(subject['location'])

    new_subject.metadata.update(subject['metadata'])

    new_subject.save()
    subject_set.add(new_subject)

print("Upload Complete")
