#!/bin/tclsh
proc runtimer { seconds } {
set x 0
set timerstop 0
while {!$timerstop} {
incr x
after 1000
  if { ![ expr {$x % 60} ] } {
          set y [ expr $x / 60 ]
          puts "Timer: $y minutes elapsed"
  }
update
if {  [ vucomplete ] || $x eq $seconds } { set timerstop 1 }
    }
return
}
dbset db mysql
diset connection mysql_host MYSQL_HOST
diset connection mysql_port 3306
diset tpcc mysql_user testuser
diset tpcc mysql_pass testpassword
diset tpcc mysql_driver timed
diset tpcc my_duration 5
print dict

loadscript
vuset vu WORKER_NUMBER
vucreate
vurun
runtimer 600
after 5000