from config import HOSTS


def place_nodes(nodes):
    """
    Distribuye los nodos entre los hosts disponibles
    mediante una política round-robin.

    Ejemplo:

    vm1 -> server1
    vm2 -> server2
    vm3 -> server3
    vm4 -> server1
    """

    host_names = list(HOSTS.keys())

    if not host_names:
        raise ValueError(
            "No existen hosts disponibles."
        )

    placement = {}

    for i, node in enumerate(nodes):
        host = host_names[i % len(host_names)]
        placement[node] = host

    return placement