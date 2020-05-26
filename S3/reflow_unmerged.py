import boto3
import os
import json
import sys
import pandas as pd

S3 = boto3.client('s3')
BUCKET_NAME = 'com-elsevier-recs-live-reviewers'
PREFIX = 'raw/manuscripts/'


def updateJsonFile(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        try:
            merged_authors = [data['authors']['corresponding']] + data['authors']['coauthors']
            data['authors'] = merged_authors
        except TypeError as t:
            if isinstance(data['authors'], list):
                pass
            else:
                print(t)
                sys.exit(1)

    dest = 'updated/'+filepath.split('/')[1]
    with open(dest, 'w') as f:
        json.dump(data, f)
        print(dest)


def download_deltas():
    deltas = pd.read_csv("~/Downloads/corrupt_manuscript_id.csv", names=["id"])['id'].tolist()
    for c, delta in enumerate(deltas):
        filename = delta + '.json'
        try:
            S3.download_file(BUCKET_NAME, PREFIX+filename, 'data/'+filename)
            print(c, filename)
        except:
            print(filename + " Not Found")


def update_deltas():
    for fileName in os.listdir('data'):
        if '.json' in fileName:
            updateJsonFile('data/'+fileName)


if __name__ == '__main__':
    update_deltas()