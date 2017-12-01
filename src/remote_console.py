import time
from pyVmomi import vim

from tools import cli as cli, connect
from tools.get_obj import get_obj


def get_args():
    """
    Use the tools.cli methods and then add a few more arguments.
    Need -s, -o, -u, -p, -d, -c for this program.
    -o is optional, needed if talking to simulator.
    """
    parser = cli.build_arg_parser()

    parser.add_argument('-v', '--vm',
                        required=True,
                        action='store',
                        help='Name of VM')

    args = parser.parse_args()

    return cli.prompt_for_password(args)


def main():
    """
    Doesn't currently work. Could be due to the firewall. Not documented much at all from vSphere 6.0 onwards, and
    older methods no longer work.
    :return:
    """
    args = get_args()

    service_instance = connect.connect_no_ssl(args.server, args.user, args.password, args.port)
    content = service_instance.RetrieveContent()
    virtual_machine = get_obj(service_instance.content, [vim.VirtualMachine], args.vm)

    ticket = virtual_machine.AcquireTicket("webmks")


    print("Open the following URL in your browser to access the Remote Console.\n"
          "You have 60 seconds to open the URL, or the session will be terminated.\n")
    print("wss://" + ticket.host + ":443/ticket/" + ticket.ticket)
    print("Waiting for 60 seconds, then exit")
    time.sleep(60)

    return 0


if __name__ == "__main__":
    main()
