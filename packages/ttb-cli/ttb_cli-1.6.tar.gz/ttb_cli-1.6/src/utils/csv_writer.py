import csv
import os
from datetime import datetime
from typing import List, Dict


def write_performance_metrics_to_csv(metrics: List[Dict], output_file_path: str):
    if not metrics:
        return

    fieldnames = ['url', 'iteration', 'test_time', 'ttfb', 'load_time', 'total_time', 'error']

    try:
        if os.path.exists(output_file_path):
            output_file_path = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{output_file_path}"

        with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for metric in metrics:
                writer.writerow(metric)

    except Exception as e:
        print(f"Failed to write metrics to CSV: {e}")


def write_lighthouse_reports_to_csv(reports: List[Dict], output_file_path: str):
    if not reports:
        return

    fieldnames = [
        'url', 'finalUrl', 'requestedUrl', 'performance', 'accessibility', 'best-practices', 'seo', 'pwa',
        'first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift',
        'speed-index', 'interactive', 'server-response-time', 'total-byte-weight', 'error'
    ]

    try:
        if os.path.exists(output_file_path):
            output_file_path = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{output_file_path}"

        with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for report in reports:
                audits = report.get('audits', {})
                row = {
                    'url': report.get('requestedUrl', 'N/A'),
                    'finalUrl': report.get('finalUrl', 'N/A'),
                    'requestedUrl': report.get('requestedUrl', 'N/A'),
                    'performance': int(report['categories']['performance']['score'] * 100) if 'performance' in report['categories'] else 'N/A',
                    'accessibility': int(report['categories']['accessibility']['score'] * 100) if 'accessibility' in report['categories'] else 'N/A',
                    'best-practices': int(report['categories']['best-practices']['score'] * 100) if 'best-practices' in report['categories'] else 'N/A',
                    'seo': int(report['categories']['seo']['score'] * 100) if 'seo' in report['categories'] else 'N/A',
                    'pwa': int(report['categories']['pwa']['score'] * 100) if 'pwa' in report['categories'] else 'N/A',
                    'first-contentful-paint': audits.get('first-contentful-paint', {}).get('numericValue', 'N/A'),
                    'largest-contentful-paint': audits.get('largest-contentful-paint', {}).get('numericValue', 'N/A'),
                    'total-blocking-time': audits.get('total-blocking-time', {}).get('numericValue', 'N/A'),
                    'cumulative-layout-shift': audits.get('cumulative-layout-shift', {}).get('numericValue', 'N/A'),
                    'speed-index': audits.get('speed-index', {}).get('numericValue', 'N/A'),
                    'interactive': audits.get('interactive', {}).get('numericValue', 'N/A'),
                    'server-response-time': audits.get('server-response-time', {}).get('numericValue', 'N/A'),
                    'total-byte-weight': audits.get('total-byte-weight', {}).get('numericValue', 'N/A'),
                    'error': report.get('error', 'N/A')
                }
                writer.writerow(row)

    except Exception as e:
        print(f"Failed to write Lighthouse reports to CSV: {e}")

