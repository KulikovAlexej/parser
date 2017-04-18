
import os.path


class BasicSourceStorage:
    @staticmethod
    def is_file_exists(filename):
        return os.path.isfile(filename)

    @staticmethod
    def read_file(filename):
        output_file = open(filename, 'r', encoding='utf8')
        text = output_file.read()
        output_file.close()
        return text

    @staticmethod
    def write_file(filename, text):
        output_file = open(filename, 'w', encoding='utf8')
        output_file.write(text)
        output_file.close()
