import subprocess

from config import HOSTS


def run_command(host_name, command, timeout=30):
    """
    Ejecuta un comando en un host Linux remoto mediante SSH.

    Retorna:
        returncode
        stdout
        stderr
    """

    if host_name not in HOSTS:
        raise ValueError(
            f"Host desconocido: {host_name}"
        )

    host = HOSTS[host_name]

    target = f"{host['user']}@{host['ip']}"

    result = subprocess.run(
        [
            "ssh",
            target,
            command
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout
    )

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }