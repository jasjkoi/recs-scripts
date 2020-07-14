import boto3

if __name__ == '__main__':
    failed_recs = []

    s3 = boto3.resource('s3')
    bucket_name = "com-elsevier-recs-live-reviewers"
    for rec in failed_recs:
        key = 'submitted-manuscripts/' + rec + '.json'
        copy_source = {
            'Bucket': bucket_name,
            'Key': key
         }
        try:
            s3.meta.client.copy(copy_source, bucket_name, key, ExtraArgs={'ServerSideEncryption': 'AES256'})
            print(copy_source, bucket_name, key)
        except Exception as e:
            print(e)
            continue
