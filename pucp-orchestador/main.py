import sys

from config import HOSTS

from orchestrator.topology import (
    create_linear_topology,
    create_ring_topology
)

from orchestrator.linux_driver import LinuxDriver


def create_placement(nodes):
    """
    Distribuye las VMs entre los hosts Linux disponibles
    utilizando una política round-robin.
    """

    host_names = list(HOSTS.keys())

    placement = {}

    for i, node in enumerate(nodes):
        host = host_names[i % len(host_names)]
        placement[node] = host

    return placement


def print_topology(
    topology_type,
    nodes,
    links
):
    print("\n=== TOPOLOGÍA ===")

    print(
        f"Tipo: {topology_type}"
    )

    print(
        f"Nodos: {nodes}"
    )

    print(
        f"Enlaces: {links}"
    )


def print_placement(placement):

    print("\n=== PLACEMENT ===")

    for node, host in placement.items():

        print(
            f"{node} -> {host}"
        )


def deploy_slice(
    topology_type,
    number_of_nodes
):
    """
    Genera la topología, realiza el placement
    y despliega las VMs en los hosts Linux.
    """

    # ---------------------------------------------
    # 1. Generar topología
    # ---------------------------------------------

    if topology_type == "linear":

        nodes, links = (
            create_linear_topology(
                number_of_nodes
            )
        )

    elif topology_type == "ring":

        nodes, links = (
            create_ring_topology(
                number_of_nodes
            )
        )

    else:

        raise ValueError(
            "Tipo de topología inválido. "
            "Use 'linear' o 'ring'."
        )

    print_topology(
        topology_type,
        nodes,
        links
    )

    # ---------------------------------------------
    # 2. Placement
    # ---------------------------------------------

    placement = create_placement(
        nodes
    )

    print_placement(
        placement
    )

    # ---------------------------------------------
    # 3. Crear drivers
    # ---------------------------------------------

    print("\n=== DEPLOYMENT ===")

    drivers = {}

    for host_name in HOSTS:

        drivers[host_name] = (
            LinuxDriver(host_name)
        )

    # ---------------------------------------------
    # 4. Crear VMs
    # ---------------------------------------------

    for index, node in enumerate(
        nodes,
        start=1
    ):

        host_name = placement[node]

        driver = drivers[host_name]

        vlan_id = 100

        # VNC único para cada VM
        vnc_port = 5910 + index

        print(
            f"\n[+] Desplegando {node} "
            f"en {host_name}"
        )

        # -----------------------------------------
        # Comprobar si la VM ya existe
        # -----------------------------------------

        result = driver.list_vms()

        if result["returncode"] != 0:

            print(
                f"[ERROR] No se pudo consultar "
                f"{host_name}"
            )

            continue

        if f"-name {node} " in result["stdout"]:

            print(
                f"[INFO] {node} ya existe en "
                f"{host_name}. Se omite."
            )

            continue

        # -----------------------------------------
        # Crear VM
        # -----------------------------------------

        result = driver.create_vm(
            node,
            "br-int",
            vlan_id,
            vnc_port
        )

        if result["returncode"] == 0:

            print(
                f"[OK] {node} creada en "
                f"{host_name}"
            )

        else:

            print(
                f"[ERROR] No se pudo crear "
                f"{node} en {host_name}"
            )

            if result["stderr"]:

                print(
                    result["stderr"]
                )

    # ---------------------------------------------
    # 5. Resumen
    # ---------------------------------------------

    print(
        "\n=== RESUMEN DEL SLICE ==="
    )

    print(
        f"Topología : {topology_type}"
    )

    print(
        f"Nodos     : {len(nodes)}"
    )

    print(
        f"Hosts     : {len(HOSTS)}"
    )

    print("\nPlacement:")

    for node, host in placement.items():

        print(
            f"  {node} -> {host}"
        )

    print("\nEnlaces lógicos:")

    for source, destination in links:

        print(
            f"  {source} <-> {destination}"
        )

    print(
        "\n[OK] Proceso de despliegue finalizado."
    )


def main():

    if len(sys.argv) != 3:

        print(
            "Uso:\n"
            "  python3 main.py linear <N>\n"
            "  python3 main.py ring <N>"
        )

        sys.exit(1)

    topology_type = sys.argv[1]

    try:

        number_of_nodes = int(
            sys.argv[2]
        )

    except ValueError:

        print(
            "[ERROR] N debe ser "
            "un número entero."
        )

        sys.exit(1)

    if number_of_nodes < 2:

        print(
            "[ERROR] Debe existir "
            "al menos 2 nodos."
        )

        sys.exit(1)

    deploy_slice(
        topology_type,
        number_of_nodes
    )


if __name__ == "__main__":
    main()