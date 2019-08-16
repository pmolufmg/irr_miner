import os
import ast


class FileManager:
    def __init__(self):
        self.file_list = set()

    @staticmethod
    def read_file(filepath):
        if os.path.isfile(filepath):
            try:
                file = open(filepath)
                content = file.read()
                file.close()
            except IOError:
                print('Could not read {}'.format(filepath))
                return None

            return content
        else:
            print('Not found: {}'.format(filepath))
            return None

    def splitted_file_content(self, filepath, char):
        content = self.read_file(filepath)
        return content.split(char)

    @staticmethod
    def eval_file(filepath):
        if os.path.isfile(filepath):
            try:
                file = open(filepath)
                file_eval = ast.literal_eval(file.read())
                file.close()
            except ValueError:
                print('Could not eval content of {}'.format(filepath))
                return None

            return file_eval
        else:
            print('Not found: {}'.format(filepath))
            return None

    def write_file(self, filepath):
        try:
            file = open(filepath, 'w')
            self.file_list.add(file)
        except IOError:
            print('Unable to write in file {}'.format(filepath))
            return None

        return file

    def append_to_file(self, filepath):
        try:
            file = open(filepath, 'a')
            self.file_list.add(file)
        except IOError:
            print('Unable to append in file {}'.format(filepath))
            return None

        return file

    @staticmethod
    def read_lines(filepath, num_of_lines):
        if os.path.isfile(filepath):
            try:
                file = open(filepath)
                text = ''
                for line in range(0, num_of_lines):
                    line = file.readline()
                    text += line
                file.close()
            except IOError:
                return None

            return text

    def close_files(self):
        if len(self.file_list) > 0:
            for file in self.file_list:
                name = str(file).split()[1].lstrip('name=').strip("'")
                try:
                    file.close()
                    print('{} closed'.format(name))
                except IOError:
                    print('Could not close {}'.format(name))
                    continue
