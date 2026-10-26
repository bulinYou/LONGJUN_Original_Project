"""Generate a factual country-level map from Natural Earth geometry."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
polygons = json.loads((ROOT / 'site/world-polygons.json').read_text())
markets = json.loads((ROOT / 'site/markets.json').read_text())
selected = {m['iso'] for m in markets}
def point(lon, lat):
    return ((lon + 180) / 360 * 1000, (85-lat) / 150 * 430)
parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430" role="img" aria-labelledby="map-title map-desc"><title id="map-title">LONGJUN customer markets</title><desc id="map-desc">01 United States; 02 Germany; 03 Russia; 04 Ukraine; 05 Australia; 06 Japan; 07 South Korea; 08 India. China is the company’s home market. Markers represent countries, not customer office locations.</desc>']
for feature in polygons:
    if feature['iso'] == 'ATA': continue
    fill = '#70455e' if feature['iso'] in selected else '#e0d5db'
    if feature['iso'] == 'CHN': fill = '#2c9299'
    path = []
    for polygon in feature['polygons']:
        for ring in polygon:
            points = [point(*p) for p in ring]
            path.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in points)+'Z')
    parts.append(f'<path d="{" ".join(path)}" fill="{fill}" stroke="#fcfaf7" stroke-width=".5" fill-rule="evenodd"/>')
for market in markets:
    x,y = point(market['lon'],market['lat']);lx=x+market['labelDx'];ly=y+market['labelDy']
    parts.append(f'<g><path d="M{x:.1f},{y:.1f}L{lx:.1f},{ly:.1f}" stroke="#431c32" stroke-width="1.2"/><circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#fff" stroke="#431c32" stroke-width="1.5"/><circle cx="{lx:.1f}" cy="{ly:.1f}" r="14" fill="#431c32" stroke="#fcfaf7" stroke-width="1.5"/><text x="{lx:.1f}" y="{ly+5:.1f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="bold" fill="#fff">{market["number"]}</text></g>')
parts.append('</svg>')
(ROOT/'dist/assets/customer-markets.svg').write_text(''.join(parts))
print('Generated country map with 8 customer markets and China as company base.')
