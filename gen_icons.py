#!/usr/bin/env python3
"""Genera icon-192.png e icon-512.png para EmergSmart sin dependencias externas:
letra 'E' teal (#14b8a6) sobre fondo slate (#0f172a). PNG escrito con stdlib (zlib)."""
import os
import zlib
import struct

OUT = os.path.dirname(os.path.abspath(__file__))
BG = (15, 23, 42)      # #0f172a slate
FG = (20, 184, 166)    # #14b8a6 teal


def rects_E(S):
    """Rectángulos (x0,y0,x1,y1) que forman la letra E, escalados al tamaño S."""
    def s(f):
        return int(round(f * S))
    x0, x1 = s(0.32), s(0.44)          # grosor del tronco vertical
    top, bot = s(0.22), s(0.78)        # extensión vertical
    return [
        (x0, top, s(0.44), bot),        # tronco vertical
        (x0, top, s(0.70), s(0.34)),    # barra superior
        (x0, s(0.44), s(0.63), s(0.56)),# barra media
        (x0, s(0.66), s(0.70), bot),    # barra inferior
    ]


def in_rects(x, y, rects):
    for (a, b, c, d) in rects:
        if a <= x < c and b <= y < d:
            return True
    return False


def make(size):
    rects = rects_E(size)
    # buffer RGB, una fila = 1 byte de filtro + size*3 bytes
    raw = bytearray()
    for y in range(size):
        raw.append(0)  # filtro None
        for x in range(size):
            c = FG if in_rects(x, y, rects) else BG
            raw.extend(c)
    png = _png(size, size, bytes(raw))
    path = os.path.join(OUT, "icon-%d.png" % size)
    with open(path, "wb") as f:
        f.write(png)
    print("escrito", path, "(%d bytes)" % len(png))


def _chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data +
            struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))


def _png(w, h, raw):
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)  # 8-bit, RGB
    idat = zlib.compress(raw, 9)
    return sig + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b"")


if __name__ == "__main__":
    make(192)
    make(512)
