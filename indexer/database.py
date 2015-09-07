CHARS = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMęĘóÓąĄśŚłŁżŻźŹćĆńŃ'


class Database(object):
    def __init__(self, chars=CHARS):
        self._files_metadata = {}
        self._indexed_files_data = {}
        self._id_generator = (i for i in range(10000000))
        self.word_chars = chars

    def search(self, word):
        result = []
        print(self._indexed_files_data[word].items())
        for file_id, positions in self._indexed_files_data[word].items():
            element = {'positions': positions}
            element.update(self._files_metadata[file_id])
            result.append(element)
        return result

    def get_files(self):
        return list(self._files_metadata.values())

    def add_file(self, filename, folder, file_data):
        file_id = self._generate_file_id()
        self._add_file_metadata(filename, folder, file_id)
        self._index_file_data(file_id, file_data)

    def _generate_file_id(self):
        return next(self._id_generator)

    def _add_file_metadata(self, filename, folder, file_id):
        self._files_metadata.update({file_id: {'filename': filename,
                                               'folder': folder, 'id': file_id}})

    def _index_file_data(self, file_id, file_data):
        for line_number, char_number, word in self._words(file_data):
            if word in self._indexed_files_data and \
                    file_id in self._indexed_files_data[word]:
                self._indexed_files_data[word][file_id].append({'pos': char_number,
                                                               'line': line_number})
                continue
            elif word in self._indexed_files_data and \
                    file_id not in self._indexed_files_data[word]:
                self._indexed_files_data[word][file_id] = [{'pos': char_number,
                                                            'line': line_number}]
                continue
            self._indexed_files_data[word] = {file_id: [{'pos': char_number,
                                                         'line': line_number}]} 

    """def _words(self, file_data):
        lines = file_data.split('\n')
        char_number = 0
        for line_number, line in enumerate(lines, start=1):
            words = line.split()
            for word in words:
                yield line_number, char_number, word
                char_number += len(word) + 1"""

    def _words(self, file_data):
        char_number = 1
        line_number = 1
        reading_word = False
        word = ''
        for char in file_data: 
            if char in self.word_chars and not reading_word: #wchodzimy do slowa
                reading_word = True
                word += char
                char_number += 1
                continue
            elif char not in self.word_chars and reading_word: #wychodzimy ze slowa
                reading_word = False
                char_number += 1
                if char == '\n':
                    line_number += 1
                word_copy = word[:]
                word = ''
                yield line_number, char_number, word_copy
                continue
            elif char in self.word_chars and reading_word: #jestesmy w slowie
                char_number += 1 
                word += char
            else: #jestesmy po za slowem
                char_number += 1 
                if char == '\n':
                    line_number += 1
