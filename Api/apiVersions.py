import sys
import json
import boto3
import argparse
import pandas as pd
from boto3.dynamodb.conditions import Key, Attr


ecr = boto3.client('ecr')
dynamoDB = boto3.resource('dynamodb')


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Uses ecr mapping for dev")
    return parser.parse_args()


def get_dynamo(itemName):
    response = dynamoDB.Table('api-version-history').query(
        KeyConditionExpression=Key('api_name').eq(itemName),
        ScanIndexForward=False,
        Limit=1
        )['Items']
    if response:
        r_data = response[0]
        return [r_data['api_version'],
                r_data['dataset_version'],
                r_data['deploy_time']]
    else:
        return [None for i in range(0, 3)]


def get_ecr_versions(env):
    if env == 'dev':
        with open('ecrMap.json', 'r') as file:
            mapping = json.load(file)
        return mapping

    if env == 'live':
        mapping = {}
        repos = [x['repositoryName']
                 for x in ecr.describe_repositories()['repositories']
                 if 'api/' in x['repositoryName']]

        for i in repos:
            versions = [x['imageTag']
                        for x in ecr.list_images(repositoryName=i)['imageIds']
                        if len(x) > 1]

            result = ([x for x in versions if x != 'latest'])
            if result:
                mapping.update({i[4:]: max(result)})
    # Stores mapping locally to allow script to be run against dev environment
        with open('ecrMap.json', 'w') as file:
            file.write(json.dumps(mapping))
        return mapping


def make_report(env):
    try:
        ecrData = get_ecr_versions(env)
    except(FileNotFoundError):
        sys.exit('Error: Generate mapping by running script against live')

    cols = ['api', 'ecr_v', 'dynamo_v', 'dataset_v', 'deploy_time']
    data = [[api[0], api[1]] + get_dynamo(api[0]) for api in ecrData.items()]
    print(pd.DataFrame(data, columns=cols))

if __name__ == '__main__':
    args = parseArguments()
    make_report(args.env)
