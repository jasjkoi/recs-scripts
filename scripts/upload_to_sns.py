import os
import json
import boto3
import argparse
from utils.sns_helper import compress_msg, send_to_sns
from utils.env_helper import get_account_number

SNS = boto3.client('sns')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Select environment")
    parser.add_argument("path", type=str,
                        help="Path to json files")
    parser.add_argument("limit", type=int,
                        help="Number of manuscripts to submit")
    return parser.parse_args()


def process_json_file(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        data['action'] = "new"
    return compress_msg(json.dumps(data))


def load_files_to_sns(topic_arn, path, limit):
    counter = 0
    for fileName in os.listdir(path):
        if '.json' in fileName:
            response = send_to_sns(SNS, process_json_file(path + fileName), topic_arn)
            counter += 1
            print(response, counter, fileName)
            if counter == limit:
                break


if __name__ == '__main__':
    args = parse_arguments()
    topic = "arn:aws:sns:us-east-1:{}:recs-rev-manuscripts-data-pump-mock".format(get_account_number(args.env))
    load_files_to_sns(topic, args.path, args.limit)
