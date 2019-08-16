import re
from collections import OrderedDict
from config.config import *


class PathPrepending:
    def __init__(self, as_patt, comm_patt, prep_patt, clean_patt, info_patt):

        # SYNONYMS
        self.synonyms = OrderedDict([('Prepend 1x', '\s1x|\A1x|1x\Z|\Ax1|\sx1|x1\Z|\s1\s|\A1\s|\s1\Z|\A1\Z|'
                                                    '\sone\s|\Aone\s|\sone\Z|\Aone\Z|once'),
                                     ('Prepend 2x', '\s2x|\A2x|2x\Z|\Ax2|\sx2|x2\Z|\s2\s|\A2\s|\s2\Z|\A2\Z|'
                                                    '\stwo\s|\Atwo\s|\stwo\Z|\Atwo\Z|twice'),
                                     ('Prepend 3x', '\s3x|\A3x|3x\Z|\Ax3|\sx3|x3\Z|\s3\s|\A3\s|\s3\Z|\A3\Z|'
                                                    '\sthree\s|\Athree\s|\sthree\Z|\Athree\Z|thrice'),
                                     ('Prepend 4x', '\s4x|\A4x|4x\Z|\Ax4|\sx4|x4\Z|\s4\s|\A4\s|\s4\Z|\A4\Z|'
                                                    '\sfour\Z|\Afour\s|\sfour\s|\Afour\Z'),
                                     ('Prepend 5x', '\s5x|\A5x|5x\Z|\Ax5|\sx5|x5\Z|\s5\s|\A5\s|\s5\Z|\A5\Z|'
                                                    '\sfive\Z|\Afive\s|\sfive\s|\Afive\Z'),
                                     ('Prepend 6x', '\s6x|\A6x|6x\Z|\Ax6|\sx6|x6\Z|\s6\s|\A6\s|\s6\Z|\A6\Z|'
                                                    '\ssix\Z|\Asix\s|\ssix\s|\Asix\Z'),
                                     ('Prepend 7x', '\s7x|\A7x|7x\Z|\Ax7|\sx7|x7\Z|\s7\s|\A7\s|\s7\Z|\A7\Z|'
                                                    '\sseven\Z|\Aseven\s|\sseven\s|\Aseven\Z'),
                                     ('Prepend 8x', '\s8x|\A8x|8x\Z|\Ax8|\sx8|x8\Z|\s8\s|\A8\s|\s8\Z|\A8\Z|'
                                                    '\seight\Z|\Aeight\s|\seight\s|\Aeight\Z'),
                                     ('Prepend 9x', '\s9x|\A9x|9x\Z|\Ax9|\sx9|x9\Z|\s9\s|\A9\s|\s9\Z|\A9\Z|'
                                                    '\snine\Z|\Anine\s|\snine\s|\Anine\Z'),
                                     ('Prepend 10x', '\s10x|\A10x|10x\Z|\Ax10|\sx10|x10\Z|\s10\s|\A10\s|\s10\Z|\A10\Z|'
                                                     '\sten\Z|\Aten\s|\sten\s|\Aten\Z'),
                                     ('Prepend 11x', '\s11x|\A11x|11x\Z|\Ax11|\sx11|x11\Z|\s11\s|\A11\s|\s11\Z|\A11 \Z|'
                                                     '\seleven\Z|\Aeleven\s|\seleven\s|\Aeleven\Z')])

        # COMMUNITY FORMAT (INT:INT)
        self.community = comm_patt

        # AS FORMAT
        self.asn = as_patt

        # PREPEND FORMAT
        self.prepend = prep_patt

        # INFO PATTERN
        self.clean_info_pattern = clean_patt
        self.destination = info_patt

    def parse(self, asn, line):
        community, new_line = self.find_community(line)
        if not community: return None, None, None
        new_line = self.prepend.sub(' ', new_line)
        _type, new_line = self.prepending_type(asn, new_line)
        info = self.get_info(asn, new_line)
        info = self.clean_info_pattern.sub('', info)
        info = info.replace('  ', ' ')
        if len(info.replace('-', '').replace(' ', '')) < 5:
            info = 'to all'
        return community.strip(' '), _type, info.strip(' ')

    def prepending_type(self, asn, line):
        for _type in self.synonyms:
            patt = self.synonyms[_type]
            syn_format = re.compile(patt, re.IGNORECASE)
            if syn_format.search(line):
                new_line = syn_format.sub('', line)
                return _type, new_line

        return self.count_asn_occurrences(asn, line)

    def count_asn_occurrences(self, asn, line):
        as_asn = asn + '|AS' + asn
        asn_pattern = re.compile(as_asn, re.IGNORECASE)
        asn_list = asn_pattern.findall(line)
        prep_count = len(asn_list)
        if prep_count:
            new_line = asn_pattern.sub('', line)
            return self.prepend_key_index(prep_count), new_line.strip(' ')

        else:
            return 'Prepend 1x', line

    @staticmethod
    def prepend_key_index(num):
        if 1 <= num <= 11:
            prep_list = ['Prepend 1x',
                         'Prepend 2x',
                         'Prepend 3x',
                         'Prepend 4x',
                         'Prepend 5x',
                         'Prepend 6x',
                         'Prepend 7x',
                         'Prepend 8x',
                         'Prepend 9x',
                         'Prepend 10x',
                         'Prepend 11x']

            return prep_list[num - 1]

        else:
            return 'Prepend 1x'

    def find_community(self, line):
        try:
            community = self.community.search(line).group()
            new_line = self.community.sub('', line)
            new_line = new_line.replace(':', '')
            return community, new_line
        except (ValueError, AttributeError):
            return None, line

    def get_info(self, asn, line):
        noise = 'AS' + asn + '\D|' \
                             'AS' + asn + '\Z|' \
                                          '\D' + asn + '\D|' \
                                                       '\D' + asn + '\Z|' \
                                                                    '\A' + asn + '\D'
        noise = re.compile(noise, re.IGNORECASE)
        time = re.compile(r'times|time', re.IGNORECASE)
        line = noise.sub('', line)
        line = time.sub('', line)
        if self.destination.search(line):
            line = self.destination.sub(' to ', line)
            dest = line[line.index(' to') + 1:]
            as_list = self.asn.findall(dest)
            if len(as_list) == 1:
                return 'to ' + as_list[0]
            return dest if dest else 'to all'

        else:
            return line

    @staticmethod
    def save_file(com_dic):
        with open(com_prepends, 'w') as prep:
            ast = 0
            comt = 0
            text = ''
            as_set = set()
            for asn in com_dic:
                for _type in com_dic[asn]:
                    if not _type.startswith('Prepend'): continue
                    if asn not in as_set:
                        as_set.add(asn)
                        text += 'ASN: {}\n'.format(asn)
                        ast += 1
                    for community in com_dic[asn][_type]:
                        info = com_dic[asn][_type][community]
                        comt += 1
                        text += '{}: {} - {}\n'.format(_type, community, info)
            if text:
                prep.write(text)

        print('PREP: TOTAL AS:{}, TOTAL COMMUNITIES: {}'.format(ast, comt))
