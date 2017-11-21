from pyVmomi import vim

from color import color
from get_obj import get_obj
from tools import cli, tasks
from tools.connect import connect_no_ssl
from tools.ide import find_free_ide_controller


def get_args():
    """
    Use the tools.cli methods and then add a few more arguments.
    """
    parser = cli.build_arg_parser()

    parser.add_argument('-v', '--vm',
                        required=True,
                        action='store',
                        help='Name of VM')

    parser.add_argument('-i', '--iso',
                        required=True,
                        action='store',
                        help='Path of iso (Absolute)')

    args = parser.parse_args()

    return cli.prompt_for_password(args)


def attach_iso(service_instance, vm, iso_path):
    connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    connectable.allowGuestControl = True
    connectable.startConnected = True

    cdrom = vim.vm.device.VirtualCdrom()
    cdrom.controllerKey = find_free_ide_controller(vm).key
    cdrom.key = -1
    cdrom.connectable = connectable
    cdrom.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo(fileName=iso_path)
    op = vim.vm.device.VirtualDeviceSpec.Operation
    devSpec = vim.vm.device.VirtualDeviceSpec()
    devSpec.operation = op.add
    devSpec.device = cdrom

    print("Attaching iso to CD drive of " + color.RED + "{0} ".format(vm.name) + color.END)
    cdspec = None

    vmconf = vim.vm.ConfigSpec()
    vmconf.deviceChange = [devSpec]
    print("Giving first priority for CDrom Device in boot order")
    vmconf.bootOptions = vim.vm.BootOptions(bootOrder=[vim.vm.BootOptions.BootableCdromDevice()])

    task = vm.ReconfigVM_Task(vmconf)
    tasks.wait_for_tasks(service_instance, [task])

    print("Successfully changed boot priority and attached iso to  " + color.RED + "{0} ".format(vm.name) + color.END)


def main():
    args = get_args()
    service_instance = connect_no_ssl(host=args.server,
                                      user=args.user,
                                      pwd=args.password,
                                      port=int(args.port))

    vm = get_obj(service_instance.RetrieveContent(), [vim.VirtualMachine], args.vm)

    attach_iso(service_instance, vm, args.iso)

    return 0


# Start program
if __name__ == "__main__":
    main()
