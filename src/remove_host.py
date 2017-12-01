#hello
#from pyVim import connect
from tools.connect import connect_no_ssl
from pyVmomi import vim
from pyVmomi import vmodl
from tools import cli as cli
import atexit
#from create_vm import Vcenter

def get_args():
	parser = cli.build_arg_parser()
						
	parser.add_argument('-q','--host',
						required=True,
						action='store',
						help='name of host to remove')
						
	args = parser.parse_args()
	
	return args
	
def remove_host(host):
	#TODO: check to see if cluster exists
	#if cluster exists, check for existing host by specified name
	#if exists, destroy; else, print "does not exist" exit
	host_name = host.name
	# ESXi Host enters Maintenance Mode
	host.EnterMaintenanceMode(timeout=0, evacuatePoweredOffVms=True, maintenanceSpec=None)
	while not host.runtime.inMaintenanceMode:
		time.sleep(1)
	print("ESXi Host '%s' entered in Maintenance Mode successfully!" % host_name)
	
	#print(host.config)
	# Destroy ESXi Host
	task_destroyhost = host.Destroy()
	print("never makes it here")
	while task_destroyhost.info.state == vim.TaskInfo.State.running:
		time.sleep(1)
	if task_destroyhost.info.state != vim.TaskInfo.State.success:
		raise SystemExit("ABORT: ESXi Host '%s' failed to be removed from the vC inventory" % host_name)
	print("ESXi Host '%s' removed from the vC inventory!" % host_name)

def main():
	args = get_args()
	service_instance = connect_no_ssl(host=args.server,
									  user=args.user,
									  pwd=args.password,
									  port=int(args.port))
		
	container = service_instance.RetrieveContent()
	host_view = container.viewManager.CreateContainerView(container.rootFolder,[vim.HostSystem],True)
		
	for host in host_view.view:
		if host.name == args.host:
			remove_host(host)
			break
			
	
# Start program
if __name__ == "__main__":
    main()