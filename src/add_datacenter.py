from pyVmomi import vim

from tools import cli as cli
from tools.color import color
from tools.connect import connect_no_ssl
from tools.get_obj import get_obj


def get_args():
    """
    Use the tools.cli methods and then add a few more arguments.
    Need -s, -o, -u, -p, -d for this program.
    -o is optional, needed if talking to simulator.
    """
    parser = cli.build_arg_parser()

    parser.add_argument('-d', '--datacenter',
                        required=True,
                        action='store',
                        help='Name of Datacenter')

    args = parser.parse_args()

    return cli.prompt_for_password(args)


def create_datacenter(service_instance, dc_name, folder=None):
    """Create a new datacenter with given name
    :param folder: Folder object to create DC in. If None it will default to rootFolder
    :param dc_name: Name for the new Datacenter.
    :param service_instance: root service instance of a given server
    :return: Either the existing datacenter with given name, or a newly created datacenter
    """
    datacenter = get_obj(service_instance.RetrieveContent(), [vim.Datacenter], dc_name)

    if datacenter is not None:
        print("Datacenter " + color.RED + "{0}".format(dc_name + color.END + " already exists."))
        return datacenter
    else:
        if len(dc_name) > 79:
            raise ValueError("Datacenter name must be under 80 characters.")
        if folder is None:
            folder = service_instance.content.rootFolder
        if isinstance(folder, vim.Folder):
            datacenter = folder.CreateDatacenter(name=dc_name)
            print("Created datacenter " + color.RED + "{0}".format(dc_name) + color.END +
                  " in folder " + color.RED + "{0}".format(folder.name) + color.END)
        return datacenter


def main():
    args = get_args()
    service_instance = connect_no_ssl(host=args.server,
                                      user=args.user,
                                      pwd=args.password,
                                      port=int(args.port))

    datacenter = create_datacenter(service_instance, args.datacenter)

    return 0


if __name__ == "__main__":
    main()
