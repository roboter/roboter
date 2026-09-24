import urllib.request
import json
import re
import os

FALLBACK_DESCRIPTIONS = {
    'ArduinoClock': 'Arduino digital clock using 4-digit 7-segment LED display',
    'BarcodeFileSearch': 'Search and organize files using barcode scanner input in C#',
    'CircuitFlow': 'Lightweight, high-performance web PCB & circuit design tool',
    'CircuitFlowAi': 'AI-assisted PCB design and schematic routing platform',
    'DinamiclyExecuteCode.NET': 'Dynamically compile and execute C# code at runtime with UI',
    'gotstl.web': 'Web-based 3D STL file viewer and renderer in JavaScript',
    'Lunokhod': 'Arduino robotics project inspired by the Lunokhod rover',
    'MSX': 'MSX microcomputer tools and emulator project in C#',
    'NodePCB': 'Interactive node-based PCB layout and schematic editor prototype',
    'QuadratureEcnoderCNC': 'Quadrature encoder decoding firmware for CNC systems',
    'roboter': 'Personal GitHub profile README and showcase repository',
    'USB_Device_List': 'C# utility to enumerate and inspect connected USB devices',
}

def fill_descriptions():
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, 'repos_data.json')

    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found. Run 3_find_screenshots.py first.")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        repos = json.load(f)

    print("Enriching repository descriptions...")

    for r in repos:
        name = r['name']
        desc = r.get('description') or ''

        if name in FALLBACK_DESCRIPTIONS:
            r['description'] = FALLBACK_DESCRIPTIONS[name]
        elif not desc or desc.strip() in ['', 'None'] or len(desc) < 5:
            r['description'] = f"{name} repository"

    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(repos, f, indent=2)

    print("Descriptions enriched successfully.")

if __name__ == '__main__':
    fill_descriptions()
