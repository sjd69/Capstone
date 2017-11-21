from pyVmomi import vim

from cluster import create_cluster
from color import color
from connect import connect_no_ssl
from datacenter import create_datacenter
from get_obj import get_obj
from tools import cli as cli


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
                        help='Name of VM')

    args = parser.parse_args()

    return cli.prompt_for_password(args)


def create_vm(service_instance, vm_name, cluster, datacenter, template_name):
    """Create a new datacenter with given name
    :param template_name: Name of the template VM.
    :param datacenter: Datacenter object that contains cluster.
    :param cluster: Cluster object to create VM in.
    :param vm_name: Name for the new VM.
    :param service_instance: ServiceInstance connection to a given vCenter
    :return:
    """
    template_vm = get_obj(service_instance.RetrieveContent(), [vim.VirtualMachine], template_name)
    resource_pool = cluster.resourcePool
    config = vim.vm.ConfigSpec()

    relocate_spec = vim.vm.RelocateSpec(pool=resource_pool)
    cloned_spec = vim.vm.CloneSpec(powerOn=True, template=False,
                                   location=relocate_spec, customization=None, config=config)

    clone = template_vm.Clone(name=vm_name, folder=datacenter.vmFolder, spec=cloned_spec)

    print("Created VM %s" % vm_name)
    return clone


def main():
    args = get_args()
    service_instance = connect_no_ssl(host=args.server,
                                      user=args.user,
                                      pwd=args.password,
                                      port=int(args.port))

    # Run through checks to see if infrastructure exists. Could just get_obj cluster though as well.
    datacenter = create_datacenter(service_instance, args.datacenter)
    cluster = create_cluster(service_instance, args.cluster, datacenter)
    if args.port == 443:
        vm = create_vm(service_instance, args.vm, cluster, datacenter, "Template_VM")
    else:
        vm = create_vm(service_instance, args.vm, cluster, datacenter, "DC0_H0_VM0")

    return 0


if __name__ == "__main__":
    main()