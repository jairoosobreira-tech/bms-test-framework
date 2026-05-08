import udsoncan
from udsoncan import Request, Response
from udsoncan.services import ReadDataByIdentifier

#Simular un request ReadDataByIdentifier (0x22)
#DID 0xF190 = VIN (Vehicle Identification Number)

#Request: 22 F1 90
request = Request(ReadDataByIdentifier, data = b'\xF1\x90')

#Simular response de ECU
#0x62 = PR from 0x22 SID
#F190 = DID
# !7 bytes from VIN value

vin = "3VWFE21C04M000001"
vin_bytes = vin.encode('ascii')

response_bytes = bytes([0x62,0xF1,0x90]) + vin_bytes
print(f"Response bytes: {response_bytes.hex().upper()}")

#Parsear el request y mostrar el VIN
did = response_bytes[1:3].hex().upper()
data = response_bytes[3:]

print(f"\nDID: 0x{did}")
print(f"VIN: {data.decode('ascii')}")
print(f"Longitud de VIN: {len(data)}")

#Validat formato VIN

if len(data) == 17 and all(c.isalnum() for c in data.decode('ascii')):
    print("VIN válido: PASS ")
else:
    print("VIN inválido: FAIL x")
    print(f"VIN recibido: {data.decode('ascii')}")

