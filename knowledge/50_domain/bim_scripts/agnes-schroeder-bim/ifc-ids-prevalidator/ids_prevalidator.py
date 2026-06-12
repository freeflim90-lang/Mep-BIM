#!/usr/bin/env python3
"""
Lightweight IFC/IDS pre-validator for BIM data quality checks.
This is NOT a full IDS-certified validator. It supports the subset used here:
- IfcDoor attributes: Name, Tag, OverallHeight, OverallWidth, OperationType
- IfcPropertySet / IfcPropertySingleValue checks
- required cardinality, simple enumerations, simple boolean applicability filters
"""
from __future__ import annotations
import re
import csv
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from lxml import etree

NS = {"ids": "http://standards.buildingsmart.org/IDS", "xs": "http://www.w3.org/2001/XMLSchema"}

ATTR_POS = {
    "GlobalId": 0,
    "Name": 2,
    "Description": 3,
    "ObjectType": 4,
    "Tag": 7,
    "OverallHeight": 8,
    "OverallWidth": 9,
    "PredefinedType": 10,
    "OperationType": 11,
}

@dataclass
class Requirement:
    kind: str  # attribute/property
    name: str
    pset: Optional[str]
    data_type: Optional[str]
    allowed: List[str]
    cardinality: str

@dataclass
class ApplicabilityFilter:
    kind: str
    name: str
    pset: Optional[str]
    expected: Optional[str]

@dataclass
class Specification:
    name: str
    entity: str
    filters: List[ApplicabilityFilter]
    reqs: List[Requirement]


def split_top_level(s: str) -> List[str]:
    parts, cur = [], []
    depth = 0
    in_str = False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "'":
            cur.append(ch)
            # STEP string quote escaping uses doubled single quote
            if in_str and i + 1 < len(s) and s[i+1] == "'":
                cur.append(s[i+1]); i += 2; continue
            in_str = not in_str
        elif not in_str:
            if ch == '(':
                depth += 1; cur.append(ch)
            elif ch == ')':
                depth -= 1; cur.append(ch)
            elif ch == ',' and depth == 0:
                parts.append(''.join(cur).strip()); cur = []
            else:
                cur.append(ch)
        else:
            cur.append(ch)
        i += 1
    parts.append(''.join(cur).strip())
    return parts


def unstep(v: str) -> str:
    v = v.strip()
    if v == '$' or v == '*': return ''
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1].replace("''", "'")
    if v.startswith('.') and v.endswith('.'):
        return v[1:-1]
    return v


def parse_measure(value: str) -> Tuple[Optional[str], Any]:
    value = value.strip()
    if value in ('$','*'):
        return None, None
    m = re.match(r"(IFC[A-Z0-9_]+)\((.*)\)$", value, flags=re.I)
    if m:
        typ = m.group(1).upper()
        raw = m.group(2).strip()
        if typ == 'IFCBOOLEAN':
            return typ, True if raw == '.T.' else False if raw == '.F.' else unstep(raw)
        if raw.startswith("'") and raw.endswith("'"):
            return typ, unstep(raw)
        try:
            return typ, float(raw)
        except Exception:
            return typ, unstep(raw)
    if value.startswith('.') and value.endswith('.'):
        return 'ENUM', value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return 'STRING', unstep(value)
    try:
        return 'NUMBER', float(value)
    except Exception:
        return None, unstep(value)


