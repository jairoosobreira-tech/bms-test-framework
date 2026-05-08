import csv
import json


def decode_voltage(byte0, byte1):
    raw_value = (byte0 << 8) | byte1
    voltage = raw_value * 0.01
    return round(voltage, 2)


def decode_temperature(byte2):
    return byte2 - 40


def analyze_bms_session(filepath):
    results = []
    failures = []

    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:

            if row['arbitration_id'] != '0x300':
                continue

            byte0 = int(row['byte0'], 16)
            byte1 = int(row['byte1'], 16)
            byte2 = int(row['byte2'], 16)

            voltage = decode_voltage(byte0, byte1)
            temperature = decode_temperature(byte2)

            status = "PASS"
            issues = []

            if voltage < 2.5 or voltage > 4.2:
                status = "FAIL"
                issues.append(f"Voltage out of range: {voltage}V")

            if temperature < -10 or temperature > 45:
                status = "FAIL"
                issues.append(
                    f"Temperature out of range: {temperature}C"
                )

            message = {
                "timestamp": row['timestamp'],
                "voltage": voltage,
                "temperature": temperature,
                "status": status
            }

            results.append(message)

            if issues:
                failures.append({
                    "timestamp": row['timestamp'],
                    "issues": issues
                })

    total = len(results)
    passed = len([r for r in results if r['status'] == 'PASS'])
    failed = len([r for r in results if r['status'] == 'FAIL'])

    report = {
        "total_messages": total,
        "pass": passed,
        "fail": failed,
        "failures": failures
    }

    return report


def save_report(report, output_file):
    with open(output_file, 'w') as file:
        json.dump(report, file, indent=4)


if __name__ == "__main__":

    report = analyze_bms_session("data/can_session.csv")

    print(json.dumps(report, indent=4))

    save_report(report, "reports/bms_report.json")