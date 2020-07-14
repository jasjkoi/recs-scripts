import boto3

S3 = boto3.client('s3')
BUCKET_NAME = 'com-elsevier-recs-live-reviewers'
PREFIX = 'submitted-manuscripts/'


def download_deltas():
    deltas = []
    for c, delta in enumerate(deltas):
        try:
            S3.download_file(BUCKET_NAME, PREFIX+delta, 'data/'+delta)
            print(c, delta)
        except:
            print(delta + " Not Found")


if __name__ == '__main__':
    download_deltas()
