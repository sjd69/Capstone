from pyVim import connect
from pyVmomi import vim
from pyVmomi import vmodl
import atexit
#import tools.cli as cli
import ssl

def PrintVmInfo(vm):
	summary = vm.summary
	print("Name       : ", summary.config.name)
	print("Template   : ", summary.config.template)
	print("Path       : ", summary.config.vmPathName)
	print("Guest      : ", summary.config.guestFullName)
	annotation = summary.config.annotation
	if annotation:
		print("Annotation : ", annotation)
	print("State      : ", summary.runtime.powerState)
	if summary.guest is not None:
		ip_address = summary.guest.ipAddress
		tools_version = summary.guest.toolsStatus
		if tools_version is not None:
			print("VMware-tools: ", tools_version)
		else:
			print("Vmware-tools: None")
		if ip_address:
			print("IP         : ", ip_address)
		else:
			print("IP         : None")
	if summary.runtime.question is not None:
		print("Question  : ", summary.runtime.question.text)
	print("")
	
def main():
	service_instance = connect.SmartConnectNoSSL(host='127.0.0.1',user='user',pwd='pass',port=8989)
	
	atexit.register(connect.Disconnect, service_instance)
	content = service_instance.RetrieveContent()
	
	container = content.rootFolder
	viewType = [vim.VirtualMachine]
	recursive = True
	containerView = content.viewManager.CreateContainerView(container,viewType,recursive)
	
	children = containerView.view
	for child in children:
		PrintVmInfo(child)
		
	#except vmodl.MethodFault as error:
	#	print("Caught vmodl fault : " + error.msg)
	#	return -1

	return 0
	
	
if __name__ == "__main__":
    main()
	