from pyVmomi import vim

from color import color
from datacenter import create_datacenter
from get_obj import get_obj
from tools import cli as cli
from tools.connect import connect_no_ssl


def get_args():
    """
    Use the tools.cli methods and then add a few more arguments.
    Need -s, -o, -u, -p, -d, -c for this program.
    -o is optional, needed if talking to simulator.
    """
    parser = cli.build_arg_parser()

    parser.add_argument('-d', '--datacenter',
                        required=True,
                        action='store',
                        help='Name of Datacenter to create cluster in')

    parser.add_argument('-c', '--cluster',
                        required=True,
                        action='store',
                        help='Name of Cluster')

    args = parser.parse_args()

    return cli.prompt_for_password(args)


def create_cluster(service_instance, cls_name, datacenter):
    """Create a new datacenter with given name
    :param datacenter: Datacenter object to create cluster in.
    :param cls_name: Name for the new Cluster.
    :param service_instance: ServiceInstance connection to a given vCenter
    :return:
    """
    cluster = get_obj(service_instance.RetrieveContent(), [vim.ClusterComputeResource], cls_name)

    if cluster is not None:
        print("Cluster " + color.RED + "{0}".format(cls_name + color.END + " already exists."))
        return cluster
    else:
        print("Creating cluster " + color.RED + "{0}".format(cls_name) + color.END +
              " in datacenter " + color.RED + "{0}".format(datacenter.name) + color.END)
        cluster_config = vim.cluster.ConfigSpecEx()

        host = datacenter.hostFolder
        cluster = host.CreateClusterEx(name=cls_name, spec=cluster_config)
        return cluster


def main():
    args = get_args()
    service_instance = connect_no_ssl(host=args.server,
                                      user=args.user,
                                      pwd=args.password,
                                      port=int(args.port))
    datacenter = create_datacenter(service_instance, args.datacenter)
    cluster = create_cluster(service_instance, args.cluster, datacenter)

    return 0


if __name__ == "__main__":
    main()
