import zlib
import base64
import boto3
import json
import argparse
from datetime import datetime


SNS = boto3.client('sns')


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Select environment")
    return parser.parse_args()


def compressMsg(msg):
    compressed = zlib.compress(msg.encode('UTF-8'))
    encoded = base64.b64encode(compressed)
    return encoded.decode('UTF-8')


def generateMsg(uid):
    return json.dumps({"action": "resubmit", "manuscriptId": uid})


def sendToSNS(msg, topic):
    response = SNS.publish(
        TopicArn=topic,
        Message=msg
    )
    return response['ResponseMetadata']['HTTPStatusCode']


def getAcc(env):
    if env == "live":
        return "589287149623"
    elif env == "dev":
        return "975165675840"


def isOverTimeStamp(last_modified, start_date):
    return last_modified.replace(tzinfo=None) > start_date


def listS3Objects(bucket_object, prefix, start_date):
    return [i.key.split("/")[1] for i in bucket_object.objects.filter(Prefix=prefix)
            if isOverTimeStamp(i.last_modified, start_date)]


def generateManuscriptList(env):
    s3 = boto3.resource("s3")
    reviewers_bucket = s3.Bucket('com-elsevier-recs-{}-reviewers'.format(env))
    reviewers_prefix = 'submitted-manuscripts'

    valid_period_start = datetime.strptime('2020-03-11 09:47', "%Y-%m-%d %H:%M")
    return listS3Objects(reviewers_bucket, reviewers_prefix, valid_period_start)


def resubmit(topic, env):
    for count, uid in enumerate(generateManuscriptList(env)):
        msg = compressMsg(generateMsg(uid))
        resp = sendToSNS(msg, topic)
        print(count, resp, uid)


if __name__ == '__main__':
    args = parseArguments()
    topic_arn = "arn:aws:sns:us-east-1:{}:recs-rev-manuscripts-data-pump-mock".format(getAcc(args.env))
    resubmit(topic_arn, args.env)
