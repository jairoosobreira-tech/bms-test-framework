from bms_parser import (
    decode_voltage,
    decode_temperature
)


def test_voltage_normal():

    voltage = decode_voltage(0x01, 0x72)

    assert voltage == 3.70


def test_voltage_overvoltage():

    voltage = decode_voltage(0x01, 0xA5)

    assert voltage > 4.2


def test_temperature_out_of_range():

    temperature = decode_temperature(0x69)

    assert temperature > 45