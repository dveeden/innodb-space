#!/usr/bin/python3 -tt
import os
import sys
import argparse
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

# Assumptions:
# - innodb_data_home_dir is not set
# - innodb_file_per_table is not set
# - files are specified w/o path

def size_to_int(size):
    unit_part = size[-1]
    size_part = int(size[:-1])
    if unit_part == 'K':
        real_size = size_part * 1024
    elif unit_part == 'M':
        real_size = size_part * 1048576
    elif unit_part == 'G':
        real_size = size_part * 1073741824
    else:
        real_size = size
    return int(real_size)

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
        retval += ('Free size: %s ' % self.freesize)
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
        fileinfo = os.stat(self.fullpath)
        return fileinfo.st_size

    @property
    def freesize(self):
        if self.maxsize:
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
    
    mysql_config = ConfigParser.RawConfigParser(allow_no_value=True)
    try:
        mysql_config.read(configfile)
    except ConfigParser.DuplicateOptionError as msg:
        print('Warning: %s' % msg)

    try:
        datadir = mysql_config.get('mysqld','datadir')
        if isinstance(datadir, list):
            datadir=datadir[0]
        datadir = datadir.strip('"')
        ibpath = mysql_config.get('mysqld','innodb_data_file_path')
        ibpath = ibpath.strip('"')
    except ConfigParser.NoOptionError as msg:
        sys.exit('Error: Required option not found: %s' % msg)
    
    print('Datadir: %s' % datadir)
    print('InnoDB Data File Path: %s' % ibpath)
    
    datafiles = {}
    keywords = ['autoextend','max']
    prevpart = None
    for part in ibpath.split(':'):
        if not part in keywords:
            if not part[0].isdigit():
                datafile = part
                datafiles[datafile] = ibdatafile(datafile)
                datafiles[datafile].datadir = datadir
            elif prevpart == 'max':
                datafiles[datafile].maxsize = part
            elif prevpart == datafile:
                datafiles[datafile].initsize = part
        elif part == 'autoextend':
            datafiles[datafile].autoextend = 'on'
        prevpart = part
                
    
    for datafile in datafiles:
        print(datafiles[datafile])
