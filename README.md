
InnoDB Free Space Moitor
========================
This tool monitors a InnoDB tablespace wich a autoincrement with a maximum set.

It compares the setting in the config file against the size of the file on the filesystem.

It does not check the size of the data within the tablespace, it only checks if the 
datafile is allowed to grow enough or not.

Example:

	$ ./innodb_check_free.py --critical 10000000 -c /etc/my.cnf 
	CRITICAL: Datafile ibdata1 is allowed to grow with 6291456 bytes, critical threshold is 10000000
