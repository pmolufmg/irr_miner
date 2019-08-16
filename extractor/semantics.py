import os
import re
from config.config import *

class Semantics:
    def __init__(self):
        self.no_export_syn = ['no-export','no_export','noexport','not export']
        self.no_advertise_syn = ['no-advertise','no_advertise', 'noadvertise', 'not avertise']
        self.negative = re.compile('\sno\s|\snot\s|\Ano\s|\Anot\s|no-|no_', re.IGNORECASE)
        self.term = re.compile('(\ssend\s|'
                               'advertise\s|'
                               'advertise\Z|'
                               'export\s|'
                               'export\Z|'
                               'route\s|'
                               'route\Z|'
                               'announce\s|'
                               'announce\Z)', re.IGNORECASE)
        self.space = re.compile(' +')
        self.remarks = re.compile('remarks:', re.IGNORECASE)

    def search_occurrences(self):
        os.chdir(data_dir)
        with open('results.txt', 'w') as res:
            for dirname, dirnames, filenames in os.walk('.'):
                for filename in filenames:
                    if filename.endswith('.txt'):
                        print(filename)
                        file = os.path.join(dirname, filename)
                        with open(file, encoding="ISO-8859-1") as f:
                            asn = str(filename).rstrip('.txt')
                            lines = f.read().splitlines()
                            for line in lines:
                                if self.negative.search(line) and self.term.search(line):
                                    res.write('{}\n'.format(line))

if __name__ == '__main__':
    Semantics().search_occurrences()