

sudo bash -c "echo '0' > /proc/sys/kernel/randomize_va_space"
ulimit -a
ulimit -c unlimited

