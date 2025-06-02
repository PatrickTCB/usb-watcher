#!/bin/bash
/usr/sbin/ioreg -p IOUSB -a | /usr/bin/plutil -convert json -o - -