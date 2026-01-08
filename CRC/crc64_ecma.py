class CRC64_ECMA:
    def __init__(self):
        self.polynomial = 0x42F0E1EBA9EA3693
        self.initial = 0x0000000000000000
        self.final_xor = 0x0000000000000000
        self.width = 64
        self.ref_in = False
        self.ref_out = False
        self.mask = 0xFFFFFFFFFFFFFFFF
        self.table = self._generate_table()
    
    def _generate_table(self):
        table = []
        for i in range(256):
            crc = i << (self.width - 8)
            for _ in range(8):
                if crc & (1 << (self.width - 1)):
                    crc = (crc << 1) ^ self.polynomial
                else:
                    crc <<= 1
                crc &= self.mask
            table.append(crc)
        return table
    
    def calculate(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        crc = self.initial
        for byte in data:
            crc = (crc << 8) ^ self.table[((crc >> (self.width - 8)) ^ byte) & 0xFF]
            crc &= self.mask
        
        return crc ^ self.final_xor
