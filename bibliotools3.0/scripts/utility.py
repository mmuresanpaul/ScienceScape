#! /usr/bin/env python

#outer modules
import os
import sys
import glob
import numpy
import argparse
import re

#personal modules
import utilities
'''
This class contains logic for various utilities used thoughout the scripts.
It has a collection of all the items from the .dat files and the WOS Lines from 
the initial files.
'''
class Utility:
    # TODO Use config file accessors instead when the config file is working!
    #list for all the utily objects
    __articles = []
    __authors = []
    __countries = []
    __institutions = []
    __keywords = []
    __labs = []
    __refs = []
    __subjects = []

    __woslines = []

    #dictionary for all the objects
    collection = { 'articles': __articles , 'authors' : __authors,
            'countries' : __countries, 'institutions' : __institutions,
            'keywords' : __keywords, 'labs' : __labs, 'references' : __refs,
            'subjects' : __subjects, 'woslines' : __woslines }

    '''
        Takes a path of a file and return the file's name without the extension.
        eg: /foo/bar/test.txt returns test
    '''
    def file_name(file_path):
        base = os.path.basename(file_path)
        return os.path.splitext(base)[0]

    '''
        Reads from a given .dat file which is targeted to a specific object.
        Based on what object is chosen, a new object of that type is created,
        for every line of the file. Every line gets passed to its constructor.
    '''
    def read_file(file_path, object_name):
        with open(file_path) as f:
            content = [x.strip('\n') for x in f.readlines()]
            for line in content:
                #parse line based on object type
                object_name = Utility.file_name(file_path)
                re_line = re.split('\t', line)
                Utility.collection[object_name].append(
                    Utility.new_object(object_name, re_line))

    '''
        Takes a WOS txt file as source and creates a WOS Line in the collection.
    '''
    def init_wos(src):
        with open(src) as f:
            content = [x.strip('\n') for x in f.readlines()]
            has_header = False
            for line in content:
                if line != "":
                    re_line = line.replace('\xef\xbb\xbf','').split('\t')
                    if not has_header: # define columns thanks to 1st line
                        from utilities import wosline
                        (def_cols, num_cols) = wosline.defColumns(re_line)
                        has_header = True
                    elif has_header: # do not take 1st line into account!
                        Utility.collection['woslines'].append(wosline.Wosline(re_line, def_cols, num_cols))

    '''
        Takes a list of .dat files corrresponding to the items in the
        collection, and populates the items based on the data.
    '''
    def init_utilities(files_list):
        #after we have .dat files created by parser, use utility to store them
        #in the collection
        for path in files_list:
            name = path.strip('.dat')
            Utility.read_file(path, name)

    '''
        A factory that creates items based on a given name. It passes the given
        line to its constructor.
        Returns the created item.
    '''
    def new_object(object_name, line):
        if(object_name == 'articles'):
            from utilities import article
            return article.Article(line)
        elif(object_name == 'authors'):
            from utilites import author
            return author.Author(line)
        elif(object_name == 'countries'):
            from utilites import country
            return country.Country(line)
        elif(object_name == 'institutions'):
            from utilites import institution
            return institution.Institution(line)
        elif('keywords' in object_name):
            from utilites import keyword
            return keyword.Keyword(line)
        elif(object_name == 'labs'):
            from utilities import lab
            return keyword.Lab(line)
        elif(object_name == 'refs'):
            from utilities import ref
            return ref.Ref(line)
        elif(object_name == 'subjects'):
            from utilities import subject
            return subject.Subject(line)
        elif(object_name == 'woslines'):
            from utilities import wosline
            return wosline.WosLine(line)

    def __str__():
       return str(collection) 
