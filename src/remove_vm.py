from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
from pyVmomi import vmodl
import atexit
import subprocess
from tools import tasks
import tools.cli as cli


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