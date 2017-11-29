import atexit

from pyVim import connect


def connect_with_ssl(host, user, pwd, port):
    service_instance = connect.SmartConnect(host=host,
                                            user=user,
                                            pwd=pwd,
                                            port=int(port))
    if not service_instance:
        print("Could not connect to the specified host")
        return -1

    atexit.register(connect.Disconnect, service_instance)
    return service_instance


def connect_no_ssl(host, user, pwd, port):
    service_instance = connect.SmartConnectNoSSL(host=host,
                                                 user=user,
                                                 pwd=pwd,
                                                 port=int(port))
    if not service_instance:
        print("Could not connect to the specified host")
        return -1

    atexit.register(connect.Disconnect, service_instance)
    return service_instance
