from argparse import Namespace

from TIGr import AbstractSourceReader
from TurtleDrawer import TurtleDrawer
from TigrParser import TigrParser
import sys
from TigrExcptionHandler import ExceptionHandler


class TigerReaderOne(AbstractSourceReader):
    def go(self):
        try:
            if not self.reader.source:     # check source is available
                if not self.reader.file_name:
                    self.reader.file_name = input('Please enter a file name: ')
                try:
                    self.reader.source = open(self.reader.file_name).readlines()
                except (IOError, FileNotFoundError) as e:
                    print('NO file Found or IO error', e)
            self.reader.parser.parse(self.reader.source)
        except Exception as e:  # nice error display to user
            print('Error', e)


def arg_parser():
    import argparse
    '''
    example usage within a terminal:
    > python TigrReader.py -f commands.txt

    > type commands.txt | python TigrReader.py

    > python TigrReader.py
    > Enter your commands. Ctrl + Z to exit
    > If no commands are entered, you will be prompted for a file name.

    '''
    args_parser = argparse.ArgumentParser(description="Tigr Assignment")
    args_parser.add_argument("-f", "--file", help="Enter name of the file", default=None)
    stored_args = args_parser.parse_args()
    return stored_args


class ReaderConstructor(object):
    def __init__(self, reader_builder):
        self.r = reader_builder

    def set_reader(self, new_reader):
        self.r = new_reader

    def action(self):
        new_exception_handling = ExceptionHandler("TIGr went wrong and stopped")
        argument = arg_parser()
        if argument.file:
            self.r.reader.set_file(argument.file)
            self.r.reader.set_parser(TigrParser(TurtleDrawer(), new_exception_handling))
        else:
            # read from input at prompt
            print("Enter your commands. Ctrl + Z to exit or finish.")
            # only on windows, if this was portable we should add the linux interrupt command x3
            print("If no commands are entered, you will be prompted for a file name.")
            source = sys.stdin.readlines()
            self.r.reader.set_parser(TigrParser(TurtleDrawer(), new_exception_handling))
            self.r.reader.set_source(source)
        self.r.go()
        time.sleep(10)


if __name__ == "__main__":
    # check for file name arguments
    import time
    reader_one = TigerReaderOne()
    con = ReaderConstructor(reader_one)
    con.action()
