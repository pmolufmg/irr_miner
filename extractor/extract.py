from extractor.prepend import *
from extractor.no_export import *
from extractor.no_advertise import *
from extractor.blackhole import *
from extractor.not_send import *
from collections import defaultdict
import os
import re
import ast
import json


class CommunitiesFilesExtractor:
    def __init__(self):
        # ASN, TYPE, COMMUNITY, INFO
        self.com_dic = self.import_dict()

        # COMMUNITY FORMAT (INT:INT)
        self.community = re.compile('\s+\d+:\d+\s|\A\d+:\d+\s|\s\d+:\d+\Z')

        #INVALID COMMUNITY FORMAT
        self.invalid = re.compile('\d+:\d+\[\w|\d+:\d+\(\w|\d+:\d+{\w|\d+:\d+[a-zA-Z]')

        # AS FORMAT
        self.asn = re.compile('as\d+', re.IGNORECASE)

        # LINE FORMAT
        self.remarks = re.compile('remarks:', re.IGNORECASE)

        # PREPEND FORMAT
        self.prepend = re.compile('prepend|prepending|pre-pend', re.IGNORECASE)

        # INFO PATTERN
        self.clean_info_pattern = re.compile('\sx\s', re.IGNORECASE)
        self.destination = re.compile('(\sto\s|\Ato\s|toward.)', re.IGNORECASE)

        # CHARS TO BE REMOVED FROM TEXT
        self.remove_chars = ['"', "'", '\\', '|', '/', '(', ')', '[', ']', '{', '}', '<', '>', '+', '=', '*',
                             '!', '#', '$', '-', '_']

        # AUXILIARY PATTERN
        self.negation = re.compile('\sno\s|'
                                   '\snot\s|'
                                   '\Ano\s|'
                                   '\Anot\s|'
                                   '\snone\s|'
                                   '\snone\Z|'
                                   'noone|'
                                   'nobody|'
                                   'no-|'
                                   'no_', re.IGNORECASE)

        # NO-EXPORT FORMAT
        self.export = re.compile('(export\s|'
                                 'export\Z|'
                                 '\Aexport)', re.IGNORECASE)

        # UNDEFINED NO-EXPORT OR NO-ADNVERTISE
        self.send = re.compile('(\ssend\s|'
                                 '\Asend|'
                                 '\ssend\Z|'
                                 'route\s|'
                                 'route\Z|'
                                 '\Aroute\s|'
                                 'announce\s|'
                                 'announce\Z|'
                                 '\Aannounce)', re.IGNORECASE)

        # NO-ADVERTISE FORMAT
        self.advertise = re.compile('(advertise\s|'
                                    'advertise\Z)', re.IGNORECASE)

        # BLACKHOLE FORMAT
        self.blackhole_patt = re.compile('blackhole|blackholing|black-hole|black-holing', re.IGNORECASE)

        self.path_prepending = PathPrepending(self.asn,
                                              self.community,
                                              self.prepend,
                                              self.clean_info_pattern,
                                              self.destination)
        self.no_export = NoExport(self.asn,
                                  self.community,
                                  self.negation,
                                  self.export,
                                  self.clean_info_pattern,
                                  self.destination,
                                  'NO-EXPORT')

        self.not_send = NotSend(self.asn,
                                  self.community,
                                  self.negation,
                                  self.send,
                                  self.clean_info_pattern,
                                  self.destination,
                                  'NOT-SEND')

        self.no_advertise = NoAdvertise(self.asn,
                                        self.community,
                                        self.negation,
                                        self.advertise,
                                        self.clean_info_pattern,
                                        self.destination,
                                        'NO-ADVERTISE')

        self.blackhole = Blackhole(self.asn,
                                   self.community,
                                   self.clean_info_pattern,
                                   self.destination,
                                   'BLACKHOLE')

    def extract(self):
        os.chdir(data_dir)
        for dirname, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if filename.endswith('.txt'):
                    print(filename)
                    file = os.path.join(dirname, filename)
                    with open(file, encoding="ISO-8859-1") as f:
                        asn = str(filename).rstrip('.txt')
                        lines = f.read().splitlines()
                        for line in lines:
                            if not self.remarks.match(line) \
                                    and not self.community.match(line): continue
                            if self.invalid.search(line): continue

                            prepend = self.find_prepend(asn, line)
                            if prepend: continue

                            no_export = self.find_no_export(asn, line)
                            if no_export: continue

                            not_snd = self.find_not_send(asn, line)
                            if not_snd: continue

                            no_advertise = self.find_no_advertise(asn, line)
                            if no_advertise: continue

                            self.find_blackhole(asn, line)


        self.save_dict_file()
        self.save_files()

    def find_prepend(self, asn, line):
        if self.prepend.search(line):
            line = self.clean_text(line)
            community, _type, info = self.path_prepending.parse(asn, line)
            if community:
                self.com_dic[asn][_type][community] = info
            return True
        return False

    def find_no_export(self, asn, line):
        if self.negation.search(line) \
                and self.export.search(line):
            line = self.clean_text(line)
            community, _type, info = self.no_export.parse(asn, line)
            if community:
                self.com_dic[asn][_type][community] = info
            return True
        return False

    def find_not_send(self, asn, line):
        if self.negation.search(line) \
                and self.send.search(line):
            line = self.clean_text(line)
            community, _type, info = self.not_send.parse(asn, line)
            if community:
                self.com_dic[asn][_type][community] = info
            return True
        return False

    def find_no_advertise(self, asn, line):
        if self.negation.search(line) \
                and self.advertise.search(line):
            line = self.clean_text(line)
            community, _type, info = self.no_advertise.parse(asn, line)
            if community:
                self.com_dic[asn][_type][community] = info
            return True
        return False

    def find_blackhole(self, asn, line):
        if self.blackhole_patt.search(line):
            # if self.community.search(line):
            line = self.clean_text(line)
            community, _type, info = self.blackhole.parse(asn, line)
            if community:
                self.com_dic[asn][_type][community] = info
            return True
        return False

    def clean_text(self, line):
        line = line.replace('remarks:', ' ')
        for char in self.remove_chars:
            if char in line:
                line = line.replace(char, ' ')
        line = line.replace('  ', ' ')
        return line

    @staticmethod
    def import_dict():
        if os.path.isfile(com_dict):
            read = open(com_dict).read()
            read = json.loads(read)
            com_dic = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
            try:
                com_dic = ast.literal_eval(read)
                com_dic = defaultdict(str, com_dic)
            except (ValueError, SyntaxError):
                pass
            finally:
                return com_dic
        else:
            open(com_dict, 'w').close()
            return defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

    def check_ases(self):
        with open(com_ases) as ases, open(collected, 'w') as col:
            text = []
            asns = 0
            cms = 0
            as_list = []
            lines = ases.read().splitlines()
            for line in lines:
                line = line.strip(' ')
                if line in self.com_dic:
                    # col.write('AS: {}\n'.format(line))
                    asns += 1
                    for _type in self.com_dic[line]:
                        for comm in self.com_dic[line][_type]:
                            cms += 1
                            info = self.com_dic[line][_type][comm]
                            text.append('{}|{}|{}|{}\n'.format(line, _type, comm, info))
                            # col.write('{}: {} - {}\n'.format(_type, comm, info ))
                            # print('{} - {}'.format(comm, self.com_dic[line][_type][comm]))

            header = '#TOTAL: {} ASES, {} COMMUNITIES\n'.format(asns, cms)
            header += '#ASN|COMMUNITY TYPE|COMMUNITY|INFORMATION\n'
            header += ''.join(text)
            col.write(header)
        print('FOUND {} SPECIFIC ASes and {} COMMUNITIES'.format(asns, cms))

    def save_dict_file(self):
        with open(com_dict, 'w') as cd:
            cd.write(json.dumps(self.com_dic))

    def save_files(self):
        self.path_prepending.save_file(self.com_dic)
        self.no_export.save_file(self.com_dic)
        self.no_advertise.save_file(self.com_dic)
        self.blackhole.save_file(self.com_dic)
        self.not_send.save_file(self.com_dic)


if __name__ == "__main__":
    c = CommunitiesFilesExtractor()
    c.extract()
    c.check_ases()
