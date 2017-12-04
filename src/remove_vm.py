from pyVmomi import vim

import tools.cli as cli
from tools import tasks, connect
from tools.get_obj import get_obj
from tools.power import power_off_vm


def get_args():
    """
    Use the tools.cli methods and then add a few more arguments.
    Need -s, -o, -u, -p for this program.
    -o is optional, needed if talking to simulator.
    Either one of j, i, or v is required.
    """
    parser = cli.build_arg_parser()

    parser.add_argument('-j', '--uuid',
                        required=False,
                        action='store',
                        help='UUID of VM to remove')

    parser.add_argument('-i', '--ip',
                        required=False,
                        action='store',
                        help='DNS IP of VM to remove')

    parser.add_argument('-v', '--vm',
                        required=False,
                        action='store',
                        help='Name of VM to remove')

    args = parser.parse_args()

    return cli.prompt_for_password(args)


def main():
    args = get_args()

    service_instance = connect.connect_no_ssl(args.server, args.user, args.password, args.port)

    virtual_machine = None

    if args.uuid:
        virtual_machine = service_instance.content.searchIndex.FindByUuid(None, args.uuid, True, False)
    elif args.vm:
        virtual_machine = get_obj(service_instance.content, [vim.VirtualMachine], args.vm)
    elif args.ip:
        virtual_machine = service_instance.content.searchIndex.FindByIp(None, args.ip, True)

    if virtual_machine is None:
        raise SystemExit("Unable to locate VirtualMachine. Arguments given: "
                         "vm - {0} , uuid - {1} , ip - {2}"
                         .format(args.vm, args.uuid, args.ip))

    print("Found: {0}".format(virtual_machine.name))
    print("The current powerState is: {0}".format(virtual_machine.runtime.powerState))
    if format(virtual_machine.runtime.powerState) == "poweredOn":
        print("Attempting to power off {0}".format(virtual_machine.name))
        task = power_off_vm(service_instance, virtual_machine)
        print("{0}".format(task.info.state))

    print("Destroying VM")
    task = virtual_machine.Destroy_Task()
    tasks.wait_for_tasks(service_instance, [task])

    print("{0}".format(task.info.state))

    return 0


if __name__ == "__main__":
    main()
