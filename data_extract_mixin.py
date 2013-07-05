#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DataExtractMixin(object):
    _fields = {}
    def __call__(self, fields):
        self._fields = fields

    def __getattribute__(self, item):
        if item == '_fields':
            return object.__getattribute__(self, '_fields')

        if item in object.__getattribute__(self, 'ExtractedFields'):
            return self._fields.get(item, None)

        return super(DataExtractMixin, self).__getattribute__(item)

    def __setattr__(self, key, value):
        if key in self.ExtractedFields:
            self._fields[key] = value
        else:
            self.__dict__[key] = value
            #object.__setattr__(self, key, value)


class ParserNew(DataExtractMixin, object):
    ExtractedFields = ['a', 'b', 'c']
    def parse(self, data):
        self.a = data['a']
        self.b = data['b']
        self.c = data['c']

    def get_data(self):
        #return parsed data
        return [self.a, self.b, self.c]

    def build(self):
        #return original raw data
        return {'a': self.a, 'b': self.b, 'c': self.c}




if __name__ == '__main__':
    #super-puper raw binary protocol packets
    packet_list = [
        {'a': 1, 'b': 2, 'c': 3},
        {'a': 123, 'b': 2244, 'c': 34},
        {'a': 341, 'b': 32, 'c': 323},
    ]

    #old things
    class Parser(object):
        def __init__(self, data):
            #inside data
            self.a = self.b = self.c = None
            self.parse(data)

        def parse(self, data):
            self.a = data['a']
            self.b = data['b']
            self.c = data['c']

        def get_data(self):
            #return parsed data
            return [self.a, self.b, self.c]

        def build(self):
            #return original raw data
            return {'a': self.a, 'b': self.b, 'c': self.c}

    for packet in packet_list:
        #parse data
        pk_parser = Parser(packet)
        data = pk_parser.get_data()
        print data
        #make changes in packet/or make new
        pk_parser.a = data[0] + 10
        #make raw
        print pk_parser.build()

    #summary:
    #by every packet we have new object (need memory and time to build object from class)

    #new things
    pk_parser = ParserNew()
    extract_data_list = []
    for packet in packet_list:
        extract_data = {}
        extract_data_list.append(extract_data)
        #init
        pk_parser(extract_data)
        #parse data
        pk_parser.parse(packet)
        data = pk_parser.get_data()
        print data
        #make changes in packet/or make new
        pk_parser.a = data[0] + 10
        #make raw
        print pk_parser.build()

    print extract_data_list