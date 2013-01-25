#!/usr/bin/tclsh8.4
while 1 {
    set time [
        time { exec /usr/local/bin/python /home/tester/tools/python/python_project/sbu_pdt/version_get.py > /dev/null 2>&1}
    ]
    #Sleep, Accurate to millisecond
    if [regexp {\d+} $time microseconds] {
        after [expr [expr 60000000-$microseconds]/1000]
        continue
    } else {
        puts "Didn't get the time"
        exit
    }
}
