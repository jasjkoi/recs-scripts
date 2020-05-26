import re
import boto3
import logging
import requests
import argparse
from datetime import datetime


ENDPOINT = 'https://recs-reviewers-recommender.dev.d.elsevier.com/recommendations/journals/enable/'

S3 = boto3.client('s3')
logging.getLogger().setLevel(logging.INFO)
logging.info('Sending to {}'.format(ENDPOINT))


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return 0


def parseResponseText(respText):
    return re.findall('Resubmitting ([1-9][0-9]*)|Skipped ([0-9]+)',
                      respText)


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("manuscripts", type=int,
                        help="Number of manuscrpts to be submitted through api")
    return parser.parse_args()


def logTime():
    logging.info('Submitting at: {}'.format(datetime.now()))


def getLatest():
    prefixes = S3.list_objects_v2(Bucket='com-elsevier-recs-dev-reviewers',
                                  Prefix='manuscripts-for-resubmission',
                                  Delimiter='/data')

    return prefixes['CommonPrefixes'][-1]['Prefix'].split('/')[1]


def countManuscripts(prefix):
    return S3.list_objects_v2(Bucket='com-elsevier-recs-dev-reviewers',
                              Prefix=prefix,
                              Delimiter='/part')['KeyCount']


def enableAcronym(acronym):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        }
    response = requests.get(ENDPOINT+acronym, headers=headers)
    resp_data = sum([to_int(x[0]) if x[0] else to_int(x[1])*-1
                      for x in parseResponseText(response.text)])
    logging.info('Enabling {} ({} manuscripts)'.format(acronym, resp_data))
    logging.info(response.status_code)
    return resp_data


def fetchAcronyms(maxManuscripts):
    logTime()
    latestPerfix = 'manuscripts-for-resubmission/{}'.format(getLatest())
    prefixes = S3.list_objects_v2(Bucket='com-elsevier-recs-dev-reviewers',
                                  Prefix=latestPerfix,
                                  Delimiter='/manuscript')['CommonPrefixes']
    manTotal = 0
    for prefix in prefixes:
        manCount = enableAcronym(re.search('[A-Z]+', prefix['Prefix']).group(0))
        manTotal += manCount

        if manTotal > maxManuscripts:
            break

    logging.info('Submitted {} manuscripts'.format(manTotal))


if __name__ == '__main__':
    args = parseArguments()
    fetchAcronyms(args.manuscripts)
    logTime()
