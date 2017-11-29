from pyVmomi import vim

from tools import cli as cli
from tools.color import color
from tools.connect import connect_no_ssl
from tools.get_obj import get_obj


def get_args():
    """
    Use the tools.cli methods and then add a few more arguments.
    Need -s, -o, -u, -p, -d, -c, -v for this program.
    -o is optional, needed if talking to simulator.
    """
    parser = cli.build_arg_parser()

    parser.add_argument('-d', '--datacenter',
                        required=True,
                        action='store',
                        help='Name of Datacenter')

    parser.add_argument('-c', '--cluster',
                        required=True,
                        action='store',
                        help='Name of Cluster')

    parser.add_argument('-v', '--vm',
                        required=True,
                        action='store',
                        help='Name/basename of VM')

    parser.add_argument('-n', '--number',
                        required=False,
                        action='store',
                        help='Number of VMs to create')

    args = parser.parse_args()

    return cli.prompt_for_password(args)


def create_vm(service_instance, vm_name, cluster, datacenter, template_name):
    """Create a new VM with a given name within given datacenter and cluster. VM is templated from given template vm
    :param str template_name: Name of the template VM.
    :param datacenter: Datacenter object that contains cluster.
    :param cluster: Cluster object to create VM in.
    :param vm_name: Name for the new VM.
    :param service_instance: ServiceInstance connection to a given vCenter
    :return: The newly created VM task
    """

    # Search the service instance content for the template VM
    template_vm = get_obj(service_instance.RetrieveContent(), [vim.VirtualMachine], template_name)

    # Set the resource pool to the cluster's resource pool as well as setup the config.
    resource_pool = cluster.resourcePool
    config = vim.vm.ConfigSpec()
    relocate_spec = vim.vm.RelocateSpec(pool=resource_pool)
    cloned_spec = vim.vm.CloneSpec(powerOn=True, template=False,
                                   location=relocate_spec, customization=None, config=config)

    # Clone the template VM into the given datacenter's VM folder using the spec we just created.
    clone = template_vm.Clone(name=vm_name, folder=datacenter.vmFolder, spec=cloned_spec)

    print("Created VM" + color.RED + " {0} ".format(vm_name) + color.END)
    return clone


def main():
    args = get_args()
    service_instance = connect_no_ssl(host=args.server,
                                      user=args.user,
                                      pwd=args.password,
                                      port=int(args.port))

    # Get the requested datacenter and cluster
    datacenter = get_obj(service_instance.RetrieveContent(), [vim.Datacenter], args.datacenter)
    cluster = get_obj(service_instance.RetrieveContent(), [vim.ClusterComputeResource], args.cluster)
    # datacenter = create_datacenter(service_instance, args.datacenter)
    # cluster = create_cluster(service_instance, args.cluster, datacenter)

    # Datacenter doesn't exist. Can't continue.
    if not datacenter:
        print("ERROR: Datacenter" + color.RED + " {0} ".format(args.datacenter) + color.END + "doesn't exist.")
        return -1

    # Cluster doesn't exist. Can't continue.
    if not cluster:
        print("ERROR: Cluster" + color.RED + " {0} ".format(args.cluster) + color.END + "doesn't exist.")
        return -1

    if args.number:
        for i in range(0, int(args.number)):
            if args.port == 443:
                create_vm(service_instance, args.vm + "_" + str(i), cluster, datacenter, "Template_VM")
            else:
                create_vm(service_instance, args.vm + "_" + str(i), cluster, datacenter, "DC0_H0_VM0")
    else:
        if args.port == 443:
            vm = create_vm(service_instance, args.vm, cluster, datacenter, "Template_VM")
        else:
            vm = create_vm(service_instance, args.vm, cluster, datacenter, "DC0_H0_VM0")

    return 0


if __name__ == "__main__":
    main()
