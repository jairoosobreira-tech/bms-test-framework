def parse_log(filepath):
    pass_count = 0
    fail_count = 0
    dtcs = []

    with open(filepath, 'r') as f:
        for line in f:
            if 'PASS' in line:
                pass_count += 1
            if 'FAIL' in line:
                fail_count += 1
            if 'DTC' in line:
                parts = line.strip().split(', ')
                timestamp = parts[0]
                dtc_code = parts[4].replace('DTC:', '')
                dtcs.append(f"{timestamp} — {dtc_code}")

    return {
        'pass': pass_count,
        'fail': fail_count,
        'pass_rate': round(pass_count / (pass_count + fail_count) * 100, 1),
        'dtcs': dtcs
    }

def write_report(results, output_file):
    with open(output_file, 'w') as f:
        f.write("=== REPORTE DE SESIÓN BMS ===\n")
        f.write(f"PASS: {results['pass']}\n")
        f.write(f"FAIL: {results['fail']}\n")
        f.write(f"Pass rate: {results['pass_rate']}%\n")
        f.write("\nDTCs activos:\n")
        for dtc in results['dtcs']:
            f.write(f"  {dtc}\n")

if __name__ == "__main__":
    results = parse_log('session_log.txt')
    write_report(results, 'report.txt')
    print("Reporte guardado en report.txt")