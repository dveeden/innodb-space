#!/usr/bin/python3 -tt
import sys
import os
import argparse

import innodb_tablespace_info

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--warning", type=int,
                        help="Warning threshold in bytes")
    parser.add_argument("--critical", type=int,
                        help="Critical threshold in bytes")
    parser.add_argument("-c", "--config", type=str, help="MySQL Config File")
    args = parser.parse_args()
    configfile = args.config
    if args.warning:
        twarn = args.warning
    else:
        twarn = None
    if args.critical:
        tcrit = args.critical
    else:
        tcrit = None
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
            if tcrit and datafileinfo.freesize < tcrit:
                print("CRITICAL: Datafile %s is allowed to grow with %s bytes"
                      ", critical threshold is %s"
                      % (datafile, datafileinfo.freesize, tcrit))
            elif twarn and datafileinfo.freesize < twarn:
                print("WARNING: Datafile %s is allowed to grow with %s bytes"
                      ", warning threshold is %s"
                      % (datafile, datafileinfo.freesize, twarn))
            elif twarn and tcrit:
                print("OK: Datafile %s is allowed to grow with %s bytes"
                      ", warning threshold is %s"
                      ", critical threshold is %s"
                      % (datafile, datafileinfo.freesize, twarn, tcrit))
            elif tcrit:
                print("OK: Datafile %s is allowed to grow with %s bytes"
                      ", critical threshold is %s"
                      % (datafile, datafileinfo.freesize, tcrit))
            elif twarn:
                print("OK: Datafile %s is allowed to grow with %s bytes"
                      ", warning threshold is %s"
                      % (datafile, datafileinfo.freesize, twarn))
            else:
                print("Datafile %s is allowed to grow with %s bytes"
                      % (datafile, datafileinfo.freesize))
        else:
            print("Datafile %s does not have a maximum size set" % datafile)
