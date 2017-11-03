from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
from pyVmomi import vmodl
import atexit
import subprocess
from tools import tasks
import tools.cli as cli


class Vcenter(object):
    def get_obj(self, type, name):
        obj = None
        container = self.content.viewManager.CreateContainerView(self.content.rootFolder, type, True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj

    def create_datacenter(self, name, folder=None):
        datacenter = self.get_obj([vim.Datacenter], name)
        if datacenter is not None:
            print("Datacenter %s already exists. Using existing datacenter." % name)
            return datacenter
        else:
            if len(name) > 79:
                raise ValueError("Datacenter name must be under 80 characters.")
            if folder is None:
                folder = self.service_instance.content.rootFolder
            if isinstance(folder, vim.Folder):
                print("Creating Datacenter %s" % name)
                datacenter = folder.CreateDatacenter(name=name)
        return datacenter

    def create_cluster(self, datacenter, name):
        cluster = self.get_obj([vim.ClusterComputeResource], name)
        if cluster is not None:
            print("Cluster %s already exists. Using existing cluster." % name)
            return cluster
        else:
            print("Creating cluster %s" % name)
            cluster_config = vim.cluster.ConfigSpecEx()

            host = datacenter.hostFolder
            cluster = host.CreateClusterEx(name=name, spec=cluster_config)
            return cluster

    def add_host(self, cluster, name, ssl_thumb, user, pwd):
        host = self.get_obj([vim.HostSystem], name)

        if host is not None:
            print("Host %s already exists. Using existing host.")
            return host
        else:
            cls = self.get_obj([vim.ClusterComputeResource], cluster)
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

    def get_ssl_thumbprint(self, ip):
        p1 = subprocess.Popen(('echo', '-n'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p2 = subprocess.Popen(('openssl', 's_client', '-connect', '{0}:443'.format(ip)), stdin=p1.stdout,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p3 = subprocess.Popen(('openssl', 'x509', '-noout', '-fingerprint', '-sha1'), stdin=p2.stdout,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = p3.stdout.read()
        ssl_thumbprint = out.decode().split('=')[-1].strip()
        return ssl_thumbprint

    def add_vm(self, name):

        template_vm = self.get_obj([vim.VirtualMachine], 'DC0_H0_VM0')
        config = vim.vm.ConfigSpec(numCPUs=1, memoryMB=512)

        adapter_map = vim.vm.customization.AdapterMapping()
        adapter_map.adapter = vim.vm.customization.IPSettings(ip=vim.vm.customization.DhcpIpGenerator(),
                                                              dnsDomain='domain.local')

        ip = vim.vm.customization.GlobalIPSettings()
        id = vim.vm.customization.LinuxPrep(domain='domain.local', hostName=vim.vm.customization.FixedName(name=name))
        spec = vim.vm.customization.Specification(nicSettingMap=[adapter_map], globalIPSettings=ip, identity=id)

        resource_pool = self.get_obj([vim.ResourcePool], 'DEV')
        relocate_spec = vim.vm.RelocateSpec(pool=resource_pool)
        cloned_spec = vim.vm.CloneSpec(powerOn=True, template=False,
                                       location=relocate_spec, customization=None, config=config)

        clone = template_vm.Clone(name=name, folder=template_vm.parent, spec=cloned_spec)

        print("Created VM %s" % name)
        return clone

    def find_free_ide_controller(self, vm):
        for dev in vm.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualIDEController):
                # If there are less than 2 devices attached, we can use it.
                if len(dev.device) < 2:
                    return dev
        return None

    def attach_iso(self, iso_path):
        testvm = self.get_obj([vim.VirtualMachine], 'testvm')

        connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        connectable.allowGuestControl = True
        connectable.startConnected = True

        cdrom = vim.vm.device.VirtualCdrom()
        cdrom.controllerKey = self.find_free_ide_controller(testvm).key
        cdrom.key = -1
        cdrom.connectable = connectable
        cdrom.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo(fileName=iso_path)
        op = vim.vm.device.VirtualDeviceSpec.Operation
        devSpec = vim.vm.device.VirtualDeviceSpec()
        devSpec.operation = op.add
        devSpec.device = cdrom




        print("Attaching iso to CD drive of %s" % testvm)
        cdspec = None


        vmconf = vim.vm.ConfigSpec()
        vmconf.deviceChange = [devSpec]
        print("Giving first priority for CDrom Device in boot order")
        vmconf.bootOptions = vim.vm.BootOptions(bootOrder=[vim.vm.BootOptions.BootableCdromDevice()])

        task = testvm.ReconfigVM_Task(vmconf)
        tasks.wait_for_tasks(self.service_instance, [task])

        print("Successfully changed boot order priority and attached iso to the CD drive of VM %s" % testvm)

        print("Power On the VM to boot from iso")
        testvm.PowerOnVM_Task()

    def vcenter_connect(self, args):
        self.service_instance = connect.SmartConnect(host=args.host,
                                                     user=args.user,
                                                     pwd=args.password,
                                                     port=int(args.port))
        if not self.service_instance:
            print("Could not connect to the specified host using specified "
                  "username and password")
            return -1
        self.content = self.service_instance.RetrieveContent()

        atexit.register(connect.Disconnect, self.service_instance)


def get_args():
    """
    Use the tools.cli methods and then add a few more arguments.
    """
    parser = cli.build_arg_parser()

    parser.add_argument('-d', '--datacenter',
                        required=True,
                        action='store',
                        help='Name of Datacenter to create VM in')

    parser.add_argument('-c', '--cluster',
                        required=True,
                        action='store',
                        help='Name of Cluster to create VM in')

    parser.add_argument('-v', '--vm',
                        required=True,
                        action='store',
                        help='Name of VM to create')

    parser.add_argument('-i', '--iso',
                        required=True,
                        action='store',
                        help='Path of iso (Absolute)')

    args = parser.parse_args()

    return cli.prompt_for_password(args)


def main():
    args = get_args()

    vc = Vcenter()
    vc.vcenter_connect(args)
    dc = vc.create_datacenter(args.datacenter)
    cls = vc.create_cluster(dc, args.cluster)

    ssl_thumbprint = vc.get_ssl_thumbprint(args.host)
    host = vc.add_host(args.cluster, args.host, ssl_thumbprint, args.user, args.password)

    vm_folder = dc.vmFolder
    hosts = dc.hostFolder.childEntity
    resource_pool = hosts[0].resourcePool

    vm = vc.add_vm(args.vm)
    vc.attach_iso(args.iso)
    return 0


# Start program
if __name__ == "__main__":
    main()
