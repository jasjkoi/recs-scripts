import boto3
import argparse
from utils.file_reader import get_list_from_resources, PROJECT_PATH
from utils.s3_helper import s3_download

S3 = boto3.client('s3')
PREFIX = 'submitted-manuscripts'


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Select environment")
    return parser.parse_args()


def download_manuscripts(bucket_name):
    manuscripts = get_list_from_resources('manuscripts.txt')
    for c, manuscript in enumerate(manuscripts):
        try:
            s3_download(S3, bucket_name, PREFIX, manuscript)
            print(c, manuscript)
        except Exception as e:
            print(manuscript + " Not Found ", e)


if __name__ == '__main__':
    args = parse_arguments()
    bucket = 'com-elsevier-recs-{}-reviewers'.format(args.env)
    download_manuscripts(bucket)
