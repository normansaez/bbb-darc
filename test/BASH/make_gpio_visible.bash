for i in $(seq 127)
    do
        echo $i > /sys/class/gpio/export
        echo out > /sys/class/gpio/gpio$i/direction
        echo 0 > /sys/class/gpio/gpio$i/value
    done


