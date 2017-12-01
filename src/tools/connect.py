import atexit

from pyVim import connect


def connect_with_ssl(host, user, pwd, port):
    """
    Connect to given host with SSL enabled and registers the disconnect with atexit.
    :param host: The host to connect to
    :param user: Username to login to server
    :param pwd: Password to login to server
    :param port: Port to access server (443 for vCenter server, 8989 for sim)
    :return: The service instance of that server. None if host does not exist.
    """
    service_instance = connect.SmartConnect(host=host,
                                            user=user,
                                            pwd=pwd,
                                            port=int(port))
    if not service_instance:
        print("Could not connect to the specified host")
        return None

    atexit.register(connect.Disconnect, service_instance)
    return service_instance


def connect_no_ssl(host, user, pwd, port):
    """
    Connect to given host with SSL disabled and registers the disconnect with atexit.
    :param host: The host to connect to
    :param user: Username to login to server
    :param pwd: Password to login to server
    :param port: Port to access server (443 for vCenter server, 8989 for sim)
    :return: The service instance of the server. None if host does not exist.
    """
    service_instance = connect.SmartConnectNoSSL(host=host,
                                                 user=user,
                                                 pwd=pwd,
                                                 port=int(port))
    if not service_instance:
        print("Could not connect to the specified host")
        return None

    atexit.register(connect.Disconnect, service_instance)
    return service_instance
