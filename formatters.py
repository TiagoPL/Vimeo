import json
from abc import ABCMeta, abstractmethod


class Formatter(metaclass=ABCMeta):
    def __init__(self, headers):
        self.headers = headers

    def validate_data_size(self, data):
        if len(data) != len(self.headers):
            raise ValueError('data size != headers size')

    @abstractmethod
    def format_header(self):
        raise NotImplementedError

    @abstractmethod
    def format_footer(self):
        raise NotImplementedError

    @abstractmethod
    def format_row(self, data):
        raise NotImplementedError


class CSVFormatter(Formatter):
    def __init__(self, *args, delimiter=','):
        super().__init__(*args)
        self.delimiter = delimiter

    def format_header(self):
        return self.delimiter.join(self.headers)

    def format_footer(self):
        return ''

    def format_row(self, data):
        self.validate_data_size(data)
        return self.delimiter.join(map(str, data))


class JSONFormatter(Formatter):
    def format_header(self):
        return ''

    def format_footer(self):
        return ''

    def format_row(self, data):
        self.validate_data_size(data)
        formatted = json.dumps(dict(zip(self.headers, data)))
        return formatted
