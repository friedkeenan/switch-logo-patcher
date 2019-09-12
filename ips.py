import struct

class Patch:
    class Record:
        def __init__(self, offset, cont, rle_size=-1, ips32=True):
            if rle_size >= 0 and len(cont) != 1:
                raise ValueError("Invalid content for an RLE record")

            if (not ips32 and offset > 0xFFFFFF) or (ips32 and offset > 0xFFFFFFFF):
                    raise ValueError("Offset is too large for patch format")

            if rle_size > 0xFFFF: # If the RLE size can't fit in 16 bits
                raise ValueError("RLE size is too large")

            if rle_size < 0 and len(cont) > 0xFFFF: # If the size can't fit in 16 bits
                raise ValueError("Length of content is too large")

            self.offset = offset
            self.cont = cont
            self.rle_size = rle_size
            self.ips32 = ips32

        def __bytes__(self):
            buf = b""

            buf += struct.pack(">I", self.offset)
            if not self.ips32:
                buf = buf[1:]

            if self.rle_size >= 0:
                buf += struct.pack(">H", 0)
                buf += struct.pack(">H", self.rle_size)
            else:
                buf += struct.pack(">H", len(self.cont))

            buf += self.cont

            return buf

    def __init__(self, ips32=True):
        self.ips32 = ips32

        self.records = []

    @property
    def header(self):
        return b"IPS32" if self.ips32 else b"PATCH"

    @property
    def tail(self):
        return b"EEOF" if self.ips32 else b"EOF"

    def add_record(self, offset, cont, rle_size=-1):
        self.records.append(self.Record(offset, cont, rle_size, self.ips32))

    def __bytes__(self):
        buf = b""

        buf += self.header

        for r in self.records:
            buf += bytes(r)

        buf += self.tail

        return buf

    @classmethod
    def from_buffer(cls, buf):
        buf_off = 0

        header = struct.unpack_from("5s", buf)[0]
        buf_off += 5

        if header == b"IPS32":
            ips32 = True
        elif header == b"PATCH":
            ips32 = False
        else:
            raise ValueError("Invalid buffer for an IPS patch")

        p = cls(ips32)

        while True:
            tail = struct.unpack_from(f"{len(p.tail)}s", buf, buf_off)[0]
            if tail == p.tail:
                return p

            offset = struct.unpack_from("B" * len(p.tail), buf, buf_off)
            buf_off += len(p.tail)

            if ips32:
                offset = (offset[0] << 24) | (offset[1] << 16) | (offset[2] << 8) | (offset[3])
            else:
                offset = (offset[0] << 16) | (offset[1] << 8) | (offset[2])

            size = struct.unpack_from(">H", buf, buf_off)[0]
            buf_off += 2

            rle_size = -1
            if size == 0:
                rle_size, cont = struct.unpack_from(">Hc", buf, buf_off)
                buf_off += 3
            else:
                cont = struct.unpack_from(f"{size}s", buf, buf_off)[0]
                buf_off += size

            p.add_record(offset, cont, rle_size)

    @classmethod
    def gen_patch(cls, old_buf, new_buf):
        """
        Uh, don't use this until it's finished
        """

        return

        p = Patch(len(new_buf) > 0xFFFFFF) # Only make it IPS32 if an offset could not fit into 24 bits

        old_buf = old_buf[:len(new_buf)] # Truncate the old buffer to the length of the new buffer
        old_buf += b"\x00" * (len(new_buf) - len(old_buf)) # Add null bytes to the old buffer if the new buffer is larger than it

        for offset, (old, new) in enumerate(zip(old_buf, new_buf)):
            pass

        