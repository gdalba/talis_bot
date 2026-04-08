import math
import re
import sys
import pymem

class SelfPointers:
    def __init__(self, info_pid):
        self.pm = pymem.Pymem()
        self.pm.open_process_from_id(pid)
        self.CLIENT = 0x00400000
        self.CHAR_NAME_POINTER = 



    def get_pointer(self, base_address, offsets):
        """
        Calcula o ponteiro final seguindo uma cadeia de offsets.
        """
        try:
            address = base_address
            for offset in offsets:  # Navega pelos offsets até o endereço final
                address = self.pm.read_int(address) + offset
            return address
        except Exception as e:
            #print(f"Erro ao calcular o ponteiro: {e}")
            return None

    def resolve_pointer_chain_vc(self, base_address, offsets):
        """
        Resolve chain using the same style as scanner vc:
        addr = read_int(base)
        for each offset except last: addr = read_int(addr + offset)
        final = addr + last_offset
        """
        try:
            if not offsets:
                return base_address

            addr = self.pm.read_int(base_address)
            for offset in offsets[:-1]:
                addr = self.pm.read_int(addr + offset)

            return addr + offsets[-1]
        except Exception:
            return None        


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python self_pointers.py <PID>")
        sys.exit(1)

    pid = int(sys.argv[1])
    sp = SelfPointers(pid)
    print(sp.CHAR_BASE_STATIC)