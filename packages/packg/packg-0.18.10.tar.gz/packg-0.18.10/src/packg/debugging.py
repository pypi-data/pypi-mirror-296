import time
from typing import Optional

from attrs import define

from typedparser import add_argument


def connect_to_pycharm_debug_server(host: Optional[str] = None, port: Optional[int] = None) -> None:
    """
    Connect to a running pycharm debug server.

    To setup in PyCharm See Debug -> Edit Configurations -> Add New Configuration ->
        Python Debug Server -> Configure port, install packages, etc. -> Run

    Then run this function at the start of your code to connect it to the server.

    Args:
        host: host or None for skipping the connection process
        port: port or None for default port 12345
    """
    if host is None:
        return
    import pydevd_pycharm  # noqa  # pylint: disable=import-error

    if port is None:
        port = 12345
    while True:
        try:
            pydevd_pycharm.settrace(
                host, port=port, stdoutToServer=True, stderrToServer=True, suspend=False
            )
            break
        except ConnectionRefusedError:
            print(f"Debug server connection refused: {host}:{port}. Retrying...")
            time.sleep(2)

@define
class PyCharmDebugArgs:
    trace: str | None = add_argument(
        type=str, help="Connect debug server on this host.", default=None
    )
    trace_port: int = add_argument(type=int, default=33553, help="Target debugging server port")