import os
from .file_reader import PROJECT_PATH


def data_dir_check():
    data_dir = PROJECT_PATH / 'data'
    if os.path.exists(data_dir):
        pass
    else:
        os.mkdir(data_dir)


def s3_download(s3_client, bucket, prefix, filename):
    data_dir_check()
    key = prefix + '/' + filename
    dl_path = str(PROJECT_PATH / 'data/{}'.format(filename))
    s3_client.download_file(bucket, key, dl_path)
