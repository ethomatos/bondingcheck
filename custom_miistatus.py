# the following try/except block will make the custom check compatible with any Agent version
try:
	# first, try to import the base class from old versions of the Agent...
	from checks import AgentCheck

except ImportError:
	# ...if the above failed, the check is running in Agent version 6 or later
	from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class HelloCheck(AgentCheck):
	def check(self, instance):
		self.gauge('hello.world', 1, tags=['owner:et'])

"""
import argparse
import os
import subprocess

from maas_common import metric_bool
from maas_common import print_output


def bonding_ifaces_check(_):
    bonding_ifaces = os.listdir("/proc/net/bonding")
    for bonding_iface in bonding_ifaces:
        bonding_iface_check_cmd = ['cat', '/proc/net/bonding/%s'
                                   % bonding_iface]
        bonding_iface_check_cmd_output = subprocess.check_output(
            bonding_iface_check_cmd
        )

        bonding_iface_check_cmd_output_lines = (
            bonding_iface_check_cmd_output.split('\n')
        )

        has_slave_down = False
        slave_count = 0
        for idx, line in enumerate(bonding_iface_check_cmd_output_lines):
            if line.startswith("Slave Interface"):
                slave_count = slave_count + 1
                slave_inface_mii_status_line = (
                    bonding_iface_check_cmd_output_lines[idx + 1]
                )
                slave_inface_mii_status = (
                    slave_inface_mii_status_line.split(":")[1]
                )
                if 'up' not in slave_inface_mii_status or slave_count < 2:
                    has_slave_down = True

        if has_slave_down:
            metric_bool('host_bonding_iface_%s_slave_down' %
                        bonding_iface,
                        True)
        else:
            metric_bool('host_bonding_iface_%s_slave_down' %
                        bonding_iface,
                        False)


def main(args):
    bonding_ifaces_check(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Check statuses of local bonding interfaces')
    parser.add_argument('--telegraf-output',
                        action='store_true',
                        default=False,
                        help='Set the output format to telegraf')
    args = parser.parse_args()
    with print_output(print_telegraf=args.telegraf_output):
        main(args)
"""
