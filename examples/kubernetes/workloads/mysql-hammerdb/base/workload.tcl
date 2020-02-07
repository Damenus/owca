#!/bin/tclsh

global complete
proc wait_to_complete {} {
global complete
set complete [vucomplete]
if {!$complete} { after 5000 wait_to_complete } else { exit }
}


dbset db mysql
diset connection mysql_host MYSQL_HOST
diset connection mysql_port 3306
diset tpcc mysql_user testuser
diset tpcc mysql_pass testpassword
diset tpcc mysql_driver timed
diset tpcc mysql_rampup 1
diset tpcc mysql_duration 20160
print dict

loadscript
vuset vu VIRTUAL_USERS
vucreate
vurun
wait_to_complete
vwait forever
