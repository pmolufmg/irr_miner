import os
import subprocess


class Rir:
    def __init__(self, name, server):
        if isinstance(name, str) \
                and isinstance(server, str):
            self.name = name
            self.server = server
            # self.as_list = as_list
            self.last = ''
            self.counter = 0
            curr_dir = os.path.dirname(os.getcwd())
            os.makedirs(curr_dir + '/' + 'data' + '/' + name + '/', exist_ok=True)
            self.dir = curr_dir + '/data/' + name + '/'
            # self.run(as_list)
        else:
            print("Invalid parameters.")
            exit(1)

    def run(self, as_list):
        if len(as_list) > 0:
            for asn in as_list:
                text = self.collect(asn)
                if not self.control(text):
                    self.last = str(asn)
                    self.counter += 1
                    print('ASN: {} | Count: {}'.format(asn, self.counter))
                else:
                    return self.last, self.counter

    @staticmethod
    def control(text):
        lines = text.split('\n')
        aux = 0
        for line in lines:
            if line.startswith('%'):
                aux += 1
                if aux == 6:
                    if line.startswith('%ERROR:201:'):
                        return True
                    elif line.startswith('% Note:'):
                        return False
            elif line.startswith('as-block:'):
                return False
        return False

    def collect(self, asn):
        if isinstance(asn, int):
            try:
                irr_file = os.path.join(self.dir, str(asn) + '.txt')
                with open(irr_file, 'w') as irr:
                    as_n = 'as' + str(asn)
                    whois = subprocess.Popen(["whois", '-h', self.server, as_n],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT)
                    output = whois.communicate()[0]
                    output = output.decode('utf-8', 'ignore')

                    # self.last = asn
                    irr.write('{}\n'.format(output))
                    return output
            except IOError:
                return False
        else:
            return False


if __name__ == "__main__":
    lst = [asn for asn in range(1, 15375)]
    lst = sorted(lst, reverse=True)
    ripe = Rir('ripe', "whois.ripe.net")
    asn, count = ripe.run(lst)
    print("Ended. Last asn: {} | Collection num: {}".format(asn, count))
