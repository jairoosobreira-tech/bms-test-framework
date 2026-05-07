import pytest
from bms import BMSCell

# --- CASOS QUE DEBEN PASAR ---

def test_voltaje_normal():
    celda = BMSCell(voltage=3.7, temperature=25)
    assert celda.is_safe() == True

def test_voltaje_limite_minimo():
    celda = BMSCell(voltage=2.5, temperature=25)
    assert celda.is_safe() == True

def test_voltaje_limite_maximo():
    celda = BMSCell(voltage=4.2, temperature=25)
    assert celda.is_safe() == True

def test_temperatura_normal():
    celda = BMSCell(voltage=3.7, temperature=0)
    assert celda.is_safe() == True

# --- CASOS QUE DEBEN LANZAR EXCEPCION ---

def test_sobrevoltaje():
    celda = BMSCell(voltage=5.1, temperature=25)
    with pytest.raises(ValueError) as info:
        celda.is_safe()
    assert "Sobrevoltaje" in str(info.value)

def test_bajo_voltaje():
    celda = BMSCell(voltage=1.9, temperature=25)
    with pytest.raises(ValueError) as info:
        celda.is_safe()
    assert "Bajo voltaje" in str(info.value)

def test_sobretemperatura():
    celda = BMSCell(voltage=3.7, temperature=60)
    with pytest.raises(ValueError) as info:
        celda.is_safe()
    assert "Sobretemperatura" in str(info.value)

def test_temperatura_baja():
    celda = BMSCell(voltage=3.7, temperature=-20)
    with pytest.raises(ValueError) as info:
        celda.is_safe()
    assert "Temperatura baja" in str(info.value)

def test_voltaje_no_numerico():
    celda = BMSCell(voltage="alto", temperature=25)
    with pytest.raises(TypeError):
        celda.is_safe()