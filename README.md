
InnoDB Free Space Monitor
=========================
This tool monitors a InnoDB tablespace wich a autoincrement with a maximum set.

It compares the setting in the config file against the size of the file on the filesystem.

It does not check the size of the data within the tablespace, it only checks if the 
datafile is allowed to grow enough or not.

Examples:

	$ ./innodb_check_free.py --critical 10000000 -c /etc/my.cnf 
	CRITICAL: Datafile ibdata1 is allowed to grow with 6291456 bytes, critical threshold is 10000000

	$ ./innodb_check_free_pynag.py -m /etc/my.cnf -c 10000000: -w 1000000:
	WARNING: 2097152 is within warning range: 1000000: | 'ibdata1_free'=2097152;;;;


Notes on the tablespace settings in InnoDB
 - It looks like a size in KB is not actually supported (MySQL Bug #68282)

All script use Python 3 except innodb_check_free_pynag.py as pynag doesn't support Python3 yet
