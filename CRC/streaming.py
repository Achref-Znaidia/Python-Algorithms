class StreamingCRC:
    def __init__(self, crc_class, *args, **kwargs):
        self.crc_instance = crc_class(*args, **kwargs)
        self.crc_value = self.crc_instance.initial
    
    def update(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        for byte in data:
            if self.crc_instance.ref_in:
                byte = self.crc_instance._reflect(byte, 8)
            
            self.crc_value = (self.crc_value >> 8) ^ self.crc_instance.table[
                (self.crc_value ^ byte) & 0xFF
            ]
            self.crc_value &= self.crc_instance.mask
    
    def digest(self):
        crc = self.crc_value
        
        if self.crc_instance.ref_out:
            crc = self.crc_instance._reflect(crc, self.crc_instance.width)
        
        return crc ^ self.crc_instance.final_xor
    
    def reset(self):
        self.crc_value = self.crc_instance.initial
