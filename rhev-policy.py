#!/usr/bin/env python
#
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@redhat.com)
#
# Description: Script for switching clusters policy to specified one, actually power_saving or evenly_distributed
#
# Requires ovirt-engine-sdk to work
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import sys
import getopt
import optparse
import os
import time

from ovirtsdk.api import API
from ovirtsdk.xml import params
from random import choice


description="""
RHEV-policy is a script for managing via API cluster policy

"""

# Option parsing
p = optparse.OptionParser("rhev-policy.py [arguments]",description=description)
p.add_option("-u", "--user", dest="username",help="Username to connect to RHEVM API", metavar="admin@internal",default="admin@internal")
p.add_option("-w", "--password", dest="password",help="Password to use with username", metavar="admin",default="admin")
p.add_option("-s", "--server", dest="server",help="RHEV-M server address/hostname to contact", metavar="127.0.0.1",default="127.0.0.1")
p.add_option("-p", "--port", dest="port",help="API port to contact", metavar="8443",default="8443")
p.add_option('-v', "--verbosity", dest="verbosity",help="Show messages while running", metavar='[0-n]', default=0,type='int')
p.add_option("--policy", dest="policy",help="Set destination polciy", metavar='policy', default="power_saving")

(options, args) = p.parse_args()

baseurl="https://%s:%s" % (options.server,options.port)

api = API(url=baseurl, username=options.username, password=options.password)

# FUNCTIONS

def process_cluster(clusid):
  if options.verbosity > 1:
    print "\nProcessing cluster with id %s and name %s" % (clusid,api.clusters.get(id=clusid).name)
    print "#############################################################################"
    
    cluster=api.clusters.get(id=clusid)
    cluster.scheduling_policy.policy=options.policy
    cluster.update()
    
    #evenly_distributed
    #power_saving


################################ MAIN PROGRAM ############################
#Check if we have defined needed tags and create them if missing

# Processing each cluster of our RHEVM
for cluster in api.clusters.list():
  process_cluster(cluster.id)