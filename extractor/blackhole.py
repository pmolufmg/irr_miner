from config.config import *
import re


class Blackhole:
    def __init__(self, as_patt, comm_patt, clean_patt, info_patt, c_type):

        # COMMUNITY FORMAT (INT:INT)
        self.community = comm_patt

        # COMMUNITY TYPE
        self.c_type = c_type

        # AS FORMAT
        self.asn = as_patt

        # INFO PATTERN
        self.clean_info_pattern = clean_patt
        self.destination = info_patt

    def parse(self, asn, line):
        community, new_line = self.find_community(line)
        if not community: return None, None, None
        new_line = self.format_line(asn, new_line)
        info = self.get_info(asn, new_line)
        info = self.clean_info_pattern.sub('', info)
        info = info.replace('  ', ' ')
        if len(info.replace('-', '').replace(' ', '')) < 3:
            info = 'to all'
        return community.strip(' '), self.c_type, info.strip(' ')

    def find_community(self, line):
        try:
            community = self.community.search(line).group()
            new_line = self.community.sub('', line)
            new_line = new_line.replace(':', '')
            return community, new_line
        except (ValueError, AttributeError):
            return None, line

    @staticmethod
    def format_line(asn, line):
        try:
            asn_form = '\w+' + asn + '\s|\w+' + asn + '\Z|\D' + asn + '\D|\A' + asn + '\D|\D' + asn + '\Z'
            asn_form = re.compile(asn_form, re.IGNORECASE)
            new_line = asn_form.sub(' ', line)
            new_line = new_line.replace('  ', ' ')
            new_line = new_line.strip(' ')
            return new_line
        except (ValueError, AttributeError):
            return line

    def get_info(self, asn, line):
        line = line.replace(asn, ' ')
        if self.destination.search(line):
            line = self.destination.sub(' to ', line)
            dest = line[line.index(' to') + 1:]
            dest = dest.replace('  ', ' ')
            dest = dest.strip(' ')
            as_list = self.asn.findall(dest)
            if len(as_list) == 1:
                return 'to ' + as_list[0]
            return dest if dest else 'to all'

        else:
            return line

    @staticmethod
    def save_file(com_dic):
        with open(com_blackhole, 'w') as n_bh:
            ast = 0
            comt = 0
            text = ''
            as_set = set()
            for asn in com_dic:
                for _type in com_dic[asn]:
                    if not _type.startswith('BLACKHOLE'): continue
                    if asn not in as_set:
                        as_set.add(asn)
                        text += 'ASN: {}\n'.format(asn)
                        ast += 1
                    for community in com_dic[asn][_type]:
                        info = com_dic[asn][_type][community]
                        comt += 1
                        text += '{}: {} - {}\n'.format(_type, community, info)
                        # print('{} - {}'.format(community, info))
            if text:
                n_bh.write(text)
        print('BLACKHOLE: TOTAL AS:{}, TOTAL COMMUNITIES: {}'.format(ast, comt))
