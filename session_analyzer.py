from collections import Counter
from datetime import datetime
import json

def analyze_session(filepath):
    results = []
    dtcs = []
    session_id = None

    with open(filepath, 'r') as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(',')]

            if 'SESSION_START' in line:
                session_id = parts[2]

            if parts[2] == 'TEST' if len(parts) > 2 else False:
                pass

            if len(parts) >= 5 and parts[2] not in ('SESSION_START', 'SESSION_END'):
                timestamp = parts[0]
                tc_id     = parts[2]
                test_name = parts[3]
                status    = parts[4]

                results.append({
                    'timestamp': timestamp,
                    'tc_id':     tc_id,
                    'test_name': test_name,
                    'status':    status
                })

                if 'DTC' in line:
                    dtc_code = parts[5].replace('DTC:', '')
                    dtcs.append({'tc_id': tc_id, 'dtc': dtc_code})

    counts = Counter(r['status'] for r in results)
    total  = len(results)

    return {
        'session_id': session_id,
        'total':      total,
        'passed':     counts['PASS'],
        'failed':     counts['FAIL'],
        'pass_rate':  round(counts['PASS'] / total * 100, 1) if total else 0,
        'dtcs':       dtcs,
        'results':    results
    }

def print_report(data):
    print(f"\n{'='*50}")
    print(f"SESSION: {data['session_id']}")
    print(f"{'='*50}")
    print(f"Total tests : {data['total']}")
    print(f"Passed      : {data['passed']}")
    print(f"Failed      : {data['failed']}")
    print(f"Pass rate   : {data['pass_rate']}%")

    if data['dtcs']:
        print(f"\nDTCs activos ({len(data['dtcs'])}):")
        for d in data['dtcs']:
            print(f"  {d['tc_id']} → {d['dtc']}")

    print(f"\nFailed tests:")
    for r in data['results']:
        if r['status'] == 'FAIL':
            print(f"  {r['tc_id']} — {r['test_name']}")

def save_report(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\nReporte guardado en {output_path}")

if __name__ == "__main__":
    data = analyze_session('data/full_session.log')
    print_report(data)
    save_report(data, 'reports/session_report.json')
