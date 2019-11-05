from argparse import Namespace
from abc import ABCMeta, abstractmethod
from TIGr import AbstractSourceReaderBuilder
from TurtleDrawer import TurtleDrawer
from TigrDrawerTwo import TkinterDrawer
from TigrParser import TigrParser
import sys
from TigrExcptionHandler import ExceptionHandler


class ReaderConcreteBuilder1(AbstractSourceReaderBuilder):  # ConcreteBuilder1 -- Builder Pattern
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


class ReaderConcreteBuilder2(AbstractSourceReaderBuilder):  # ConcreteBuilder2 -- Builder Pattern
    # A prompt source reader can be added in this class -- Builder Pattern
    # This will allow the program to use different readers, making it flexible -- Builder Pattern
    def go(self):
        pass


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


class ReaderDirector(object):   # Director -- Builder Pattern
    def __init__(self, reader_builder):
        self.r = reader_builder

    def set_reader(self, new_reader):
        self.r = new_reader

    def construct(self):
        new_exception_handling = ExceptionHandler("TIGr went wrong and stopped")
        argument = arg_parser()
        if argument.file:
            has_file = Filler(HasFile(self.r, argument.file, new_exception_handling))
            has_file.file()
        else:
            no_file = Filler(NoFile(self.r, file_name=None, exception=new_exception_handling))
            no_file.no_file()
        self.r.go()
        time.sleep(10)


class AbstractCommandFile(metaclass=ABCMeta):  # Compositor -- Strategy Pattern
    def __init__(self, reader_behaviour, file_name=None, exception=None):
        self.the_reader = reader_behaviour
        self.file = file_name
        self.exception = exception

    @abstractmethod
    def set_source(self):
        pass

    @abstractmethod
    def set_parser(self):
        pass


class Filler(object):  # Composition    -- Strategy Pattern
    # The composition in this pattern can be used for different
    # scenario for example This class handle two situations if the file is present or not.
    # Based on this reader object passed to this class as perform
    # methods according to the file status.     -- Strategy Pattern
    def __init__(self, file_class):
        self.status = file_class

    def file(self):
        self.status.set_parser()
        self.status.set_source()

    def no_file(self):
        self.status.instructions()
        self.status.set_source()
        self.status.set_parser()


class HasFile(AbstractCommandFile):  # HasFile_Compositor -- Strategy Pattern
    # if the file is present, making sure that it take source from the file. -- Strategy Pattern
    def set_source(self):
        self.the_reader.reader.set_file(self.file)

    def set_parser(self):
        self.the_reader.reader.set_parser(TigrParser(TurtleDrawer(), self.exception))


class NoFile(AbstractCommandFile):  # NoFile_Compositor -- Strategy Pattern
    # It reads lines entered in the CMD
    # if the file is not present, making sure that the commands provided in cmd are taken as a source
    # and further executed. -- Strategy Pattern
    def set_source(self):
        source = sys.stdin.readlines()
        self.the_reader.reader.set_source(source)

    def set_parser(self):
        self.the_reader.reader.set_parser(TigrParser(TurtleDrawer(), self.exception))

    @staticmethod
    def instructions():
        print("Enter your commands. Ctrl + Z to exit or finish.")
        # only on windows, if this was portable we should add the linux interrupt command x3
        print("If no commands are entered, you will be prompted for a file name.")


if __name__ == "__main__":
    # check for file name arguments
    import time
    reader_one = ReaderConcreteBuilder1()
    con = ReaderDirector(reader_one)
    con.construct()
