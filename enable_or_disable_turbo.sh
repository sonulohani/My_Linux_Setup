#! /bin/bash

if [ "$1" == "0" ];then
    echo "set_cpu_turbo_off"
    echo "1" > /sys/devices/system/cpu/intel_pstate/no_turbo
else
    echo "set_cpu_turbo_on"
    echo "0" > /sys/devices/system/cpu/intel_pstate/no_turbo
fi
