class CRC16_USB:
    def __init__(self):
        self.polynomial = 0x8005
        self.initial = 0xFFFF
        self.final_xor = 0xFFFF
        self.width = 16
        self.ref_in = True
        self.ref_out = True
        self.mask = 0xFFFF
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
            crc = self._reflect(i, 8)
            crc <<= (self.width - 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ self.polynomial
                else:
                    crc <<= 1
                crc &= self.mask
            crc = self._reflect(crc, self.width)
            table.append(crc)
        return table
    
    def calculate(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        crc = self.initial
        for byte in data:
            byte_reflected = self._reflect(byte, 8)
            crc = (crc >> 8) ^ self.table[(crc ^ byte_reflected) & 0xFF]
        
        return crc ^ self.final_xor
