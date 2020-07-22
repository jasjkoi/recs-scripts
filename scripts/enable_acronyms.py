import requests
import argparse
from utils.file_reader import get_list_from_resources


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Select environment")
    return parser.parse_args()


def enable_acronym(endpoint, acronym):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        }
    response = requests.get(endpoint+acronym, headers=headers)
    print(acronym, response.status_code)
    return response


def get_topic_arn(env):
    if env == "live":
        return 'https://recs-reviewers-recommender.api.recs.d.elsevier.com/recommendations/journals/enable/'
    elif env == "dev":
        return 'https://recs-reviewers-recommender.api.dev.recs.d.elsevier.com/recommendations/journals/enable/'
    else:
        raise Exception('Invalid env: {}'.format(env))


if __name__ == '__main__':
    args = parse_arguments()
    topic = get_topic_arn(args.env)

    for acronym in get_list_from_resources('acronyms.txt'):
        enable_acronym(topic, acronym)
