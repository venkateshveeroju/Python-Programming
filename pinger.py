#!/user/bin/python3
from fping import FastPing
import fping
import os
import subprocess

def parse(s):
 
    [host, s1]          = s.split(" : ")
    [stats, ping]       = s1.split(", ")

    # get packet loss %
    [_, s2]             = stats.split(" = ")
    [sent, recv, loss]  = s2.split("/")

    # get avg latency
    [_, s3]             = ping.split(" = ")
    [min_, avg, max_]   = s3.split("/")

    return {
        "host": host,
        "sent": sent,
        "recv": recv,
        "loss": loss.strip("%"),
        "min":  min_,
        "avg":  avg,
        "max":  max_
    }

	
#hostname='8.8.8.8'
cmd = subprocess.run(["fping", '-c', '2', '-q', hostname], stdout=subprocess.PIPE,            stderr=subprocess.STDOUT)
output = cmd.stdout.decode("utf-8").strip()
parsed = parse(output)

print(parsed['loss'])
print(parsed['avg'])