def parse_ifc(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding='utf-8', errors='ignore')
    records: Dict[str, Tuple[str, List[str]]] = {}
    # capture records across lines lazily until semicolon
    for m in re.finditer(r"#(\d+)\s*=\s*([A-Z0-9_]+)\s*\((.*?)\)\s*;", text, flags=re.I|re.S):
        rid, ent, args = '#' + m.group(1), m.group(2).upper(), m.group(3)
        records[rid] = (ent, split_top_level(args))
    doors = {}
    for rid,(ent,args) in records.items():
        if ent == 'IFCDOOR':
            door = {'id': rid, 'entity': ent, 'attributes': {}, 'psets': {}}
            for aname,pos in ATTR_POS.items():
                if pos < len(args):
                    typ,val = parse_measure(args[pos])
                    door['attributes'][aname] = {'type': typ, 'value': val, 'raw': args[pos]}
            doors[rid] = door
    # property single values
    props = {}
    for rid,(ent,args) in records.items():
        if ent == 'IFCPROPERTYSINGLEVALUE':
            pname = unstep(args[0]) if len(args)>0 else ''
            nom = args[2] if len(args)>2 else '$'
            typ,val = parse_measure(nom)
            props[rid] = {'name': pname, 'type': typ, 'value': val, 'raw': nom}
    # property sets
    psets = {}
    for rid,(ent,args) in records.items():
        if ent == 'IFCPROPERTYSET':
            psname = unstep(args[2]) if len(args)>2 else ''
            prop_refs = []
            if len(args)>4:
                blob=args[4].strip()
                if blob.startswith('(') and blob.endswith(')'):
                    prop_refs = [x.strip() for x in split_top_level(blob[1:-1])]
            psets[rid] = {'name': psname, 'props': {}}
            for pr in prop_refs:
                if pr in props:
                    psets[rid]['props'][props[pr]['name']] = props[pr]
    # attach psets to doors
    for rid,(ent,args) in records.items():
        if ent == 'IFCRELDEFINESBYPROPERTIES' and len(args) >= 6:
            related = args[4].strip()
            psref = args[5].strip()
            if psref not in psets: continue
            related_refs=[]
            if related.startswith('(') and related.endswith(')'):
                related_refs = [x.strip() for x in split_top_level(related[1:-1])]
            else:
                related_refs = [related]
            for dref in related_refs:
                if dref in doors:
                    doors[dref]['psets'][psets[psref]['name']] = psets[psref]['props']
    return {'records': records, 'doors': doors}


def get_text(node, xp: str) -> str:
    res = node.xpath(xp, namespaces=NS)
    if not res: return ''
    if isinstance(res[0], etree._Element):
        return ''.join(res[0].itertext()).strip()
    return str(res[0]).strip()


def allowed_values(node) -> List[str]:
    vals = []
    vals += [v.strip() for v in node.xpath('.//ids:value/ids:simpleValue/text()', namespaces=NS)]
    vals += [v for v in node.xpath('.//ids:value/xs:restriction/xs:enumeration/@value', namespaces=NS)]
    return vals


def parse_ids(path: Path) -> List[Specification]:
    tree = etree.parse(str(path))
    specs=[]
    for sp in tree.xpath('//ids:specification', namespaces=NS):
        name = sp.get('name') or ''
        ent = get_text(sp, './ids:applicability/ids:entity/ids:name/ids:simpleValue/text()') or 'IFCDOOR'
        filters=[]
        for prop in sp.xpath('./ids:applicability/ids:property', namespaces=NS):
            pset = get_text(prop, './ids:propertySet/ids:simpleValue/text()')
            bname = get_text(prop, './ids:baseName/ids:simpleValue/text()')
            vals = allowed_values(prop)
            expected = vals[0] if vals else None
            filters.append(ApplicabilityFilter('property', bname, pset, expected))
        reqs=[]
        for r in sp.xpath('./ids:requirements/*', namespaces=NS):
            local = etree.QName(r).localname
            if local == 'attribute':
                rname = get_text(r, './ids:name/ids:simpleValue/text()')
                reqs.append(Requirement('attribute', rname, None, r.get('dataType'), allowed_values(r), r.get('cardinality') or 'required'))
            elif local == 'property':
                pset = get_text(r, './ids:propertySet/ids:simpleValue/text()')
                bname = get_text(r, './ids:baseName/ids:simpleValue/text()')
                reqs.append(Requirement('property', bname, pset, r.get('dataType'), allowed_values(r), r.get('cardinality') or 'required'))
        specs.append(Specification(name, ent.upper(), filters, reqs))
    return specs


def normalize_for_compare(v):
    if isinstance(v, bool): return 'TRUE' if v else 'FALSE'
    return '' if v is None else str(v)


