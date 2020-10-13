import re
import requests
from datetime import datetime
import time
import glob
import concurrent.futures

FMT = '%H:%M:%S'
host = 'https://www.ubs.com'
magicRegex = r'\[.*(\d{2}:\d{2}:\d{2}).*\].*(GET|POST)\ ?(\/.*)HTTP\/'


class LogEntry:
    def __init__(self, time_stamp, method, path):
        self.time_stamp = datetime.strptime(time_stamp, FMT)
        self.method = method
        self.path = path

    def send(self):
        # Ternary condition
        return 500 #requests.post(host + self.path).status_code if self.method == "post" else requests.get(host + self.path).status_code


def start_user_traffic(access_log_path):
    end_time = None
    for entry in parse_and_sort(access_log_path):
        response = entry.send()
        if end_time is not None:
            timedelta = entry.time_stamp - end_time
            time.sleep(timedelta.total_seconds())
        end_time = entry.time_stamp
        print(entry.path + "CODE: " + str(response))


def parse_and_sort(filepath):
    execution_array = []
    pattern = re.compile(magicRegex)
    # Context manager
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            path = pattern.search(line.strip())
            if path is not None:
                execution_array.append(LogEntry(path.group(1), path.group(2), path.group(3)))
            line = fp.readline()
    execution_array.sort(key=lambda x: x.time_stamp)
    return execution_array


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        [executor.submit(start_user_traffic, file) for file in glob.glob("accesslogs/*.log")]
