#!/usr/bin/python3 -tt
import sys
import os
import argparse

import innodb_tablespace_info

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

    datadir, ibpath = innodb_tablespace_info.parse_mysql_config(configfile)

    datafiles = innodb_tablespace_info.check_datafiles(datadir, ibpath)

    for datafile in datafiles:
        datafileinfo = datafiles[datafile]
        if datafileinfo.maxsize and datafileinfo.autoextend:
            print("Datafile %s is allowed to grow with %s bytes"
                  % (datafile, datafileinfo.freesize))
        else:
            print("Datafile %s does not have a maximum size set" % datafile)
