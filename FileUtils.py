#encoding=utf-8
import os
import codecs
import jsonpickle as json

class FileUtils:

    @staticmethod
    def write_to_file(file_name, text):
        final_file_name = os.getcwd()  + '/' + file_name
        update_file = codecs.open(final_file_name, 'w', 'utf-8')
        update_file.write(text)
        update_file.close()

