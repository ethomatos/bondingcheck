# the following try/except block will make the custom check compatible with any Agent version
try:
	# first, try to import the base class from old versions of the Agent...
	from checks import AgentCheck

except ImportError:
	# ...if the above failed, the check is running in Agent version 6 or later
	from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

import os
import subprocess
import argparse

class BondingCheck(AgentCheck):
	def check(self, instance):
		dir = "/home/ec2-user/bonding"
		bonds = os.listdir(dir)
		for bond in bonds:
			cmd = ['cat', dir+'/%s' % bond]
			output = subprocess.check_output(cmd)
			output_lines = output.split('\n')
			slave_down = False
			slave_count = 0
			for idx, line in enumerate(output_lines):
				if line.startswith("Slave Interface"):
					slave_count += 1
					slave_miistatus_line = output_lines[idx + 1]
					slave_miistatus = slave_miistatus_line.split(":")[1]
					if 'up' not in slave_miistatus or slave_count < 2:
						slave_down = True
					metric = bond + '_slave_down'
					tag = 'hostbond:' + bond
					if slave_down:
						self.gauge(metric, True, tags=['owner:et',tag])
						self.service_check('BondingCheckStatus', self.WARNING, tags=None, message="")
	        else:
						self.gauge(metric, False, tags=['owner:et',tag])
						self.service_check('BondingCheckStatus', self.OK, tags=None, message="")
