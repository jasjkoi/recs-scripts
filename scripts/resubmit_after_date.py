import boto3
import json
import argparse
from datetime import datetime
from utils.sns_helper import send_to_sns, compress_msg
from utils.env_helper import get_account_number

SNS = boto3.client('sns')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Select environment")
    parser.add_argument("date", type=lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M'),
                        help="Enter date 'YYYY-MM-DD hh:mm' | for example: '2020-03-21 00:00'")
    return parser.parse_args()


def generate_msg(uid):
    return json.dumps({"action": "resubmit", "manuscriptId": uid})


def is_over_timestamp(last_modified, start_date):
    return last_modified.replace(tzinfo=None) > start_date


def list_s3_objects(bucket_object, prefix, start_date):
    return [i.key.split("/")[1] for i in bucket_object.objects.filter(Prefix=prefix)
            if is_over_timestamp(i.last_modified, start_date)]


def generate_manuscript_list(env, start_date):
    s3 = boto3.resource("s3")
    reviewers_bucket = s3.Bucket('com-elsevier-recs-{}-reviewers'.format(env))
    reviewers_prefix = 'submitted-manuscripts'
    object_list = list_s3_objects(reviewers_bucket, reviewers_prefix, start_date)
    print('Found {} objects since {}'.format(len(object_list), start_date))
    return object_list


def resubmit(topic, env, start_date):
    for count, uid in enumerate(generate_manuscript_list(env, start_date)):
        msg = compress_msg(generate_msg(uid))
        resp = send_to_sns(SNS, msg, topic)
        print(count, resp, uid)


if __name__ == '__main__':
    args = parse_arguments()
    topic_arn = "arn:aws:sns:us-east-1:{}:recs-rev-manuscripts-data-pump-mock".format(get_account_number(args.env))
    resubmit(topic_arn, args.env, args.date)
