class CRC32_C:
    def __init__(self):
        self.polynomial = 0x82F63B78
        self.initial = 0xFFFFFFFF
        self.final_xor = 0xFFFFFFFF
        self.width = 32
        self.ref_in = True
        self.ref_out = True
        self.mask = 0xFFFFFFFF
        self.table = self._generate_table()
    
    def _reflect(self, data, width):
        reflected = 0
        for i in range(width):
            if data & (1 << i):
                reflected |= 1 << (width - 1 - i)
        return reflected
    
    def _generate_table(self):
        table = []
        for i in range(256):
            crc = i
            if self.ref_in:
                crc = self._reflect(crc, 8)
            crc <<= (self.width - 8)
            for _ in range(8):
                if crc & (1 << (self.width - 1)):
                    crc = (crc << 1) ^ self.polynomial
                else:
                    crc <<= 1
                crc &= self.mask
            if self.ref_in:
                crc = self._reflect(crc, self.width)
            table.append(crc)
        return table
    
    def calculate(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        crc = self.initial
        for byte in data:
            if self.ref_in:
                byte = self._reflect(byte, 8)
            crc = (crc >> 8) ^ self.table[(crc ^ byte) & 0xFF]
        
        if self.ref_out:
            crc = self._reflect(crc, self.width)
        
        return crc ^ self.final_xor
