from tools import tasks


def power_off_vm(service_instance, vm):
    task = vm.PowerOffVM_Task()
    tasks.wait_for_tasks(service_instance, [task])
    return task


def power_on_vm(service_instance, vm):
    task = vm.PowerOnVM_Task()
    tasks.wait_for_tasks(service_instance, [task])
    return task
