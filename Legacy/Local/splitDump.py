import json
import os
import sha3


def readjsonfile(filepath):
    with open(filepath) as json_file:
        return json_file.readlines()


def readdir(dirname):
    return [z for x, y, z in os.walk(dirname)][0]


def processfiles(lines):
    for index, line in enumerate(lines):
        data = json.loads(line)
        manid = data["manuscriptId"]
        acronym = manid.split("_")[0]
        data.update({'journal': {'acronym': acronym}})
        with open("updated/" + manid + ".json", "w") as f:
            f.write(json.dumps(data))
        print(acronym, index)


def filterfiles(lines):
    for line in lines:
        filepath = "manuscripts/" + line
        data = json.loads(readjsonfile(filepath)[0])
        acronym = data["journal"]["acronym"]
        if acronym == "DUMMY":
            print(filepath)
            os.remove(filepath)


if __name__ == "__main__":
    with open("reviewers.1575255044307.txt") as lines:
        for index, line in enumerate(lines):
            data = json.loads(line)
            email = data["email"]
            hash = sha3.sha3_256(email.encode('utf-8')).hexdigest()
            with open("/mnt1/reviewers/split/" + hash.upper() + ".json", "w") as f:
                f.write(json.dumps(data))
            print(email, index)