""" import json

#config de prueba cargada desde archivo

config = {
    "test_i": config["test_id"],
    "input_voltage": actual_voltage,
    "pass": config["Thresholds"]["min_v"] <= actual_voltage <= config["Thresholds"]["max_v"]
}

with open("report.json","w") as f:
    json.dump(result,f,indent=2)
return result """
import json
from bms import BMSCell

with open('test_config.json', 'r') as f:
    config = json.load(f)

results = []

for case in config['test_cases']:
    cell = BMSCell(voltage=case['voltage'], temperature=case['temperature'])
    
    try:
        cell.is_safe()
        actual = 'PASS'
    except ValueError:
        actual = 'FAIL'
    
    match = actual == case['expected']
    
    results.append({
        'id': case['id'],
        'expected': case['expected'],
        'actual': actual,
        'result': '✓ OK' if match else '✗ MISMATCH'
    })
    
    print(f"{case['id']}: {results[-1]['result']}")

passed = sum(1 for r in results if '✓' in r['result'])
total = len(results)

print(f"\nTotal: {passed}/{total} correctos")

with open('report.json', 'w') as f:
    json.dump({
        'suite': config['test_suite'],
        'passed': passed,
        'total': total,
        'pass_rate': round(passed / total * 100, 1),
        'results': results
    }, f, indent=2)

print("Reporte guardado en report.json")