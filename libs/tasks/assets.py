# -*- coding: utf-8 -*-

from os import getenv

from .ansible import *
from .rest_client import RestClient
from .inventory import *


def base_refresh():

	inventory_hosts = get_region_inventory()

	runner = run('base_refresh', inventory_hosts)

	ansible_result = parse(runner.events)

	rest_client = RestClient()
	rest_client.auth()

	for asset in ansible_result:
		export = {'system': ansible_result[asset]['Distribution']['result'],
			'system_version': ansible_result[asset]['Distribution version']['result'],
			'hardware_vendor': ansible_result[asset]['Hardware vendor']['result'],
			'processor': ansible_result[asset]['Processor']['result'],
			'timezone': ansible_result[asset]['Timezone']['result'],
			'hostname': ansible_result[asset]['Hostname']['result'],
			'reboot_required': ansible_result[asset]['Reboot Required']['result'],
			'uptime': ansible_result[asset]['Uptime']['result'],
			'selinux': ansible_result[asset]['SELinux']['result'],
			'docker': ansible_result[asset]['Docker']['result'],
			'packages': ansible_result[asset]['Packages']['result'],
			'upgradable_packages': ansible_result[asset]['Upgradable Packages']['result'],
			'memory_used': ansible_result[asset]['Memory Used']['result'],
			'memory_total': ansible_result[asset]['Memory Total']['result'],
			'cpu_usage': ansible_result[asset]['CPU Usage']['result'],
			'kernel_version': ansible_result[asset]['Kernel']['result'],
      'process_usage': ansible_result[asset]['Process Usage']['result'],
      'bandwidth_interfaces': ansible_result[asset]['Bandwidth Interfaces']['result']
		}
		rest_client.put('assets/{}/meta'.format(asset, ), export)
		rest_client.put('assets/{}/users'.format(asset, ), ansible_result[asset]['Users']['result'])
		rest_client.put('assets/{}/storage'.format(asset, ), ansible_result[asset]['Storage']['result'])
		rest_client.put('assets/{}/interfaces'.format(asset, ), ansible_result[asset]['Interfaces']['result'])
	clear()


def playbook(playbook, asset, params=dict()):
	asset = format_inventory(asset)
	runner = run(playbook, asset, params)
	parse(runner.events)
	clear()
