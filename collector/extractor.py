from config import *
from collections import defaultdict
import os
import re
import ast


class CommunitiesFilesExtractor:
    def __init__(self):
        # ASN, TYPE, COMMUNITY, INFO
        self.com_dic = self.import_dict()

        # COMMUNITY FORMAT (INT:INT)
        self.community = re.compile('\s\d+:\d+\s')

        # AS FORMAT
        self.asn = re.compile('as\d+', re.IGNORECASE)

        # LINE FORMAT
        self.remarks = re.compile('remarks:', re.IGNORECASE)

        # PREPEND FORMAT
        self.prepend = re.compile('prepend|prepending', re.IGNORECASE)

        #INFO PATTERN
        self.clean_info_pattern = re.compile('\sx\s',re.IGNORECASE)

        # CHARS TO BE REMOVED FROM TEXT
        self.remove_chars = ['"', "'", '\\', '|', '/', '(', ')', '[', ']', '{', '}', '-', '_', '<', '>', '+', '=', '*',
                             '!', '#', '$']

        # SYNONYMS
        self.synonyms = {'Prepend 1x': [' 1x', ' x1', ' 1 ', ' one ', ' once'],
                         'Prepend 2x': [' 2x', ' x2', ' 2 ', ' two ', ' twice'],
                         'Prepend 3x': [' 3x', ' x3', ' 3 ', ' three ', ' thrice'],
                         'Prepend 4x': [' 4x', ' x4', ' 4 ', ' four '],
                         'Prepend 5x': [' 5x', ' x5', ' 5 ', ' five '],
                         'Prepend 6x': [' 6x', ' x6', ' 6 ', ' six '],
                         'Prepend 7x': [' 7x', ' x7', ' 7 ', ' seven '],
                         'Prepend 8x': [' 8x', ' x8', ' 8 ', ' eight '],
                         'Prepend 9x': [' 9x', ' x9', ' 9 ', ' nine '],
                         'Prepend 10x': [' 10x', ' x10', ' 10 ', ' ten '],
                         'Prepend 11x': [' 11x', ' x11', ' 11 ', ' eleven ']}

    # Lembrete: ir removendo o que for encontrado, juntar e depois inserir no dict

    def extract(self):
        os.chdir(data_dir)
        for dirname, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                print(filename)
                file = os.path.join(dirname, filename)
                with open(file, encoding = "ISO-8859-1") as f:
                    name = str(filename).rstrip('.txt')
                    lines = f.read().splitlines()
                    for line in lines:
                        if not self.remarks.match(line): continue
                        prepend = self.find_prepend(line)
                        if prepend:
                            asn = name
                            line = self.clean_text(line)
                            community, _type, info = self.parse(asn, line)

                            if not community: continue
                            self.com_dic[asn][_type][community] = info

        with open(com_prepends, 'w') as prep:
            ast = 0
            comt = 0
            for i in self.com_dic:
                ast += 1
                prep.write('ASN: {}\n'.format(i))
                print(i)
                for j in self.com_dic[i]:
                    prep.write('TYPE: {}\n'.format(j))
                    print(j)
                    for c in self.com_dic[i][j]:
                        comt+=1
                        prep.write('{} - {}\n'.format(c, self.com_dic[i][j][c]))
                        print('{} - {}'.format(c, self.com_dic[i][j][c]))
        print('TOTAL AS:{}, TOTAL COMMUNITIES: {}'.format(ast, comt))
    def find_prepend(self, line):
        if self.prepend.search(line):
            return True
        return False

    def parse(self, asn, line):
        community, new_line = self.find_community(line)
        if not community: return None, None, None
        new_line = self.prepend.sub(' ', new_line)
        _type, new_line = self.prepending_type(asn, new_line)
        info = self.get_info(new_line)
        info = self.clean_info_pattern.sub('', info)
        info = info.replace('  ', ' ')
        return community.strip(' '), _type, info.strip(' ')

    def prepending_type(self, asn, line):
        for _type in self.synonyms:
            for syn in self.synonyms[_type]:
                syn_format = re.compile(syn, re.IGNORECASE)
                if syn_format.search(line):
                    new_line = syn_format.sub('', line)
                    return _type, new_line

        return self.count_asn_occurrences(asn, line)

    def count_asn_occurrences(self, asn, line):
        as_asn = asn +'|AS'+ asn
        asn_pattern = re.compile(as_asn, re.IGNORECASE)
        asn_list = asn_pattern.findall(line)
        prep_count = len(asn_list)
        if prep_count:
            new_line = asn_pattern.sub('',line)
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

    def clean_text(self, line):
        line = line.replace('remarks:', ' ')
        for char in self.remove_chars:
            if char in line:
                line = line.replace(char, ' ')
        line = line.replace('  ',' ')
        return line

    def get_info(self, line):
        pattern = re.compile('(\sto\s|towards)', re.IGNORECASE)

        if pattern.search(line):
            pattern.sub(' to ', line)
            dest = line[line.index(' to')+1:]
            as_list = self.asn.findall(dest)
            if len(as_list) == 1:
                return 'to ' + as_list[0]
            return dest if dest else 'to all'

        #########Deixar mais específico, analisar casos
        else:
            return line

        # get destination

    @staticmethod
    def import_dict():
        if os.path.isfile(com_dict):
            read = open(com_dict).read()
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

if __name__ == "__main__":
    CommunitiesFilesExtractor().extract()