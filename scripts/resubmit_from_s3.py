import boto3
import argparse
from utils.file_reader import get_list_from_resources

S3 = boto3.resource('s3')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Select environment")
    return parser.parse_args()


def resubmit_failed_manuscripts(bucket, failed_manuscripts):
    for manuscript in failed_manuscripts:
        key = 'submitted-manuscripts/' + manuscript
        copy_source = {
            'Bucket': bucket_name,
            'Key': key
         }
        try:
            S3.meta.client.copy(copy_source, bucket, key, ExtraArgs={'ServerSideEncryption': 'AES256'})
            print(copy_source, bucket_name, key)
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    args = parse_arguments()
    bucket_name = "com-elsevier-recs-{}-reviewers".format(args.env)
    manuscripts = get_list_from_resources('manuscripts.txt')
    resubmit_failed_manuscripts(bucket_name, manuscripts)
