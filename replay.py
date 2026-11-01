"""Offline selected-table replay. Standard library only; no source data bundled."""
import argparse
import csv
import datetime
import hashlib
import json
import math
import posixpath
import re
import statistics
import sys
import zipfile
from decimal import Decimal
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def membership_digest(rows):
    text = json.dumps(sorted(rows), ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_book(path):
    """Bound archive sizes before reading XML; never extract or resolve links."""
    require(path.stat().st_size <= 32_000_000, 'Workbook compressed-size limit')
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        require(len(infos) <= 2000, 'Archive member-count limit')
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)), 'Duplicate archive member')
        require(sum(i.file_size for i in infos) <= 256_000_000, 'Archive expanded-size limit')
        for i in infos:
            name = i.filename
            require(not (name.startswith('/') or '\\' in name or ':' in name or '..' in PurePosixPath(name).parts), 'Unsafe archive path')
            require(not i.flag_bits & 1, 'Encrypted member')
            require(i.file_size <= 64_000_000 and i.file_size <= max(i.compress_size, 1) * 2000, 'Archive member-size/ratio limit')
        def xml(name):
            require(name in names, 'Missing OOXML member: ' + name)
            data = z.read(name)
            require(not re.search(br'<!\s*(DOCTYPE|ENTITY)', data, re.I), 'XML declarations forbidden')
            return ET.fromstring(data)
        strings = []
        if 'xl/sharedStrings.xml' in names:
            strings = [''.join(t.text or '' for t in si.findall('.//m:t', NS)) for si in xml('xl/sharedStrings.xml').findall('m:si', NS)]
        rels = {}
        for r in xml('xl/_rels/workbook.xml.rels'):
            if r.get('TargetMode') == 'External':
                continue
            target = r.get('Target', '')
            require('\\' not in target and ':' not in target, 'Unsafe relationship')
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            require(target.startswith('xl/') and '..' not in PurePosixPath(target).parts, 'Unsafe relationship target')
            rels[r.get('Id')] = target
        workbook = xml('xl/workbook.xml')
        properties = workbook.find('m:workbookPr', NS)
        date1904 = properties is not None and properties.get('date1904') in ('1', 'true')
        date_styles = set()
        if 'xl/styles.xml' in names:
            styles = xml('xl/styles.xml').find('m:cellXfs', NS)
            if styles is not None:
                date_styles = {i for i, style in enumerate(styles) if 14 <= int(style.get('numFmtId', '0')) <= 22}
        result = {}
        for sheet in workbook.findall('m:sheets/m:sheet', NS):
            rows = []
            for row in xml(rels[sheet.get(REL)]).findall('m:sheetData/m:row', NS):
                n = int(row.get('r'))
                require(1 <= n <= 200000, 'Row index limit')
                cells = {}
                for cell in row.findall('m:c', NS):
                    ref = cell.get('r', '')
                    require(re.fullmatch('[A-Z]{1,3}[1-9][0-9]*', ref) is not None, 'Invalid cell reference')
                    col = re.match('[A-Z]+', ref).group()
                    v = cell.find('m:v', NS)
                    value = None if v is None else v.text
                    typ = cell.get('t')
                    if typ == 's' and value is not None:
                        value = strings[int(value)]
                    elif typ == 'inlineStr':
                        value = ''.join(t.text or '' for t in cell.findall('.//m:t', NS))
                    elif value is not None and typ in (None, 'n') and int(cell.get('s', '0')) in date_styles:
                        serial = float(value)
                        days = int(serial)
                        if not date1904 and 0 < serial < 60:
                            days += 1
                        epoch = datetime.datetime(1904, 1, 1) if date1904 else datetime.datetime(1899, 12, 30)
                        value = str(epoch + datetime.timedelta(days=days, milliseconds=round((serial-int(serial))*86400000)))
                    cells[col] = value
                rows.append((n, cells))
            require(sheet.get('name') not in result, 'Duplicate sheet name')
            result[sheet.get('name')] = rows
        return result


def direction(z):
    return 'up' if z >= 1.5 else 'down' if z <= -1.5 else 'unchanged'


