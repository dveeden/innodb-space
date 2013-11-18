#!/usr/bin/python3 -tt
'''
Get info about InnoDB table spaces.

This uses the my.cnf file and access to the filesystem.

Assumptions:
- innodb_data_home_dir is not set
- innodb_file_per_table is not set
- files are specified w/o path
- no raw device tablespaces are in use
'''

import os
import sys
import argparse
import logging
try:
    import ConfigParser
except ImportError:    # For Python 3.x
    import configparser as ConfigParser


def size_to_int(size):
    '''Get size in bytes from human readable size like 100M, 10G'''

    unit_part = size[-1]
    size_part = int(size[:-1])
    if unit_part == 'K':
        real_size = size_part * 1024
    elif unit_part == 'M':
        real_size = size_part * 1048576
    elif unit_part == 'G':
        real_size = size_part * 1073741824
    elif unit_part.isdigit():
        real_size = size
    else:
        raise ValueError('%s is not a valid size' % size)
    return int(real_size)


def parse_mysql_config(configfile):
    '''Get datadir and InnoDB data file path from the my.cnf'''

    mysql_config = ConfigParser.RawConfigParser(allow_no_value=True)
    try:
        mysql_config.read(configfile)
    except ConfigParser.DuplicateOptionError as msg:
        logging.warn('%s', msg)

    try:
        datadir = mysql_config.get('mysqld', 'datadir')
        if isinstance(datadir, list):
            datadir = datadir[0]
        datadir = datadir.strip('"')
        ibpath = mysql_config.get('mysqld', 'innodb_data_file_path')
        ibpath = ibpath.strip('"')
    except ConfigParser.NoOptionError as msg:
        logging.critical('Required option not found: %s', msg)
        raise

    return (datadir, ibpath)


def check_datafiles(datadir, ibpath):
    datafiles = {}
    for datafileconfig in ibpath.split(';'):
        parts = datafileconfig.split(':')
        datafile = parts[0]
        datafiles[datafile] = ibdatafile(datafile)
        datafiles[datafile].datadir = datadir
        datafiles[datafile].initsize = parts[1]
        if 'autoextend' in parts:
            datafiles[datafile].autoextend = 'on'
        if 'max' in parts:
            # Find the index numer for the location of 'max' in the parts list
            max_index = [i for i, x in enumerate(parts) if x == 'max'][0]
            maxsize = parts[max_index + 1]
            datafiles[datafile].maxsize = maxsize
    return datafiles


class ibdatafile(object):
    def __init__(self, datafile):
        self.datafile = datafile
        self._initsize = None
        self._maxsize = None
        self.autoextend = None
        self.datadir = None

    def __str__(self):
        retval = ('Datafile: %s, ' % self.datafile)
        retval += ('Initial size: %s, ' % self.initsize)
        retval += ('Max size: %s, ' % self.maxsize)
        retval += ('Autoextend: %s, ' % self.autoextend)
        retval += ('Current size: %s, ' % self.cursize)
        retval += ('Free size: %s, ' % self.freesize)
        retval += ('File exists: %s ' % self.file_exists)
        return retval

    @property
    def fullpath(self):
        if self.datadir:
            fullpath = os.path.join(self.datadir, self.datafile)
        else:
            fullpath = self.datafile
        return fullpath

    @property
    def cursize(self):
        if not self.file_exists is True:
            return None
        try:
            fileinfo = os.stat(self.fullpath)
        except FileNotFoundError:
            fileinfo = None
        return fileinfo.st_size

    @property
    def file_exists(self):
        if os.path.exists(self.fullpath):
            return True
        else:
            return False

    @property
    def freesize(self):
        if self.maxsize and self.cursize:
            freesize = self.maxsize - self.cursize
        else:
            freesize = None
        return freesize

    @property
    def maxsize(self):
        if self._maxsize:
            return self._maxsize

    @maxsize.setter
    def maxsize(self, newsize):
        self._maxsize = size_to_int(newsize)

    @property
    def initsize(self):
        if self._initsize:
            return self._initsize

    @initsize.setter
    def initsize(self, newsize):
        self._initsize = size_to_int(newsize)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, help="MySQL Config File")
    args = parser.parse_args()
    configfile = args.config
    if args.config is None:
        print('Error: No config file specified')
        parser.print_usage()
        sys.exit(1)

    if not os.path.exists(configfile):
        sys.exit('Error: Config file %s does not exist' % configfile)

    datadir, ibpath = parse_mysql_config(configfile)

    print('Datadir: %s' % datadir)
    print('InnoDB Data File Path: %s\n' % ibpath)

    datafiles = check_datafiles(datadir, ibpath)

    for datafile in datafiles:
        print(datafiles[datafile])
