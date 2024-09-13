import socket
import struct
from collections import deque
from collections.abc import Iterator
from logging import getLogger
from threading import Event
from time import gmtime, time

from dcspy import get_config_yaml_item
from dcspy.dcsbios import ProtocolParser
from dcspy.logitech import LogitechDevice
from dcspy.models import MULTICAST_IP, RECV_ADDR, LogitechDeviceModel
from dcspy.utils import check_bios_ver, get_version_string

LOG = getLogger(__name__)
LOOP_FLAG = True
__version__ = '3.5.2'


def _handle_connection(logi_device: LogitechDevice, parser: ProtocolParser, sock: socket.socket, ver_string: str, event: Event) -> None:
    """
    Handle the main loop where all the magic is happened.

    :param logi_device: Type of Logitech keyboard with LCD
    :param parser: DCS protocol parser
    :param sock: Multicast UDP socket
    :param ver_string: Current version to show
    :param event: Stop event for the main loop
    """
    start_time = time()
    LOG.info('Waiting for DCS connection...')
    support_banner = _supporters(text='Huge thanks to: Simon Leigh, Alexander Leschanz, Sireyn, Nick Thain, BrotherBloat and others! For support and help! ',
                                 width=26)
    while not event.is_set():
        try:
            dcs_bios_resp = sock.recv(2048)
            for int_byte in dcs_bios_resp:
                parser.process_byte(int_byte)
            start_time = time()
            _load_new_plane_if_detected(logi_device)
            logi_device.button_handle()
        except OSError as exp:
            _sock_err_handler(logi_device, start_time, ver_string, support_banner, exp)


def _load_new_plane_if_detected(logi_device: LogitechDevice) -> None:
    """
    Load instance when new plane detected.

    :param logi_device: Type of Logitech keyboard with LCD
    """
    global LOOP_FLAG
    if logi_device.plane_detected:
        logi_device.unload_old_plane()
        logi_device.load_new_plane()
        LOOP_FLAG = True


def _supporters(text: str, width: int) -> Iterator[str]:
    """
    Scroll text with widow width.

    :param text: Text to scroll
    :param width: Width of a window
    """
    queue = deque(text)
    while True:
        yield ''.join(queue)[:width]
        queue.rotate(-1)


def _sock_err_handler(logi_device: LogitechDevice, start_time: float, ver_string: str, support_iter: Iterator[str], exp: Exception) -> None:
    """
    Show basic data when DCS is disconnected.

    :param logi_device: Type of Logitech keyboard with LCD
    :param start_time: Time when connection to DCS was lost
    :param ver_string: Current version to show
    :param support_iter: Iterator for banner supporters
    :param exp: Caught exception instance
    """
    global LOOP_FLAG
    if LOOP_FLAG:
        LOG.debug(f'Main loop socket error: {exp}')
        LOOP_FLAG = False
    wait_time = gmtime(time() - start_time)
    logi_device.display = ['Logitech LCD OK',
                           f'No data from DCS:   {wait_time.tm_min:02d}:{wait_time.tm_sec:02d}',
                           f'{next(support_iter)}',
                           ver_string]


def _prepare_socket() -> socket.socket:
    """
    Prepare a multicast UDP socket for DCS-BIOS communication.

    :return: Socket object
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(RECV_ADDR)
    mreq = struct.pack('=4sl', socket.inet_aton(MULTICAST_IP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.settimeout(0.5)
    return sock


def dcspy_run(model: LogitechDeviceModel, event: Event) -> None:
    """
    Real starting point of DCSpy.

    :param model: Logitech device model
    :param event: stop event for the main loop
    """
    with _prepare_socket() as dcs_sock:
        parser = ProtocolParser()
        logi_dev = LogitechDevice(parser=parser, sock=dcs_sock, model=model)
        LOG.info(f'Loading: {str(logi_dev)}')
        LOG.debug(f'Loading: {repr(logi_dev)}')
        dcspy_ver = get_version_string(repo='emcek/dcspy', current_ver=__version__, check=bool(get_config_yaml_item('check_ver')))
        _handle_connection(logi_device=logi_dev, parser=parser, sock=dcs_sock, ver_string=dcspy_ver, event=event)
    LOG.info('DCSpy stopped.')
    logi_dev.display = ['DCSpy stopped', '', f'DCSpy: {dcspy_ver}', f'DCS-BIOS: {check_bios_ver(bios_path=get_config_yaml_item("dcsbios")).ver}']
