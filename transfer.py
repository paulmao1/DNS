# -*- coding: utf-8 -*-

#-------------------------------------------------
#  File Name：     tranfer
#  Description :  This is DNS zone transfer sample. 
#                 Not apply to Master-Slave deployment.
#  Author :       mobity
#  date：          2/11/2019
#------------------------------------------------

import os,sys,time
import  dns.update
import dns.zone
import dns.query
import dns.tsigkeyring
import dns.resolver
from dns.rdataclass import *
from dns.rdatatype import *


def diff_zone(zone1,zone2,ignore_ttl=True):
    differences = []
    for node in zone1:
        namestr=str(node)
        n1=zone1.get_node(namestr)
	n2=zone2.get_node(namestr)
	if not n2:
	    differences.append((namestr,n1,n2))
	elif diff_node(n1,n2):
	    differences.append((namestr,n1,n2))
    for node in zone2:
	n3=zone1.get_node(namestr)
	if not n3:
	    n4=zone2.get_node(namestr)
	    differences.append((namestr,n3,n4))
    return differences	     

def diff_node(n1,n2):
    for record in n1.rdatasets:
	if record.rdtype == dns.rdatatype.SOA:
            continue
	if record not in n2.rdatasets:
	    return True
    for record in n2.rdatasets:
	if record.rdtype == dns.rdatatype.SOA:
	    continue
	if record not in n1.rdatasets:
	    return True

"""
def Update_Records(differences):
    for name,mater,slave in differences:
        for node in zone1.nodes:
            if name== str(node):
                host_ipaddr=zone1[node].to_text(node).split(" ")[-1] 
                update = dns.update.Update(domain_name,keyring=keyring)
                update.replace(name, 300, 'a', host_ipaddr)
                dns.query.tcp(update, slave_ip)
                print "Done"
            continue 
"""

def Records(differences):
    for name,master,slave in differences:
        if master:
            for record in master.rdatasets:
                value=record[-1]
                update = dns.update.Update(domain_name)
                update.add(name,record.ttl,record.rdtype,str(value))
                dns.query.tcp(update, slave_ip)
        else:
            print "Record is none on the master zone"        

def usage():
    print '----------------------------------------------------------------------------'
    print 'USAGE: python transfer.py <domain_name> <zone1_ip> <zone2_ip>'
    print 'for example:'
    print 'python transfer.py xenmobile.com 192.168.168.1 192.168.168.2'
    print '-----------------------------------------------------------------------------'

if len(sys.argv) <4:
    usage()
    sys.exit()
else:
    domain_name=sys.argv[1]
    master_ip=sys.argv[2]
    slave_ip=sys.argv[3]
    keyring = dns.tsigkeyring.from_text({'rndc-key' : 'svJxyxYhji9Vxcz42n+S7w=='})
    zone1=dns.zone.from_xfr(dns.query.xfr(master_ip, domain_name))
    zone2=dns.zone.from_xfr(dns.query.xfr(slave_ip, domain_name))
    soa1 = zone1.get_rdataset('@', 'SOA')
    soa2 = zone2.get_rdataset('@', 'SOA')
    serial1=soa1[0].serial
    serial2=soa2[0].serial

    if serial1 == serial2:
        print "No updates for two zones"
    elif  serial1 < serial2:  
        print "You shoudn't add record on the slave zones"
    else:
        differences=diff_zone(zone1,zone2)
    if not len(differences):
        print "No updates for two zones"
    else:
        Records(differences)       