def get_prop(door, pset, name):
    return door['psets'].get(pset, {}).get(name)


def filter_applies(door, f: ApplicabilityFilter) -> bool:
    if f.kind == 'property':
        p = get_prop(door, f.pset, f.name)
        if not p: return False
        if f.expected is None: return True
        return normalize_for_compare(p['value']) == f.expected
    return True


def validate(ids_path: Path, ifc_path: Path):
    specs=parse_ids(ids_path)
    ifc=parse_ifc(ifc_path)
    rows=[]
    for sp in specs:
        if sp.entity != 'IFCDOOR':
            continue
        applicable=[]
        for dref,door in ifc['doors'].items():
            if all(filter_applies(door, f) for f in sp.filters):
                applicable.append((dref,door))
        for dref,door in applicable:
            door_name = normalize_for_compare(door['attributes'].get('Name',{}).get('value'))
            door_tag = normalize_for_compare(door['attributes'].get('Tag',{}).get('value'))
            for req in sp.reqs:
                status='PASS'; actual=''; message=''
                if req.kind == 'attribute':
                    a = door['attributes'].get(req.name)
                    if not a or a['value'] in (None,''):
                        status='FAIL'; message=f'Missing required attribute {req.name}'
                    else:
                        actual = normalize_for_compare(a['value'])
                        if req.allowed and actual not in req.allowed:
                            status='FAIL'; message=f'Value {actual!r} not in allowed list'
                elif req.kind == 'property':
                    p = get_prop(door, req.pset, req.name)
                    if not p or p['value'] in (None,''):
                        status='FAIL'; message=f'Missing required property {req.pset}.{req.name}'
                    else:
                        actual = normalize_for_compare(p['value'])
                        # simple type sanity
                        if req.data_type and p['type'] and req.data_type.upper()!=p['type'].upper():
                            # IFCLABEL vs IFCIDENTIFIER are both string-like, but keep as warning/fail? Use fail to expose exact mismatch.
                            status='FAIL'; message=f'Data type {p["type"]} does not match IDS {req.data_type}'
                        if status == 'PASS' and req.allowed and actual not in req.allowed:
                            status='FAIL'; message=f'Value {actual!r} not in allowed list'
                rows.append({
                    'ifc_file': ifc_path.name,
                    'spec': sp.name,
                    'door_id': dref,
                    'door_name': door_name,
                    'door_tag': door_tag,
                    'requirement': (req.pset + '.' if req.pset else '') + req.name,
                    'status': status,
                    'actual': actual,
                    'allowed': ';'.join(req.allowed),
                    'message': message,
                })
    return rows


def main():
    if len(sys.argv)<3:
        print('Usage: ids_prevalidator.py <ids-file> <ifc-file> [csv-out]')
        sys.exit(2)
    ids_path=Path(sys.argv[1]); ifc_path=Path(sys.argv[2])
    rows=validate(ids_path, ifc_path)
    total=len(rows); failed=sum(1 for r in rows if r['status']=='FAIL')
    print(f'IFC: {ifc_path.name}')
    print(f'IDS: {ids_path.name}')
    print(f'Requirement checks: {total}; PASS: {total-failed}; FAIL: {failed}')
    byspec={}
    for r in rows:
        if r['status']=='FAIL': byspec.setdefault(r['spec'],0); byspec[r['spec']]+=1
    if byspec:
        print('\nFailed specs:')
        for k,v in sorted(byspec.items()): print(f'- {k}: {v}')
        print('\nFirst 25 failures:')
        c=0
        for r in rows:
            if r['status']=='FAIL':
                print(f"- {r['door_name'] or r['door_id']} | {r['requirement']} | actual={r['actual']!r} | {r['message']}")
                c += 1
                if c>=25: break
    else:
        print('No failures.')
    if len(sys.argv)>=4:
        out=Path(sys.argv[3])
        with out.open('w', newline='', encoding='utf-8-sig') as f:
            w=csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['empty'])
            w.writeheader(); w.writerows(rows)
        print(f'CSV written: {out}')

if __name__ == '__main__':
    main()
