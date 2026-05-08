import pytest

def simulate_did_response(did, mock_data):
    did_bytes = did.to_bytes(2, 'big')
    return bytes([0x62]) + did_bytes + mock_data

def decode_cell_voltage(response):
    raw = response[3:]
    return int.from_bytes(raw, 'big') / 100

def decode_temperature(response):
    raw = response[3:]
    return int.from_bytes(raw, 'big') - 40

def decode_soc(response):
    return response[3]

# --- TESTS ---

def test_cell_voltage_normal():
    resp = simulate_did_response(0x0201, bytes([0x01, 0x72]))  # 3.70V
    voltage = decode_cell_voltage(resp)
    assert 2.5 <= voltage <= 4.2
    assert voltage == 3.70

def test_cell_voltage_overvoltage():
    resp = simulate_did_response(0x0201, bytes([0x01, 0xA4]))  # 4.20V límite
    voltage = decode_cell_voltage(resp)
    assert voltage == 4.20

def test_temperature_normal():
    resp = simulate_did_response(0x0202, bytes([0x00, 0x41]))  # 25°C
    temp = decode_temperature(resp)
    assert -10 <= temp <= 45
    assert temp == 25

def test_temperature_over_limit():
    resp = simulate_did_response(0x0202, bytes([0x00, 0x69]))  # 65°C
    temp = decode_temperature(resp)
    assert temp > 45  # fuera de rango

def test_soc_normal():
    resp = simulate_did_response(0x0203, bytes([0x4B]))  # 75%
    soc = decode_soc(resp)
    assert 0 <= soc <= 100
    assert soc == 75

def test_vin_length():
    vin = b"3VWFE21C04M000001"
    resp = simulate_did_response(0xF190, vin)
    data = resp[3:]
    assert len(data) == 17

def test_vin_alphanumeric():
    vin = b"3VWFE21C04M000001"
    resp = simulate_did_response(0xF190, vin)
    data = resp[3:]
    assert data.isalnum()
