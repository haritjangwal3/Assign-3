from abc import ABC, abstractmethod, ABCMeta
import json

""" Tiny Interpreted GRaphic = TIGR
Keep the interfaces defined below in your work.
 """


class AbstractDrawer(ABC):
    """ Responsible for defining an interface  for drawing """

    @abstractmethod
    def select_pen(self, pen_num):
        pass

    @abstractmethod
    def pen_down(self):
        pass

    @abstractmethod
    def pen_up(self):
        pass

    @abstractmethod
    def go_along(self, along):
        pass

    @abstractmethod
    def go_down(self, down):
        pass

    @abstractmethod
    def draw_line(self, direction, distance):
        pass

class Parser:
    def __init__(self, new_drawer):
        self.drawer = new_drawer
        self.source = []
        self.command = ''
        self.data = 0
        self.exception_handler = ''

    def set_source(self, new_source):
        self.source = new_source

    def set_drawer(self, new_drawer):
        self.drawer = new_drawer


class AbstractParserBuilder(ABC):
    def __init__(self, new_drawer):
        self.the_parser = Parser(new_drawer)

    @abstractmethod
    def parse(self, raw_source):
        pass


class AbstractParser(ABC):
    def __init__(self, drawer, ex):
        self.drawer = drawer
        self.source = []
        self.command = ''
        self.data = 0

    @abstractmethod
    def parse(self, raw_source):
        pass


class Reader:
    def __init__(self):
        self.parser = None
        self.file_name = None
        self.source = []
        self.exception = None

    def set_parser(self, parser):
        self.parser = parser

    def set_file(self, file_name):
        self.file_name = file_name

    def set_source(self, source_list):
        self.source = source_list

    def print_attributes(self):
        print('Parser', self.parser)
        print('file_name', self.file_name)
        print('source', self.source)


class AbstractSourceReader(metaclass=ABCMeta):
    """ responsible for providing source text for parsing and drawing
        Initiates the Draw use-case.
        Links to a parser and passes the source text onwards
    """

    def __init__(self):
        self.reader = Reader()


    @abstractmethod
    def go(self):
        pass


    # def __init__(self, parser, optional_file_name=None):
    #     self.parser = parser
    #     self.file_name = optional_file_name
    #     self.source = []
    #
    # @abstractmethod
    # def go(self):
    #     pass





