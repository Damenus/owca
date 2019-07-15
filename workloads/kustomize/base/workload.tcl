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
puts "SETTING CONFIGURATION"
dbset db mysql
diset connection mysql_host mysql
diset connection mysql_port 3306
diset tpcc mysql_user testuser
diset tpcc mysql_pass testpassword
diset tpcc mysql_driver timed
diset tpcc my_rampup 2
diset tpcc my_duration 5
vuset logtotemp 1
loadscript
puts "SEQUENCE STARTED"
foreach z { 1 2 } {
puts "$z VU TEST"
vuset vu $z
vucreate
vurun
runtimer 600
vudestroy
after 5000
        }
puts "TEST SEQUENCE COMPLETE"