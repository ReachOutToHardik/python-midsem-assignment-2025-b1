# attendance_analyzer.py
"""
Smart Attendance Analyzer (Offline)
- Menu-driven terminal app
- Stores attendance in data/attendance.csv
- Analyzes, deduplicates, plots results (PNG in data/)
Run: python attendance_analyzer.py
"""
import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt

DATA_DIR = 'data'
DATA_FILE = os.path.join(DATA_DIR, 'attendance.csv')
DATE_FORMAT = '%Y-%m-%d'

os.makedirs(DATA_DIR, exist_ok=True)

# Ensure file exists with header
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['student_id', 'student_name', 'date', 'status'])


def clean_row(row):
    """Normalize a CSV row dict: strip, uppercase status, validate date."""
    sid = str(row.get('student_id', '')).strip()
    name = row.get('student_name', '').strip()
    date_s = row.get('date', '').strip()
    status = str(row.get('status', '')).strip().upper()
    # normalize long words like 'PRESENT' -> 'P'
    if status and status not in ('P', 'A', 'L', 'H'):
        status = status[0] if status else ''
    # validate date
    try:
        d = datetime.strptime(date_s, DATE_FORMAT).date()
        date_s = d.isoformat()
    except Exception:
        raise ValueError(f'Invalid date: {date_s}')
    return {'student_id': sid, 'student_name': name, 'date': date_s, 'status': status}


def append_record(student_id, name, date_s, status):
    try:
        row = {'student_id': student_id, 'student_name': name, 'date': date_s, 'status': status}
        row = clean_row(row)
    except Exception as e:
        print('Error:', e)
        return
    # append
    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([row['student_id'], row['student_name'], row['date'], row['status']])
    print('Record added.')


def read_all_records():
    records = []
    with open(DATA_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                r = clean_row(r)
                records.append(r)
            except Exception as e:
                # skip invalid rows but inform user
                print('Skipping invalid row:', e)
    return records


def deduplicate_records(records):
    seen = set()
    out = []
    for r in records:
        key = (r['student_id'], r['date'])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def analyze(records, defaulter_threshold=75):
    # compute attendance stats
    records = deduplicate_records(records)
    students = defaultdict(lambda: {'name': '', 'present': 0, 'total': 0})
    daily = defaultdict(lambda: {'present': 0, 'total': 0})
    for r in records:
        sid = r['student_id']
        students[sid]['name'] = students[sid]['name'] or r['student_name']
        students[sid]['total'] += 1
        daily[r['date']]['total'] += 1
        if r['status'] == 'P':
            students[sid]['present'] += 1
            daily[r['date']]['present'] += 1
    # compute percentages
    result = []
    for sid, v in students.items():
        perc = (v['present'] / v['total'] * 100) if v['total'] else 0
        result.append({'student_id': sid, 'name': v['name'], 'present': v['present'], 'total': v['total'], 'percentage': round(perc, 2)})
    # defaulters
    defaulters = [r for r in result if r['percentage'] < defaulter_threshold]
    # daily rates
    daily_rates = []
    for date_s, v in sorted(daily.items()):
        rate = (v['present'] / v['total'] * 100) if v['total'] else 0
        daily_rates.append({'date': date_s, 'present': v['present'], 'total': v['total'], 'rate': round(rate, 2)})
    return {'students': result, 'defaulters': defaulters, 'daily_rates': daily_rates}


def save_cleaned(records):
    # overwrite cleaned unique records back to file
    records = deduplicate_records(records)
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['student_id', 'student_name', 'date', 'status'])
        for r in records:
            writer.writerow([r['student_id'], r['student_name'], r['date'], r['status']])
    print('Cleaned data saved to', DATA_FILE)


def plot_attendance_by_student(students, top_n=10):
    # students: list of dicts with percentage
    data = sorted(students, key=lambda x: x['percentage'], reverse=True)[:top_n]
    if not data:
        print('No student data to plot.')
        return
    names = [f"{x['name']} ({x['student_id']})" for x in data]
    vals = [x['percentage'] for x in data]
    plt.figure(figsize=(10, 6))
    plt.barh(names[::-1], vals[::-1])
    plt.xlabel('Attendance Percentage')
    plt.title(f'Top {len(vals)} Students by Attendance')
    plt.tight_layout()
    out = os.path.join(DATA_DIR, 'top_students.png')
    plt.savefig(out)
    plt.close()
    print('Saved', out)


def plot_daily_rate(daily_rates):
    if not daily_rates:
        print('No daily data to plot.')
        return
    dates = [x['date'] for x in daily_rates]
    rates = [x['rate'] for x in daily_rates]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, rates, marker='o')
    plt.xticks(rotation=45)
    plt.ylabel('Attendance Rate (%)')
    plt.title('Daily Attendance Rate')
    plt.tight_layout()
    out = os.path.join(DATA_DIR, 'daily_rate.png')
    plt.savefig(out)
    plt.close()
    print('Saved', out)


def generate_sample_data():
    """
    Helper: generate sample data for demo (uncomment call in __main__ if you want to use)
    Creates 10 students over 12 days with some random absences.
    """
    import random
    start = datetime.today().date() - timedelta(days=15)
    students = [(str(100 + i), f"Student_{i}") for i in range(1, 11)]
    rows = []
    for d in range(12):
        date_s = (start + timedelta(days=d)).isoformat()
        for sid, name in students:
            # random absence ~ 10-25%
            status = 'P' if random.random() > 0.15 else 'A'
            rows.append({'student_id': sid, 'student_name': name, 'date': date_s, 'status': status})
    # write to file (append)
    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for r in rows:
            writer.writerow([r['student_id'], r['student_name'], r['date'], r['status']])
    print(f'Generated {len(rows)} sample rows in {DATA_FILE}')


def menu():
    while True:
        print('\nSmart Attendance Analyzer')
        print('1. Add record')
        print('2. Analyze & Show Summary')
        print('3. Save cleaned data (deduplicate)')
        print('4. Generate sample data (demo)')
        print('5. Exit')
        c = input('Choose: ').strip()
        if c == '1':
            sid = input('Student ID: ').strip()
            name = input('Student Name: ').strip()
            date_s = input(f'Date ({DATE_FORMAT}): ').strip()
            status = input('Status (P/A/L/H): ').strip()
            append_record(sid, name, date_s, status)
        elif c == '2':
            records = read_all_records()
            res = analyze(records)
            print('\nAttendance Summary (Top 10):')
            students = sorted(res['students'], key=lambda x: x['percentage'], reverse=True)
            for s in students[:10]:
                print(f"{s['student_id']} - {s['name']}: {s['percentage']}% ({s['present']}/{s['total']})")
            print('\nDefaulters (<75%):')
            for d in res['defaulters']:
                print(f"{d['student_id']} - {d['name']}: {d['percentage']}%")
            plot_attendance_by_student(res['students'], top_n=10)
            plot_daily_rate(res['daily_rates'])
        elif c == '3':
            records = read_all_records()
            save_cleaned(records)
        elif c == '4':
            confirm = input('This will append sample rows to data/attendance.csv. Continue? (y/n): ').strip().lower()
            if confirm == 'y':
                generate_sample_data()
        elif c == '5':
            print('Bye')
            break
        else:
            print('Invalid choice')


if __name__ == '__main__':
    menu()
