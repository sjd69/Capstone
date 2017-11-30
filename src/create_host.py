# hello
from pyVmomi import vim

from tools import cli as cli
from tools.connect import connect_no_ssl
from tools.get_obj import get_obj


def get_args():
    parser = cli.build_arg_parser()

    parser.add_argument('c', '--cluster',
                        required=True,
                        action='store',
                        help='name of cluster')


def get_ssl_thumbprint(ip):
    p1 = subprocess.Popen(('echo', '-n'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p2 = subprocess.Popen(('openssl', 's_client', '-connect', '{0}:443'.format(ip)), stdin=p1.stdout,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p3 = subprocess.Popen(('openssl', 'x509', '-noout', '-fingerprint', '-sha1'), stdin=p2.stdout,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out = p3.stdout.read()
    ssl_thumbprint = out.decode().split('=')[-1].strip()
    return ssl_thumbprint


def add_host(service_instance, cluster, name, ssl_thumb, user, pwd):
    host = get_obj([vim.HostSystem], name)

    if host is not None:
        print("Host %s already exists. Using existing host." % host)
        return host
    else:
        cls = get_obj([vim.ClusterComputeResource], cluster)
        if cls is None:
            error = 'Error - Cluster %s not found. Unable to add host %s' % (cluster, name)
            raise ValueError(error)

        try:
            host_config = vim.host.ConnectSpec(hostName=name, userName=user, sslThumbprint=ssl_thumb, password=pwd,
                                               force=True)
            task = cls.AddHost(spec=host_config, asConnected=True)

        except vmodl.MethodFault as error:
            print("Caught vmodl fault: %s" % error.msg)
            return -1
        tasks.wait_for_tasks(self.service_instance, [task])
        host = self.get_obj([vim.HostSystem], name)
        return host


def main():
    args = get_args()
    service_instance = connect_no_ssl(host=args.server,
                                      user=args.user,
                                      pwd=args.password,
                                      port=int(args.port))

    ssl_thumbprint = get_ssl_thumbprint(args.host)

    host = add_host(args.cluster, args.host, ssl_thumbprint, args.user, args.password)

    if host is None:
        error = 'Could not properly create host. Exiting...'
        raise ValueError(error)
        return 0
    else:
        return 1