def analyze(study, book, expected):
    require(list(book) == list(expected['headers']), 'Unexpected worksheets/order')
    for name, headers in expected['headers'].items():
        rows = dict(book[name])
        for row, cells in headers.items():
            require(rows.get(int(row)) == cells, 'Header mismatch: ' + name)
    records, summary = [], {}
    if study == 'ad':
        groups = {'vehicle': set(), 'abeta': set()}
        anchors = {}
        for name, rows in book.items():
            treatment = 'vehicle' if 'control' in name else 'abeta'
            for row, c in rows:
                gene = c.get('A')
                if row == 1 or gene is None or not gene.strip():
                    continue
                groups[treatment].add(gene)
                anchors.setdefault(gene, []).append(f'{name}!A{row}')
        v, a = groups['vehicle'], groups['abeta']
        summary = dict(vehicle=len(v), abeta=len(a), vehicle_unique=len(v-a), abeta_unique=len(a-v), shared=len(v&a), union=len(v|a))
        records = [[g, 'shared' if g in v&a else 'vehicle_unique' if g in v else 'abeta_unique', ';'.join(anchors[g])] for g in sorted(v|a)]
        fields = ['gene', 'category', 'source_anchors']
    elif study == 'pd':
        fields = ['contrast', 'excel_row', 'id', 'geneSymbol', 'population_direction', 'source_direction']
        summary = {'contrasts': []}
        for contrast, (name, rows) in zip(['GS', 'GSDA', 'KO'], book.items()):
            data = [(n, c) for n, c in rows if n > 1]
            ds = [math.log2(float(c['F'])/float(c['H'])) - math.log2(float(c['E'])/float(c['G'])) for _, c in data]
            m, sp, ss = statistics.mean(ds), statistics.pstdev(ds), statistics.stdev(ds)
            max_delta = max(abs(d-float(c['L'])) for d, (_, c) in zip(ds, data))
            max_te = max(max(abs(math.log2(float(c['E'])/float(c['G']))-float(c['J'])), abs(math.log2(float(c['F'])/float(c['H']))-float(c['K']))) for _, c in data)
            max_z = max(abs((d-m)/ss-float(c['M'])) for d, (_, c) in zip(ds, data))
            require(max_delta < 1e-10 and max_te < 1e-10 and max_z < 1e-10, 'TE/delta/source ddof1 z mismatch')
            stats = dict(contrast=contrast, n=len(ds), mean=m, population_sd=sp, sample_sd=ss, population_up=sum((d-m)/sp >= 1.5 for d in ds), population_down=sum((d-m)/sp <= -1.5 for d in ds), source_up=sum(float(c['M']) >= 1.5 for _, c in data), source_down=sum(float(c['M']) <= -1.5 for _, c in data), max_delta_error=max_delta, max_TE_error=max_te, max_sample_z_error=max_z)
            summary['contrasts'].append(stats)
            records.extend([contrast, str(n), c['B'], c['C'], direction((d-m)/sp), direction(float(c['M']))] for d, (n, c) in zip(ds, data))
    else:
        fields = ['threshold', 'direction', 'excel_row', 'gene_id']
        data, panel = [], None
        for row, c in book['Table S1']:
            a = c.get('A') or ''
            if a.startswith('Supplementary Table S1A.'):
                panel = 'down'
            elif a.startswith('Supplementary Table S1B.'):
                panel = 'up'
            if not a.startswith('ENSG'):
                continue
            require(panel is not None, 'Unassigned source panel')
            q, effect = Decimal(c['D']), Decimal(c['E'])
            require(q.is_finite() and effect.is_finite() and (effect < 0 if panel == 'down' else effect > 0), 'Invalid source value/sign')
            data.append((row, a, panel, q))
        summary = {'rows': len(data), 'counts': {}}
        require(len({r[1] for r in data}) == len(data), 'Duplicate literal ID')
        for threshold in ['0.01', '0.05']:
            for panel in ['down', 'up']:
                chosen = [r for r in data if r[2] == panel and r[3] < Decimal(threshold)]
                summary['counts'][threshold + '_' + panel] = len(chosen)
                records.extend([threshold, panel, str(r[0]), r[1]] for r in chosen)
    return fields, records, summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study', required=True, choices=['ad', 'pd', 'pdac'])
    p.add_argument('--input', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    expected = json.loads(Path(__file__).with_name('expectations.json').read_text(encoding='utf-8'))[args.study]
    require(sha(args.input) == expected['input_sha256'], 'Input SHA256 mismatch')
    fields, records, summary = analyze(args.study, read_book(args.input), expected)
    digest = membership_digest(records)
    require(digest == expected['membership_sha256'], 'Membership/row-anchor mismatch')
    if args.study == 'pd':
        for actual, original in zip(summary['contrasts'], expected['counts']['contrasts']):
            for k, v in original.items():
                require(math.isclose(actual[k], v, rel_tol=1e-12, abs_tol=1e-12) if isinstance(v, float) else actual[k] == v, 'Count/statistic mismatch: ' + k)
    else:
        require(summary == expected['counts'], 'Count mismatch')
    args.output.mkdir(parents=True, exist_ok=True)
    require(args.output.resolve() != Path(__file__).resolve().parent, 'Use a separate output directory')
    with (args.output/'membership.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerows(records)
    report = dict(status='PASS', study=args.study, input_sha256=expected['input_sha256'], membership_sha256=digest, membership_records=len(records), summary=summary, scope='Selected-table arithmetic and membership replay only; not independent human or clinical validation')
    (args.output/'results.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, IndexError, zipfile.BadZipFile, ET.ParseError) as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        sys.exit(1)
