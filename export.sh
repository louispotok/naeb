#!/usr/bin/env bash

# from https://coderwall.com/p/byoycg/export-all-tables-in-a-sqlite3-db-to-csv-files
# with minor modifications

# obtains all data tables from database
# the `--init FAKE` prevents my .sqliterc file from mesisng this up
TS=`sqlite3 $1 --init FAKE "SELECT tbl_name FROM sqlite_master WHERE type='table' and tbl_name not like 'sqlite_%';"`

# exports each table to csv
for T in $TS; do

sqlite3 $1 --init FAKE <<!
.headers on
.mode csv
.output data/naeb_dump/$T.csv
select * from $T;
!

done
