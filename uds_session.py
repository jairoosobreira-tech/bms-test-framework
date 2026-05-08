# Simular lectura de DIDs del BMS
# Como los que validabas en Stellantis

bms_dids = [
    {"did": 0xF190, "name": "VIN",              "mock_data": b"3VWFE21C04M000001"},
    {"did": 0xF18C, "name": "ECU Serial",        "mock_data": b"BMS2024001234"},
    {"did": 0x0201, "name": "Cell Voltage",      "mock_data": bytes([0x01, 0x72])},  # 370 = 3.70V
    {"did": 0x0202, "name": "Pack Temperature",  "mock_data": bytes([0x00, 0x41])},  # 65 - 40 = 25°C
    {"did": 0x0203, "name": "SOC",               "mock_data": bytes([0x4B])},         # 75%
]

print("=== SESIÓN DE DIAGNÓSTICO BMS ===\n")

for item in bms_dids:
    did_bytes = item["did"].to_bytes(2, 'big')
    
    # Request
    req = bytes([0x22]) + did_bytes
    
    # Response simulada de ECU
    resp = bytes([0x62]) + did_bytes + item["mock_data"]
    
    # Decodificar según DID
    raw_data = resp[3:]
    
    if item["did"] == 0x0201:
        value = f"{int.from_bytes(raw_data, 'big') / 100:.2f}V"
    elif item["did"] == 0x0202:
        value = f"{int.from_bytes(raw_data, 'big') - 40}°C"
    elif item["did"] == 0x0203:
        value = f"{raw_data[0]}%"
    else:
        value = raw_data.decode('ascii', errors='replace')
    
    print(f"DID 0x{item['did']:04X} | {item['name']:<18} | {value}")

print("\nSesión completada.")
