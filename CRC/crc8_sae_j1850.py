class CRC8_SAE_J1850:
    def __init__(self):
        self.polynomial = 0x1D
        self.initial = 0xFF
        self.final_xor = 0xFF
        self.width = 8
        self.ref_in = False
        self.ref_out = False
        self.mask = 0xFF
        self.table = self._generate_table()
    
    def _generate_table(self):
        table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 0x80:
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
            crc = self.table[crc ^ byte]
        
        return crc ^ self.final_xor
