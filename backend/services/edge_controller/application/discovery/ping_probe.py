import subprocess


def ping(ip: str, timeout_ms: int = 300) -> bool:
    try:
        subprocess.check_output(
            ["ping", "-n", "1", "-w", str(timeout_ms), ip],
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False
