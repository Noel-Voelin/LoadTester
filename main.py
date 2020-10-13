import re
import requests
from datetime import datetime
import time
import concurrent.futures
import os

parts = [
    r'\[.*(\d{2}:\d{2}:\d{2}).*\].*(GET|POST)\ ?(\/.*)HTTP\/',  # host %h
]
FMT = '%H:%M:%S'


def get_timestamp(entry):
    return datetime.strptime(entry[0], FMT)


def get_method(entry):
    return entry[1]


def get_path(entry):
    return entry[2]


def make_user(access_list):
    def send(entry):

        # Ternary condition
        return requests.post(host + get_path(entry)).status_code if get_method(entry) == "post" else requests.get(
            host + get_path(entry)).status_code

    host = 'https://www.ubs.com'
    endTime = None
    for entry in access_list:
        response = 500
        send(entry)
        if endTime is not None:
            timedelta = get_timestamp(entry) - datetime.strptime(endTime, FMT)
            time.sleep(timedelta.total_seconds())
        endTime = entry[0]
        print(get_path(entry) + "CODE: " + str(response))


def parse_and_sort(filepath):
    executionArray = []
    pattern = re.compile(parts[0])
    #Context manager
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            path = pattern.search(line.strip())
            if path is not None:
                pathEntry = ["{}".format(path.group(1)), "{}".format(path.group(2)), "{}".format(path.group(3))]
                executionArray.append(pathEntry)
            line = fp.readline()
    executionArray.sort(key=get_timestamp)
    return executionArray


if __name__ == '__main__':
    sorted_list_of_access_entries = parse_and_sort("access-log-1.log")
    with concurrent.futures.ProcessPoolExecutor() as executor:
         [executor.submit(make_user, sorted_list_of_access_entries) for _ in range(os.cpu_count())]


