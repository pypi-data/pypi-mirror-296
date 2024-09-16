import zlib
from itertools import cycle
from typing import Iterable

import win32clipboard
from qrcode import ERROR_CORRECT_L, QRCode

MAX_DATA_PER_QR: int = 2950
XOR_BITS: bytes = b'ScWqJwy5smUH279uBbDGRXZgkzhTY6xQLjpVF4vafKdN8AtenE'


def get_clipboard_path():
    win32clipboard.OpenClipboard()
    if not win32clipboard.EnumClipboardFormats(win32clipboard.CF_HDROP):
        raise RuntimeError('No files in clipboard')
    files = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
    if len(files) != 1:
        raise RuntimeError('Must be only one file in clipboard')
    win32clipboard.CloseClipboard()
    return files[0]


def read_data(path) -> bytes:
    with open(path, 'rb') as f:
        data = f.read()
    return data


def batched(buffer: bytes, batch_size: int) -> Iterable[bytes]:
    begin: int = 0
    end: int = begin + batch_size
    while begin < len(buffer):
        yield buffer[begin : end]
        begin += batch_size
        end += batch_size


def print_qrs(data: bytes):
    for qr_n, qr_data in enumerate(batched(data, MAX_DATA_PER_QR)):
        qr = QRCode(error_correction=ERROR_CORRECT_L)
        qr.add_data(data=qr_data, optimize=0)
        print(f'QR #{qr_n}, version: {qr.version}, size : {len(qr_data)}')
        # qr.print_ascii(invert=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img.save(f'qr_{qr_n}.jpg')


def xor_data(data: bytes) -> bytes:
    return bytes(a ^ b for (a, b) in zip(data, cycle(XOR_BITS)))


def compress_data(data: bytes) -> bytes:
    return zlib.compress(data, level=zlib.Z_BEST_COMPRESSION)


def main():
    path = get_clipboard_path()
    print(f'Processing file: {path}')

    raw_data = read_data(path)
    print(f'Size of raw data: {len(raw_data)}')

    compressed_data = compress_data(raw_data)
    print(f'Size of compressed data: {len(compressed_data)}')

    xored_data = xor_data(compressed_data)
    print_qrs(xored_data)


if __name__ == '__main__':
    main()
