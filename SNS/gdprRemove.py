import zlib
import json
import base64
import boto3
import os

FILENAME = "s6KCNcbf.csv" # Enter the path of a csv file downloaded from API
TOPIC_ARN = "arn:aws:sns:us-east-1:589287149623:recs-rev-manuscripts-data-pump-mock"
BUCKET_NAME = "com-elsevier-recs-live-reviewers"


SNS = boto3.client('sns')
S3 = boto3.client('s3')


def download(key):
    location = key.split('/')[2]
    try:
        S3.download_file(BUCKET_NAME, key, location)
        return location
    except Exception as e:
        print(e)
        return None


def compressMsg(msg):
    compressed = zlib.compress(msg.encode('UTF-8'))
    encoded = base64.b64encode(compressed)
    return encoded.decode('UTF-8')


def sendToSNS(msg):
    response = SNS.publish(
            TopicArn=TOPIC_ARN,
            Message=msg
            )
    return response['ResponseMetadata']['HTTPStatusCode']


def getPath(manuscriptId):
    return "raw/manuscripts/{}.json".format(manuscriptId)


def main():
    with open(FILENAME, 'r') as f:
        data = [getPath(line.split(',')[0]) for line in f.readlines()][1:]

    for manuscriptId in data:
        path = download(manuscriptId)
        if path:
            with open(path, 'r') as f:
                data = json.load(f)
            data['action'] = "remove"
            response = sendToSNS(compressMsg(json.dumps(data)))
            if response == 200:
                print(path, response)
                os.remove(path)


if __name__ == '__main__':
    main()
