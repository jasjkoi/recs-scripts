import boto3
import json
import argparse
from aws.sns_helper import compress_msg, send_to_sns
from utils.env_helper import get_account_number

SNS = boto3.client('sns')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Select environment")
    parser.add_argument("email", type=str,
                        help="Add reviewer email")
    return parser.parse_args()


def generate_msg(uid):
    return json.dumps({"action": "remove", "email": uid})


if __name__ == '__main__':
    args = parse_arguments()
    topic = "arn:aws:sns:us-east-1:{}:recs-rev-reviewers-data-pump-mock".format(get_account_number(args.env))
    resp = send_to_sns(compress_msg(generate_msg(args.email)), SNS, topic)
    print(resp)
