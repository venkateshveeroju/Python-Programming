from fping import FastPing;
fp = FastPing()
fp.ping(filename='testing')
cmd =  ['/usr/local/sbin/fping', '-nV', '8.8.8.8',
        'www.google.com', '206.190.36.45', 'localhost',
        'host.cannotresolve.com']