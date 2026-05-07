class BMSCell:
    def __init__(self, voltage, temperature):
        self.voltage = voltage
        self.temperature = temperature

    def is_safe(self):
        if not isinstance(self.voltage, (int, float)):
            raise TypeError("Voltaje debe ser numérico")
        
        if self.voltage > 4.2:
            raise ValueError(f"Sobrevoltaje detectado: {self.voltage}V (máx 4.2V)")
        
        if self.voltage < 2.5:
            raise ValueError(f"Bajo voltaje detectado: {self.voltage}V (mín 2.5V)")
        
        if self.temperature > 45:
            raise ValueError(f"Sobretemperatura: {self.temperature}°C (máx 45°C)")
        
        if self.temperature < -10:
            raise ValueError(f"Temperatura baja: {self.temperature}°C (mín -10°C)")
        
        return True
    
