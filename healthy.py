# -*- coding: utf-8 -*-

#-------------------------------------------------
#  File Name：     healthy
#  Description : Checking the DNS record healthy using ping
#                 
#  Author :       mobity
#  date：          2/11/2019
#------------------------------------------------

import os,sys
import  dns.update
import dns.zone
import dns.query
import dns.resolver
from dns.rdataclass import *
from dns.rdatatype import *


def Del_Records():
    for name in Records_CNAME:
        full_name=name+'.'+domain_name
        update=dns.update.Update(domain_name)
        ping_test = "ping -c 1 " +full_name    
        if os.system(ping_test):
            datatype = dns.rdatatype.from_text("CNAME")
            update.delete(name,datatype)    
            dns.query.tcp(update,dns_ip)

    for name in Records_A:
        if '@' != name:
            full_name=name+'.'+domain_name
            update=dns.update.Update(domain_name)
            ping_test = "ping -c 1 " +full_name 
            if os.system(ping_test):
                update.delete(name) 
                dns.query.tcp(update,dns_ip)
    print "Done"
    
"""
def Update_Records(host_mame):
    update = dns.update.Update(domain_name)
    update.replace(host_mame, 300, 'a', "192.168.168.21")
    response = dns.query.tcp(update, master_ip)
"""

def Records(dns_ip,domain_name):
    Master_Zone=dns.zone.from_xfr(dns.query.xfr(dns_ip,domain_name))
    for nodes in Master_Zone:
        node=Master_Zone.get_node(nodes)
        for record in node:
            if record.rdtype== dns.rdatatype.SOA:
                continue
            if record.rdtype== dns.rdatatype.A:
                host_name=Master_Zone[nodes].to_text(nodes).split(" ")[0]
                Records_A.append(host_name)
            if record.rdtype== dns.rdatatype.CNAME:
                host_name=Master_Zone[nodes].to_text(nodes).split(" ")[0]
                Records_CNAME.append(host_name)
    

def usage():
    print '----------------------------------------------------------------------------'
    print 'USAGE: python healthy.py <domain_name> <DNS IP>'
    print 'for example:'
    print 'python healthy.py xenmobile.com 192.168.168.1'
    print '-----------------------------------------------------------------------------'

Records_A=[]
Records_CNAME=[]

if len(sys.argv) <3:
    usage()
    sys.exit()
else:
    domain_name=sys.argv[1]
    dns_ip=sys.argv[2]
    Records=Records(dns_ip,domain_name)
    Del_Records()


