import connect
import tools.cli as cli
from pyVmomi import vim
from tools import tasks


def get_args():
    """
    Use the tools.cli methods and then add a few more arguments.
    """
    parser = cli.build_arg_parser()

    parser.add_argument('-j', '--uuid',
                        required=False,
                        action='store',
                        help='UUID of VM to remove')

    parser.add_argument('-i', '--ip',
                        required=False,
                        action='store',
                        help='IP of VM to remove')

    parser.add_argument('-n', '--name',
                        required=False,
                        action='store',
                        help='Name of VM to remove')

    args = parser.parse_args()

    return cli.prompt_for_password(args)

def get_obj(content, type, name):
    """Create container view and search for object in it"""
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, type, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    container.Destroy()
    return obj


def main():
    args = get_args()

    service_instance = connect.connect_no_ssl(args.host, args.user, args.password, args.port)

    virtual_machine = None

    if args.uuid:
        virtual_machine = service_instance.content.searchIndex.FindByUuid(None, args.uuid,
                                                                          True,
                                                                          False)
    elif args.name:
        virtual_machine = get_obj(service_instance.content, [vim.VirtualMachine], args.name)
    elif args.ip:
        virtual_machine = service_instance.content.searchIndex.FindByIp(None, args.ip, True)

    if virtual_machine is None:
        raise SystemExit("Unable to locate VirtualMachine. Arguments given: "
                         "vm - {0} , uuid - {1} , name - {2} , ip - {3}"
                         .format(args.name, args.uuid, args.name, args.ip))

    print("Found: {0}".format(virtual_machine.name))
    print("The current powerState is: {0}".format(virtual_machine.runtime.powerState))
    if format(virtual_machine.runtime.powerState) == "poweredOn":
        print("Attempting to power off {0}".format(virtual_machine.name))
        task = virtual_machine.PowerOffVM_Task()
        tasks.wait_for_tasks(service_instance, [task])
        print("{0}".format(task.info.state))

    print("Destroying VM")
    task = virtual_machine.Destroy_Task()
    tasks.wait_for_tasks(service_instance, [task])
    print("Done")


if __name__ == "__main__":
    main()
