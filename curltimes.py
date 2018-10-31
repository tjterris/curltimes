import re, sys

"""
while true; do curl --no-keepalive --no-sessionid -w "\nhttp_code: %{http_code}\nsize_request: %{size_request}\nlocal_port: %{local_port}\nremote_ip: %{remote_ip}\ndns_resolution: %{time_namelookup}\ntcp_established: %{time_connect}\ntime_pretransfer: %{time_pretransfer}\ntime_connect: %{time_connect}\ntime_starttransfer: %{time_starttransfer}\ntime_redirect: %{time_redirect}\nssl_handshake_done: %{time_appconnect}\ntotal_time: %{time_total}\n\n" -o /dev/null -s "https://<HOST>" >> <FILE>; sleep 1m; done

==OUTPUT==
http_code: 200
size_request: 104
local_port: 44814
remote_ip: 52.27.73.51
dns_resolution: 0.509614
tcp_established: 0.647872
time_pretransfer: 0.933368
time_connect: 0.647872
time_starttransfer: 1.221591
time_redirect: 0.000000
ssl_handshake_done: 0.933267
total_time: 1.221647
"""

infile = sys.argv[1]
f = open(infile, "r")

searchString = "total_time"
searchString2 = "ssl_handshake_done"
searchString3 = "time_connect"
searchString4 = "dns_resolution"
total_times = []
ssl_handshake_times = []
connect_times = []
dns_times = []

for line in f:
    for m in re.finditer(searchString, line):
        substring = line[m.end():None]
	    time = float(substring[2:].rstrip())
 	    total_times.append(time)

     for m in re.finditer(searchString2, line):
	     substring = line[m.end():None]
         time = float(substring[2:].rstrip())
         ssl_handshake_times.append(time)

     for m in re.finditer(searchString3, line):
         substring = line[m.end():None]
         time = float(substring[2:].rstrip())
       	 connect_times.append(time)

     for m in re.finditer(searchString4, line):
         substring = line[m.end():None]
         time = float(substring[2:].rstrip())
       	 dns_times.append(time)

total_ssl_handshake_times = [x2 - x1 for (x2, x1) in zip(ssl_handshake_times, connect_times)]

print "\nAverage ssl_handshake_time: {}".format(sum(total_ssl_handshake_times) / len(total_ssl_handshake_times))
print "Average dns_resolution_time: {}".format(sum(dns_times) / len(dns_times))
print "Average total_time: {}\n".format(sum(total_times) / len(total_times))
