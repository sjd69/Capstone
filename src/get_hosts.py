from pyVim import connect
from pyVmomi import vim
from pyVmomi import vmodl
import atexit
# import tools.cli as cli
import ssl


def getHosts(content):
    host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)

    obj = [host for host in host_view.view]
    host_view.Destroy()
    return obj


def main():
    service_instance = connect.SmartConnectNoSSL(host='127.0.0.1', user='user', pwd='pass', port=8989)

    atexit.register(connect.Disconnect, service_instance)
    content = service_instance.RetrieveContent()

    hosts = getHosts(content)

    for host in hosts:
        print(host.name)


if __name__ == "__main__":
    main()
