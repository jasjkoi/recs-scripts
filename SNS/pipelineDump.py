import boto3
import json
import zlib
import base64
from smart_open import open
from pprint import pprint


S3 = boto3.client('s3')
BUCKET = 'evise-recomender-data-dump'
SNS = boto3.client('sns')
LIMIT = -1


def main():
    for item in S3.list_objects_v2(Bucket=BUCKET)['Contents']:
        name = item['Key']
        if '.txt' in name:
            readKey(name, LIMIT)


def readKey(s3Key, limit):
    dumpFile = S3.get_object(Bucket=BUCKET, Key=s3Key)
    topicArn = getTopicArn(s3Key)
    print("Reading {}".format(s3Key))
    for index, line in enumerate(open(dumpFile['Body'])):
        if index == limit:
            break
        try:
            jsonData = json.loads(line)
            jsonData['action'] = "New"

            decoded = json.dumps(jsonData)
            sendToSNS(compressMsg(decoded), topicArn)
        except Exception as e:
            print(index, e)


def sendToSNS(msg, topic):
    response = SNS.publish(
            TopicArn=topic,
            Message=msg
            )
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code != 200:
        print(status_code)
    return response


def compressMsg(msg):
    compressed = zlib.compress(msg.encode('UTF-8'))
    encoded = base64.b64encode(compressed)
    return encoded.decode('UTF-8')


def getTopicArn(s3Key):
    if 'manuscripts' in s3Key:
        return "arn:aws:sns:us-east-1:589287149623:recs-rev-manuscripts-data-pump-mock"
    else:
        return "arn:aws:sns:us-east-1:589287149623:recs-rev-reviewers-data-pump-mock"


if __name__ == '__main__':
    main()
