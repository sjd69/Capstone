from pyVmomi import vim

from tools import cli, tasks
from tools.color import color
from tools.connect import connect_no_ssl
from tools.get_obj import get_obj
from tools.ide import find_free_ide_controller
from tools.power import power_off_vm


def get_args():
    """
    Use the tools.cli methods and then add a few more arguments.
    Need -s, -o, -u, -p, -i, v for this program.
    -o is optional, needed if talking to simulator.
    """
    parser = cli.build_arg_parser()

    parser.add_argument('-v', '--vm',
                        required=True,
                        action='store',
                        help='Name of VM')

    parser.add_argument('-i', '--iso',
                        required=True,
                        action='store',
                        help='Datastore path of ISO')

    args = parser.parse_args()

    return cli.prompt_for_password(args)


def attach_iso(service_instance, vm, iso_path):
    """
    Attach an ISO to a VM
    :param service_instance: The root service instance of the connected server
    :param vm: The VM to attach the iso to.
    :param iso_path: The datastore path to the iso file.
    :return:
    """

    # Create a configuration for the connectable virtual device (CD-ROM in this case)
    # Configure it to start when the VM does, as well as enable guest control.
    connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    connectable.allowGuestControl = True
    connectable.startConnected = True

    # Create a virtual CD-ROM. Attach it to a free IDE controller on the VM.
    cdrom = vim.vm.device.VirtualCdrom()
    cdrom.controllerKey = find_free_ide_controller(vm).key
    cdrom.key = -1
    cdrom.connectable = connectable
    cdrom.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo(fileName=iso_path)

    # Add the virtual device to the VM.
    op = vim.vm.device.VirtualDeviceSpec.Operation
    dev_spec = vim.vm.device.VirtualDeviceSpec()
    dev_spec.operation = op.add
    dev_spec.device = cdrom

    print("Attaching iso to CD drive of " + color.RED + "{0} ".format(vm.name) + color.END)
    # cd_spec = None

    # Reconfigure the boot priority on the VM to boot from the CD-ROM.
    vm_conf = vim.vm.ConfigSpec()
    vm_conf.deviceChange = [dev_spec]
    print("Giving first priority for CDrom Device in boot order")
    vm_conf.bootOptions = vim.vm.BootOptions(bootOrder=[vim.vm.BootOptions.BootableCdromDevice()])

    if format(vm.runtime.powerState) == "poweredOn":
        print("Attempting to reboot" + color.RED + " {0}".format(vm.name) + color.END)
        task = power_off_vm(service_instance, vm)
        print("{0}".format(task.info.state))

    task = vm.ReconfigVM_Task(vm_conf)
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
