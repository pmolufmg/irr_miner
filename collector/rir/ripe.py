from config import *
import subprocess
import time
import ast
import os
import re


class Ripe:
    def __init__(self):
        self.name = 'ripe'
        self.server = 'whois.ripe.net'
        self.collected_files = []
        self.has_specific_list = False
        self.as_list = self.convert_list_types([i for i in range(1, 64496)], str)
        self.num_of_queries = len(self.as_list) - 1
        self.total_queries = 0
        self.valid_queries = 0

        self.last = self.get_last()
        self.first = self.last
        self.set_list()

        self.error_type = 0
        self.error_str = ''

        self.start_time = float()

    def run(self):
        try:
            if len(self.as_list) > 0:
                self.start_time = time.time()
                for asn in self.as_list[:self.num_of_queries]:
                    text, file = self.collect(asn)
                    self.total_queries += 1
                    if text and not self.denied(text, asn):
                        self.last = str(asn)
                        self.valid_queries += 1
                        self.collected_files.append(file)
                        print('ASN: {} | Count total: {}| Count valid: {}'
                              .format(asn, self.total_queries, self.valid_queries))
                    else:
                        self.reset()
                        return self.name, self.collected_files
                self.reset()
                return self.name, self.collected_files
        except KeyboardInterrupt:
            self.reset()
            return self.name, self.collected_files

    def denied(self, text, asn):
        lines = text.split('\n')
        if len(lines) > 9:
            if re.search('error', lines[0] + lines[-7], re.IGNORECASE) \
                    or re.search('daily limit', lines[-9], re.IGNORECASE):
                return self.set_error_type(asn, lines[0], lines[-7])
            else:
                return False
        elif len(lines) > 7:

            if re.search('error', lines[0] + lines[-7], re.IGNORECASE):
                return self.set_error_type(asn, lines[0], lines[-7])
            else:
                return False
        else:
            if re.search('error', lines[0], re.IGNORECASE):
                return self.set_error_type(asn, lines[0])
            else:
                return False

    def collect(self, asn):
        if asn.isnumeric():
            try:
                irr_file = os.path.join(ripe_dir, asn + '.txt')
                with open(irr_file, 'w') as irr:
                    as_n = 'as' + asn
                    whois = subprocess.Popen(["whois", '-h', self.server, as_n],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT)
                    output = whois.communicate()[0]
                    output = output.decode('utf-8', 'ignore')
                    # output = output.strip(' ')
                    irr.write('{}'.format(output))
                    return output, irr_file
            except IOError:
                return False
        else:
            return False

    def set_list(self):
        if not os.path.isfile(ripe_list):
            self.set_new_list()
            new = open(ripe_list, 'w')
            new.write(str(self.as_list))
            new.close()
        else:
            try:
                specific_list = ast.literal_eval(open(ripe_list).read())
                specific_list = sorted(self.convert_list_types(specific_list, int))
                specific_list = self.convert_list_types(specific_list, str)
                self.as_list = specific_list
                self.has_specific_list = True
                self.set_new_list()
            except ValueError:
                print('Invalid list Format')

    def get_last(self):
        if not os.path.isfile(ripe_log):
            open(ripe_log, 'a').close()
            return self.as_list[0]
        else:
            with open(ripe_log) as last_file:
                last = last_file.read().strip(' ').strip('\n').splitlines()
                data = self.get_last_record(last)

                if isinstance(data, str):
                    return data

                last_as = data[1]
                queries = data[6]
                try:
                    test = 0 < int(last_as) < 64496
                    queries = int(queries)
                    self.num_of_queries = queries if queries > 6000 else 15000
                    return last_as if test \
                        else self.as_list[0]
                except ValueError:
                    return self.as_list[0]

    def get_last_record(self, file):
        line = -1
        try:
            while len(file[line]) < 5:
                line -= 1
            data = file[line].split(',')
            if len(data) == 9:
                return data
            else:
                return self.as_list[0]
        except ValueError:
            return self.as_list[0]

    def set_new_list(self):
        if self.last:
            if not self.has_specific_list:
                try:
                    ini = int(self.last)
                    end = 64495 + ini
                    full_list = [(i % 64495) + 1 for i in range(ini, end)]
                    self.as_list = self.convert_list_types(full_list, str)
                except ValueError:
                    print('Unable to generate AS-list.')
                    exit(1)

            elif self.last in self.as_list:
                start = self.as_list.index(self.last)
                new_list = [i for i in self.as_list[start:]]
                new_list += [i for i in self.as_list[:start]]
                self.as_list = self.convert_list_types(new_list, str)

            else:
                last = int(self.last)
                while str(last) not in self.as_list:
                    if last < 64496:
                        last += 1
                    else:
                        last = 1
                last = str(last)
                start = self.as_list.index(last)
                new_list = [i for i in self.as_list[start:]]
                new_list += [i for i in self.as_list[:start]]
                self.as_list = self.convert_list_types(new_list, str)
        else:
            return

    def set_error_type(self, asn, case1='None', case2='None', case3=None):
        if re.search('error', case1, re.IGNORECASE):
            self.error_type = 1
            self.error_str = case1.replace(',', '')
            time.sleep(10)
            text, file = self.collect(asn)
            first_line = text.split('\n')[0]
            if re.search('error', first_line, re.IGNORECASE):
                return True
            else:
                self.last = str(asn)
                self.valid_queries += 1
                self.collected_files.append(file)
                return False

        elif re.search('error', case2, re.IGNORECASE):
            self.error_type = 2
            self.error_str = case2.replace(',', '')
            return True
        elif case3:
            self.error_type = 3
            self.error_str = case3.replace(',', '')
            return True
        else:
            return False

    def get_start_index(self):
        return self.as_list.index(self.last)

    def save_data(self):
        text = self.set_data_text()
        file = open(ripe_log, 'a')
        file.write(text)
        file.close()

    def save_as_list(self):
        file = open(ripe_list, 'w')
        file.write(str(self.as_list))
        file.close()

    def reset(self):
        self.save_data()
        self.set_list()
        self.save_as_list()
        self.total_queries = 0
        self.valid_queries = 0
        self.error_type = 0
        self.error_str = ''

    def set_data_text(self):
        now = time.time()
        elapsed = now - self.start_time
        st_time = self.from_timestamp(self.start_time)
        end_time = self.from_timestamp(now)
        elapsed_time = self.from_timestamp(elapsed)
        if not self.error_str:
            self.error_str = None
            self.error_type = 0
        return '{},{},{},{},{},{},{},{},{}\n' \
            .format(self.first,
                    self.last,
                    st_time,
                    end_time,
                    elapsed_time,
                    self.total_queries,
                    self.valid_queries,
                    self.error_type,
                    self.error_str)

    def get_elapsed_time(self):
        return time.strftime("%H:%M:%S", time.gmtime(self.start_time - time.time()))

    @staticmethod
    def from_timestamp(timestamp):
        return time.strftime("%H:%M:%S", time.gmtime(timestamp))

    @staticmethod
    def convert_list_types(l, dtype):
        return list(map(dtype, l))


if __name__ == "__main__":
    ripe = Ripe()
    lst = ripe.run()
    print(lst)
