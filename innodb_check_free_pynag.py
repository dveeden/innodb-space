#!/usr/bin/python -tt
#Use Python 2 instead of Python 3 as pynag does not yet work with Python 3
'''
Example:

./innodb_check_free_pynag.py -m /etc/my.cnf -c 10000000: -w 1000000:
WARNING: 2097152 is within warning range: 1000000: | 'ibdata1_free'=2097152;;;;
'''
import os

import pynag
import innodb_tablespace_info

if __name__ == '__main__':
    np = pynag.Plugins.simple()
    np.add_arg("m", "mysqlconfig", "MySQL Config File", required=True)
    np.activate()

    if np['mysqlconfig']:
        configfile = np['mysqlconfig']
    else:
        print('Error: No config file specified')
        sys.exit(1)

    if not os.path.exists(configfile):
        np.nagios_exit(pynag.Plugins.UNKNOWN, ('Config file %s does not exist' % configfile))

    datadir, ibpath = innodb_tablespace_info.parse_mysql_config(configfile)

    datafiles = innodb_tablespace_info.check_datafiles(datadir, ibpath)

    for datafile in datafiles:
        datafileinfo = datafiles[datafile]
        if datafileinfo.maxsize and datafileinfo.autoextend:
            freesize = datafileinfo.freesize
            np.add_perfdata("%s_free" % datafile, freesize)
            np.check_range(freesize)
