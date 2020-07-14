import boto3
import zlib
import json
import base64


def compressMsg(msg):
    compressed = zlib.compress(msg.encode('UTF-8'))
    encoded = base64.b64encode(compressed)
    return encoded.decode('UTF-8')


def generateMsg(uid):
    return json.dumps({"action": "remove", "email": uid})


def sendToSNS(msg, topic_arn):
    response = boto3.client('sns').publish(
        TopicArn=topic_arn,
        Message=msg
    )
    return response['ResponseMetadata']['HTTPStatusCode']


if __name__ == '__main__':

    email = 'leszek.marynowski@us.edu.pl'

    topic = "arn:aws:sns:us-east-1:975165675840:recs-rev-reviewers-data-pump-mock"
    print(sendToSNS(compressMsg(generateMsg(email)), topic))
