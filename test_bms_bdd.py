import pytest
from pytest_bdd import given, when, then, scenario, parsers
from bms import BMSCell

# --- SCENARIOS ---

@scenario('features/bms_safety.feature', 'Normal voltage is accepted')
def test_normal_voltage():
    pass

@scenario('features/bms_safety.feature', 'Overvoltage triggers fault')
def test_overvoltage():
    pass

@scenario('features/bms_safety.feature', 'High temperature triggers fault')
def test_high_temperature():
    pass

# --- FIXTURE compartido ---

@pytest.fixture
def bms_cell():
    return {'cell': None, 'error': None, 'result': None}

# --- STEPS ---

@given(parsers.parse('a BMS cell with voltage {voltage} and temperature {temperature}'))
def create_cell(bms_cell, voltage, temperature):
    bms_cell['cell'] = BMSCell(float(voltage), float(temperature))

@when('the safety check runs')
def run_safety_check(bms_cell):
    try:
        bms_cell['cell'].is_safe()
        bms_cell['result'] = 'PASS'
    except ValueError as e:
        bms_cell['result'] = 'FAIL'
        bms_cell['error'] = e

@then(parsers.parse('the result should be {expected}'))
def check_result(bms_cell, expected):
    assert bms_cell['result'] == expected

@then('a ValueError should be raised')
def check_error(bms_cell):
    assert bms_cell['error'] is not None