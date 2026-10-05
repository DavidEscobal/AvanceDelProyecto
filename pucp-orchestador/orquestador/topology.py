def create_linear_topology(num_nodes):
    """
    Crea una topología lineal.

    Ejemplo para 4 nodos:

    vm1 -- vm2 -- vm3 -- vm4
    """

    if num_nodes < 2:
        raise ValueError(
            "Una topología lineal requiere al menos 2 nodos."
        )

    nodes = [
        f"vm{i}"
        for i in range(1, num_nodes + 1)
    ]

    links = []

    for i in range(num_nodes - 1):
        links.append(
            (nodes[i], nodes[i + 1])
        )

    return nodes, links


def create_ring_topology(num_nodes):
    """
    Crea una topología en anillo.

    Ejemplo para 4 nodos:

    vm1 -- vm2
    |       |
    vm4 -- vm3
    """

    if num_nodes < 3:
        raise ValueError(
            "Una topología en anillo requiere al menos 3 nodos."
        )

    nodes = [
        f"vm{i}"
        for i in range(1, num_nodes + 1)
    ]

    links = []

    for i in range(num_nodes - 1):
        links.append(
            (nodes[i], nodes[i + 1])
        )

    # Cerrar el anillo
    links.append(
        (nodes[-1], nodes[0])
    )

    return nodes, links