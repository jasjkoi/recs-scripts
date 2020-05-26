import os


def read_dir(dir_name):
    return [z for x, y, z in os.walk(dir_name)][0]


def read_txt(file_path):
    with open(file_path, "r") as f:
        return [line.strip("\n") for line in f.readlines()]


if __name__ == "__main__":

    local_manuscripts = read_dir("updated")
    s3_manuscripts = set(read_txt("current.txt"))
    count = 0

    for manuscript in local_manuscripts:
        if manuscript in s3_manuscripts:
            fp = "updated/" + manuscript
            os.remove("updated/" + manuscript)
            count += 1
            print(fp, count)



