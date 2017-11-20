# VMware vSphere Python SDK Community Samples Addons
# Copyright (c) 2014 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module implements simple helper functions for python samples

Modified to include arguments for VCSim tools
"""
import argparse
import getpass

__author__ = "VMware, Inc."


def build_arg_parser():
    """
    Builds a standard argument parser with arguments for talking to vCenter

    -s service_host_name_or_ip
    -o optional_port_number
    -u required_user
    -p optional_password

    """
    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to vCenter')

    # because -h is reserved for 'help' we use -s for service
    parser.add_argument('-s', '--server',
                        required=True,
                        action='store',
                        help='vSphere service to connect to')

    # because we want -p for password, we use -o for port
    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='User name for server')

    parser.add_argument('-p', '--password',
                        required=True,
                        action='store',
                        help='Password for server')

    # # -s, -S, and -h are already taken, so using -t for the host IP
    # parser.add_argument('-t', '--host',
    #                     required=False,
    #                     action='store',
    #                     help='Host IP')
    #
    # parser.add_argument('-U', '--user',
    #                     required=True,
    #                     action='store',
    #                     help='User name for host')
    #
    # parser.add_argument('-P', '--password',
    #                     required=True,
    #                     action='store',
    #                     help='Password for host')
    #
    # parser.add_argument('-S', '--disable_ssl_verification',
    #                     required=False,
    #                     action='store_true',
    #                     help='Disable ssl host certificate verification')
    #
    # parser.add_argument('-d', '--datacenter',
    #                     required=False,
    #                     action='store',
    #                     help='Name of Datacenter')
    #
    # parser.add_argument('-c', '--cluster',
    #                     required=False,
    #                     action='store',
    #                     help='Name of Cluster')
    #
    # parser.add_argument('-v', '--vm',
    #                     required=False,
    #                     action='store',
    #                     help='Name of VM')
    #
    # parser.add_argument('-i', '--iso',
    #                     required=False,
    #                     action='store',
    #                     help='Path of iso (Absolute)')
    #
    # parser.add_argument('-j', '--uuid',
    #                     required=False,
    #                     action='store',
    #                     help='UUID of VM')
    #
    # parser.add_argument('-i', '--ip',
    #                     required=False,
    #                     action='store',
    #                     help='DNS IP of VM')

    return parser


def prompt_for_password(args):
    """
    if no password is specified on the command line, prompt for it
    """
    if not args.password:
        args.password = getpass.getpass(
            prompt='Enter password for host %s and user %s: ' %
                   (args.host, args.user))
    return args


def get_args():
    """
    Supports the command-line arguments needed to form a connection to vSphere.
    """
    parser = build_arg_parser()

    args = parser.parse_args()

    return prompt_for_password(args)


def prompt_y_n_question(question, default="no"):
    """ based on:
        http://code.activestate.com/recipes/577058/
    :param question: Question to ask
    :param default: No
    :return: True/False
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '{}'".format(default))

    while True:
        print(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please, respond with 'yes' or 'no' or 'y' or 'n'.")
