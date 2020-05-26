import requests
import argparse


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", choices=['dev', 'live'],
                        help="Select environment")
    return parser.parse_args()


def enableAcronym(endpoint, acronym):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        }
    response = requests.get(endpoint+acronym, headers=headers)
    print(acronym, response.status_code)
    return response


def getTopicArn(env):
    if env == "live":
        return 'https://recs-reviewers-recommender.api.recs.d.elsevier.com/recommendations/journals/enable/'
    elif env == "dev":
        return 'https://recs-reviewers-recommender.api.dev.recs.d.elsevier.com/recommendations/journals/enable/'
    else:
        raise Exception('Invalid env: {}'.format(env))


if __name__ == '__main__':
    args = parseArguments()
    topic = getTopicArn(args.env)

    with open("acronyms.txt", "r") as f:
        data = f.readlines()
    for acronym in data:
        enableAcronym(topic, acronym.strip("\n"))
