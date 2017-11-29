from tools import tasks


def power_off_vm(service_instance, vm):
    """
    Power off the given vm
    :param service_instance: The root service instance object containing the VM
    :param vm: The vm to power off
    :return: The power off task
    """
    task = vm.PowerOffVM_Task()
    tasks.wait_for_tasks(service_instance, [task])
    return task


def power_on_vm(service_instance, vm):
    """
    Power on the given vm
    :param service_instance: The root service instance object containing the VM
    :param vm: The vm to power off
    :return: The power on task
    """
    task = vm.PowerOnVM_Task()
    tasks.wait_for_tasks(service_instance, [task])
    return task
