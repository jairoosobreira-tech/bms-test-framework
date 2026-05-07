import pytest
from log_parser import parse_log

def test_conteo_pass_fail(tmp_path):
    log = tmp_path / "test.txt"
    log.write_text(
        "2026-05-06 08:01:24, VOLTAGE, 3.7V, PASS\n"
        "2026-05-06 08:01:25, VOLTAGE, 4.5V, FAIL, DTC:P0A1B, ACTIVE\n"
        "2026-05-06 08:01:26, TEMP, 25C, PASS\n"
    )
    results = parse_log(str(log))
    assert results['pass'] == 2
    assert results['fail'] == 1

def test_pass_rate(tmp_path):
    log = tmp_path / "test.txt"
    log.write_text(
        "2026-05-06 08:01:24, VOLTAGE, 3.7V, PASS\n"
        "2026-05-06 08:01:25, VOLTAGE, 4.5V, FAIL, DTC:P0A1B, ACTIVE\n"
        "2026-05-06 08:01:26, TEMP, 25C, PASS\n"
        "2026-05-06 08:01:27, TEMP, 25C, PASS\n"
    )
    results = parse_log(str(log))
    assert results['pass_rate'] == 75.0

def test_dtcs_extraidos(tmp_path):
    log = tmp_path / "test.txt"
    log.write_text(
        "2026-05-06 08:01:25, VOLTAGE, 4.5V, FAIL, DTC:P0A1B, ACTIVE\n"
        "2026-05-06 08:01:28, TEMP, 60C, FAIL, DTC:P0A2C, ACTIVE\n"
    )
    results = parse_log(str(log))
    assert len(results['dtcs']) == 2

def test_sin_dtcs(tmp_path):
    log = tmp_path / "test.txt"
    log.write_text(
        "2026-05-06 08:01:24, VOLTAGE, 3.7V, PASS\n"
        "2026-05-06 08:01:26, TEMP, 25C, PASS\n"
    )
    results = parse_log(str(log))
    assert results['dtcs'] == []

def test_dtc_codigo_correcto(tmp_path):
    log = tmp_path / "test.txt"
    log.write_text(
        "2026-05-06 08:01:25, VOLTAGE, 4.5V, FAIL, DTC:P0A1B, ACTIVE\n"
    )
    results = parse_log(str(log))
    assert "P0A1B" in results['dtcs'][0]