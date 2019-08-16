from rir.afrinic import *
from rir.apnic import *
from rir.arin import *
from rir.lacnic import *
from rir.ripe import *
from collections import defaultdict
from datetime import *
import time
import threading


class Main:
    def __init__(self):
        self.collected_files = defaultdict(list)
        self.afrinic = Afrinic()
        self.apnic = Apnic()
        self.arin = Arin()
        self.lacnic = Lacnic()
        self.ripe = Ripe()
        self.sleep_time = 86400

    def afrinic_collector(self):
        while True:
            print('Afrinic collector started: {}'
                  .format(datetime.now()))
            name, collected = self.afrinic.run()
            self.collected_files[name] += collected
            # Analysis + remove files from dict
            print('Afrinic collector sleeping: {}'
                  .format(datetime.now()))
            time.sleep(self.sleep_time)

    def apnic_collector(self):
        while True:
            print('Apnic collector started: {}'
                  .format(datetime.now()))
            name, collected = self.apnic.run()
            self.collected_files[name] += collected
            # Analysis + remove files from dict
            print('Apnic collector sleeping: {}'
                  .format(datetime.now()))
            time.sleep(self.sleep_time)

    def arin_collector(self):
        while True:
            print('Arin collector started: {}'
                  .format(datetime.now()))
            name, collected = self.arin.run()
            self.collected_files[name] += collected
            # Analysis + remove files from dict
            print('Arin collector sleeping: {}'
                  .format(datetime.now()))
            time.sleep(self.sleep_time)

    def lacnic_collector(self):
        while True:
            print('Lacnic collector started: {}'
                  .format(datetime.now()))
            name, collected = self.lacnic.run()
            self.collected_files[name] += collected
            # Analysis + remove files from dict
            print('Lacnic collector started: {}'
                  .format(datetime.now()))
            time.sleep(self.sleep_time)

    def ripe_collector(self):
        while True:
            print('Ripe collector started: {}'
                  .format(datetime.now()))
            name, collected = self.ripe.run()
            self.collected_files[name] += collected
            # Analysis + remove files from dict
            print('Ripe collector sleeping: {}'
                  .format(datetime.now()))
            time.sleep(self.sleep_time)

    def run_threads(self):
        try:
            threading.Thread(target=self.afrinic_collector).start()
            threading.Thread(target=self.apnic_collector).start()
            threading.Thread(target=self.arin_collector).start()
            threading.Thread(target=self.lacnic_collector).start()
            threading.Thread(target=self.ripe_collector).start()
        except KeyboardInterrupt:
            print('Interrupted.')
            exit(0)


if __name__ == "__main__":
    Main().run_threads()
