#!/usr/bin/env python3
"""Convertidor de XML de Event Viewer (exportados) a CSV.

Uso:
  python scripts/evtx_xml_to_csv.py -i "Data/Aplicacion 09112025.xml" -o "evtx_csv_output/Aplicacion.csv"
  python scripts/evtx_xml_to_csv.py -i Data/ -o evtx_csv_output/

Funcionalidad:
  - Soporta archivo único o directorio con archivos .xml
  - Maneja namespaces del XML del Visor de eventos
  - Usa parsing por streaming (iterparse) para archivos grandes
"""
import argparse
import csv
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict


def localname(tag):
    if tag is None:
        return ''
    return tag.split('}')[-1]


def extract_event_fields(event_elem):
    # Recolecta elementos por localname
    byname = defaultdict(list)
    for el in event_elem.iter():
        byname[localname(el.tag)].append(el)

    def first_text(name):
        lst = byname.get(name)
        if not lst:
            return ''
        return (lst[0].text or '').strip()

    provider = ''
    if byname.get('Provider'):
        provider = byname['Provider'][0].attrib.get('Name', '')

    eventid = first_text('EventID')
    level = first_text('Level')
    task = first_text('Task')
    keywords = first_text('Keywords')
    record_id = first_text('RecordId')

    time_created = ''
    if byname.get('TimeCreated'):
        time_created = byname['TimeCreated'][0].attrib.get('SystemTime', '')

    computer = first_text('Computer')

    # Agregar EventData: todas las etiquetas Data
    data_items = []
    if byname.get('Data'):
        for d in byname['Data']:
            name = d.attrib.get('Name')
            text = (d.text or '').strip()
            if name:
                data_items.append(f"{name}={text}")
            else:
                data_items.append(text)

    # Message: algunos XML contienen 'RenderingInfo'/'Message'
    message = ''
    if byname.get('Message'):
        message = (byname['Message'][0].text or '').strip()

    return {
        'TimeCreated': time_created,
        'ProviderName': provider,
        'EventID': eventid,
        'Level': level,
        'Task': task,
        'Keywords': keywords,
        'Computer': computer,
        'RecordId': record_id,
        'Message': message,
        'Data': ';'.join(data_items),
    }


def iter_events_from_file(path):
    # Iterparse para eventos 'Event' (namespace-agnóstico)
    for event, elem in ET.iterparse(path, events=("end",)):
        if localname(elem.tag) == 'Event':
            yield elem
            # liberar memoria
            elem.clear()


def process_file(infile, writer):
    try:
        count = 0
        for ev in iter_events_from_file(infile):
            row = extract_event_fields(ev)
            writer.writerow(row)
            count += 1
        return count
    except ET.ParseError as e:
        print(f"Error parseando {infile}: {e}", file=sys.stderr)
        return 0


def ensure_dir(p):
    if p and not os.path.exists(p):
        os.makedirs(p)


def main():
    parser = argparse.ArgumentParser(description='Convertir XML del Visor de eventos a CSV')
    parser.add_argument('-i', '--input', required=True, help='Archivo XML o directorio con XMLs')
    parser.add_argument('-o', '--output', required=True, help='Archivo CSV de salida o directorio destino')
    args = parser.parse_args()

    inputs = []
    if os.path.isdir(args.input):
        for name in os.listdir(args.input):
            if name.lower().endswith('.xml'):
                inputs.append(os.path.join(args.input, name))
    elif os.path.isfile(args.input):
        inputs.append(args.input)
    else:
        print('Entrada no encontrada', file=sys.stderr)
        sys.exit(2)

    # Si output es directorio, generar CSV por cada XML
    if os.path.isdir(args.output) or args.output.endswith(os.sep):
        ensure_dir(args.output)
        for infile in inputs:
            base = os.path.splitext(os.path.basename(infile))[0]
            outfile = os.path.join(args.output, base + '.csv')
            with open(outfile, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['TimeCreated', 'ProviderName', 'EventID', 'Level', 'Task', 'Keywords', 'Computer', 'RecordId', 'Message', 'Data']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                n = process_file(infile, writer)
            print(f'Procesado {infile} -> {outfile} ({n} eventos)')
    else:
        # output file: si hay varios inputs, los volcamos todos en un CSV único
        outdir = os.path.dirname(args.output)
        if outdir:
            ensure_dir(outdir)
        with open(args.output, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['TimeCreated', 'ProviderName', 'EventID', 'Level', 'Task', 'Keywords', 'Computer', 'RecordId', 'Message', 'Data']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            total = 0
            for infile in inputs:
                n = process_file(infile, writer)
                total += n
            print(f'Procesados {len(inputs)} archivos -> {args.output} ({total} eventos)')


if __name__ == '__main__':
    main()
