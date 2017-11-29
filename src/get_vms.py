from pyVim import connect
from pyVmomi import vim
from pyVmomi import vmodl
import atexit
# import tools.cli as cli
import ssl

from tools import cli
from tools.connect import connect_no_ssl


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
    args = cli.get_args()

    service_instance = connect_no_ssl(host=args.server,
                                      user=args.user,
                                      pwd=args.password,
                                      port=int(args.port))
    content = service_instance.RetrieveContent()

    container = content.rootFolder
    view_type = [vim.VirtualMachine]
    recursive = True
    container_view = content.viewManager.CreateContainerView(container, view_type, recursive)

    children = container_view.view
    for child in children:
        PrintVmInfo(child)

    # except vmodl.MethodFault as error:
    #	print("Caught vmodl fault : " + error.msg)
    #	return -1

    return 0


if __name__ == "__main__":
    main()
