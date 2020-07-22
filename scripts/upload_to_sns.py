import os
import json
import boto3
import argparse
from utils.sns_helper import compress_msg, send_to_sns
from utils.env_helper import get_account_number

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


def readJsonFile(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        data['action'] = "new"
    return compress_msg(json.dumps(data))


def main():
    counter = 0
    for fileName in os.listdir(PATH):
        if '.json' in fileName:
            response = send_to_sns(SNS, readJsonFile(PATH + fileName), TOPIC_ARN)
            counter += 1
            if response != 200:
                print(response, counter, fileName)
            if counter == LIMIT:
                break
        print(counter, fileName)


if __name__ == '__main__':
    args = parseArguments()
    TOPIC_ARN = "arn:aws:sns:us-east-1:{}:recs-rev-manuscripts-data-pump-mock".format(get_account_number(args.env))
    LIMIT = args.limit
    PATH = args.path
    main()
