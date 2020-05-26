import os
import zlib
import json
import base64
import boto3
import argparse

SNS = boto3.client('sns')


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Select environment")
    parser.add_argument("path", type=str,
                        help="Path to json files")
    parser.add_argument("limit", type=int,
                        help="Number of manuscripts to submit")
    return parser.parse_args()


def compressMsg(msg):
    compressed = zlib.compress(msg.encode('UTF-8'))
    encoded = base64.b64encode(compressed)
    return encoded.decode('UTF-8')


def readJsonFile(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        data['action'] = "new"
    return compressMsg(json.dumps(data))


def sendToSNS(msg):
    response = SNS.publish(
        TopicArn=TOPIC_ARN,
        Message=msg,
        Subject='PerformanceTest'
    )
    return response['ResponseMetadata']['HTTPStatusCode']


def getAcc(env):
    if env == "live":
        return "589287149623"
    elif env == "dev":
        return "975165675840"


def main():
    counter = 0
    for fileName in os.listdir(PATH):
        if '.json' in fileName:
            response = sendToSNS(readJsonFile(PATH + fileName))
            counter += 1
            if response != 200:
                print(response, counter, fileName)
            if counter == LIMIT:
                break
    print(counter, fileName)


def statuses():
    print(len(set(os.listdir(PATH))))


if __name__ == '__main__':
    args = parseArguments()
    TOPIC_ARN = "arn:aws:sns:us-east-1:{}:recs-rev-manuscripts-data-pump-mock".format(getAcc(args.env))
    LIMIT = args.limit
    PATH = args.path
    main()
