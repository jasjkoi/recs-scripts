import boto3
import os


def readdir(dirname):
    return [z for x, y, z in os.walk(dirname)][0]


def readTxt(path):
    with open(path, "r") as f:
        data = f.readlines()
    return [x.strip("\n") for x in data]


def uploadToS3(directory, toKeep):
    s3 = boto3.resource('s3')
    data = set(readdir(directory))
    for index, manuscript in enumerate(data):
        if manuscript not in toKeep:
            pathToUpload = directory + "/" + manuscript
            key = "raw/manuscripts/" + manuscript
            s3.meta.client.upload_file(pathToUpload,
                'com-elsevier-recs-live-reviewers',
                key,
                ExtraArgs={'ServerSideEncryption':'AES256'}
                )
            print(manuscript, key, index)

if __name__ == '__main__':
    toKeep = readTxt("keep.txt")
    directory = "updated"
    uploadToS3(directory, toKeep)

