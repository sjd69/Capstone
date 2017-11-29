from pyVmomi import vim


def find_free_ide_controller(vm):
    """
    Look for a free IDE controller on a given VM
    :param vm: The VM to search
    :return: The free VM controller. None if there is not one available.
    """
    for controller in vm.config.hardware.device:
        if isinstance(controller, vim.vm.device.VirtualIDEController):

            # If there are less than 2 devices attached, we can use it.
            if len(controller.device) < 2:
                return controller

    return None
