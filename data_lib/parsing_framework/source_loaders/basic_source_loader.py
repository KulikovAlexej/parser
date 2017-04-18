
class BasicSourceLoader:
    def __init__(self):
        pass

    def get_as_text(self, url):
        raise Exception('Method should be override')

    def save_to_file(self, url, filename):
        text = self.get_as_text(url)
        output_file = open(filename, 'w', encoding='utf8')
        output_file.write(text)
        output_file.close()
