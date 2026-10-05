from orchestrator.ssh import run_command


class LinuxDriver:

    def __init__(self, host_name):
        self.host_name = host_name

    def run(self, command):
        """
        Ejecuta un comando Linux en el host remoto.
        """
        return run_command(
            self.host_name,
            command
        )

    def hostname(self):
        """
        Obtiene el hostname del servidor.
        """
        return self.run("hostname")

    def create_vm(
        self,
        vm_name,
        ovs_name,
        vlan_id,
        vnc_port
    ):
        """
        Crea una VM utilizando el script
        create_vm.sh del worker.
        """

        command = (
            "sudo bash ~/LAB4/scripts/create_vm.sh "
            f"{vm_name} "
            f"{ovs_name} "
            f"{vlan_id} "
            f"{vnc_port}"
        )

        return self.run(command)

    def delete_vm(
        self,
        vm_name,
        ovs_name,
        vlan_id,
        vnc_port
    ):
        """
        Elimina una VM utilizando delete_vm.sh.
        """

        command = (
            "sudo bash ~/LAB4/scripts/delete_vm.sh "
            f"{vm_name} "
            f"{ovs_name} "
            f"{vlan_id} "
            f"{vnc_port}"
        )

        return self.run(command)

    def list_vms(self):
        """
        Lista los procesos QEMU/KVM
        que están ejecutándose.
        """

        command = (
            "ps -ef | "
            "grep qemu-system-x86_64 | "
            "grep -v grep || true"
        )

        return self.run(command)

    def list_interfaces(self):
        """
        Lista las interfaces de red
        del host Linux.
        """

        return self.run(
            "ip -br link"
        )

    def create_network(
        self,
        vlan_id,
        network_cidr,
        dhcp="disabled",
        dhcp_range=None
    ):
        """
        Crea una red VLAN mediante
        create_network_vlan.sh.
        """

        if dhcp == "enabled":

            if dhcp_range is None:
                raise ValueError(
                    "dhcp_range es obligatorio "
                    "cuando DHCP está habilitado"
                )

            command = (
                "sudo bash "
                "~/LAB4/scripts/create_network_vlan.sh "
                f"{vlan_id} "
                f"{network_cidr} "
                "enabled "
                f"{dhcp_range}"
            )

        else:

            command = (
                "sudo bash "
                "~/LAB4/scripts/create_network_vlan.sh "
                f"{vlan_id} "
                f"{network_cidr} "
                "disabled"
            )

        return self.run(command)