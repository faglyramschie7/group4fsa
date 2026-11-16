"""Read-only regression checks: submitted assignments control the presentation data."""
import json
import math
from pathlib import Path
from statistics import median
from openpyxl import load_workbook
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'goto-fsa-study/src/data'
M2 = ROOT / 'ASSIGNMENTS/ASSIGNMENT 7/Group4_Milestone2_GOTO.xlsx'
M3 = ROOT / 'ASSIGNMENTS/ASSIGNMENT 10/outputs/milestone3/Group4_Milestone3_GOTO.xlsx'
M4 = ROOT / 'ASSIGNMENTS/ASSIGNMENT 13/Group4_Milestone4_GOTO.docx'
A14 = ROOT / 'ASSIGNMENTS/ASSSIGNMENT 14/Group4_FSA_Valuation_Workbook_GOTO.xlsx'
m2 = load_workbook(M2, data_only=True)
m3 = load_workbook(M3, data_only=True)
v = load_workbook(A14, data_only=False)
checks = 0

def check(condition, description):
    global checks
    assert condition, description
    checks += 1

check(math.isclose(m2['Ratio Analysis']['C36'].value, -4.72174991176924), 'Week 6 Z-score control')
check(round(m3['Calculations']['D12'].value * 100, 2) == -3.95, 'Milestone 3 accrual definition')
check(round(m3['Calculations']['D36'].value * 100, 2) == 25.97, 'Milestone 3 capex coverage')
check(m3['Calculations']['D37'].value == -875335, 'Milestone 3 FCF')
ke = .04502 + v['Cost of Capital']['B7'].value * (.0423 + .02465)
we = 26550.255 / (26550.255 + 7742.643)
wacc = we * ke + (1-we) * .0691 * .78
cf = [sum(v['DCF Valuation'][f'{c}{r}'].value for r in [6,9,10,11]) for c in 'BCD']
pvcf = sum(x / (1+wacc)**(i+1) for i,x in enumerate(cf))
pvtv = cf[-1] * 1.03 / (wacc-.03) / (1+wacc)**3
bve = 28711.657
ri = []
for c in 'BCD':
    ni = v['Residual Income Valuation'][f'{c}7'].value
    ri.append(ni-bve*ke)
    bve += ni
pvri = sum(x/(1+ke)**(i+1) for i,x in enumerate(ri))
pvrit = ri[-1]*1.03/(ke-.03)/(1+ke)**3
check(round((pvcf+pvtv+14012.522)/1062.0102,1) == -121.1, 'Assignment 14 DCF result')
check(round((28711.657+pvri+pvrit)/1062.0102,1) == -75.1, 'Assignment 14 RI result')
check(round(wacc*100,2) == 7.76, 'Assignment 14 WACC')
# Comparator revisions follow the latest explicit user instruction; other assignment outputs remain controls.
forecast = [[c.text for c in r.cells] for r in Document(M4).tables[3].rows]
for lang in ['en','id']:
    path = DATA / f"presentation_deck{'_id' if lang == 'id' else ''}.json"
    deck = json.loads(path.read_text())
    by_topic = {slide['topic_id']:slide for slide in deck}
    check(len(deck) == 12, f'{lang}: total slide count')
    check(all('speaker' not in slide for slide in deck), f'{lang}: no speaker allocation')
    check(all(not s['is_appendix'] for s in deck), f'{lang}: no appendix slides')
    check(sum(float(s['time_budget'].split()[0].replace(',','.')) for s in deck) == 20, f'{lang}: time budget')
    for slide in deck:
        check(len(slide['study_explanation']) > 120, f'{lang}: sidebar explanation for {slide["topic_id"]}')
        check(len(slide['analysis_points']) == 3, f'{lang}: explanation sequence for {slide["topic_id"]}')
        if slide['topic_id'] != 'decision':
            import re
            text = ' '.join([slide['title'],slide['study_explanation'],slide['speaker_notes']]+[p['text'] for p in slide['analysis_points']])
            check(not re.search(r'\bSELL\b|\bAVOID\b|JUAL / HINDARI',text,re.I), f'{lang}: recommendation not revealed on slide {slide["slide_num"]}')
    for slide in deck:
        check(bool(slide['assignment_evidence']), f'{lang}: source references for slide {slide["slide_num"]}')
        for source in slide['assignment_evidence']:
            check((ROOT/source['path']).is_file(), f'{lang}: source exists: {source["path"]}')
    check(math.isclose(by_topic['liquidity']['z_score_schedule']['result'],m2['Ratio Analysis']['C36'].value), f'{lang}: Z-score source match')
    peer = by_topic['relative']['peer_revision']
    check(peer['retained'] == ['GRAB'], f'{lang}: Grab is the sole comparable')
    check(set(peer['excluded']) == {'SE','BUKA','BELI'}, f'{lang}: exclusions recorded')
    check(peer['grab_price_usd'] == 4.99 and peer['price_date'] == '2025-12-31', f'{lang}: dated price')
    check(peer['grab_shares'] == 3969290878 + 128355800, f'{lang}: audited ordinary share count')
    expected_pb = 4.99 / (6728e6 / (3969290878 + 128355800))
    expected_bvps = 31805.025 / 1062.010200395
    check(math.isclose(peer['pb_multiple'], expected_pb), f'{lang}: P/B recomputation')
    check(math.isclose(peer['goto_normalized_bvps'], expected_bvps), f'{lang}: parent-equity normalization')
    check(math.isclose(peer['benchmark_value_per_share'],expected_pb*expected_bvps), f'{lang}: benchmark recomputation')
    check(peer['pe_used'] is False and peer['ev_ebitda_used'] is False, f'{lang}: invalid denominators excluded')
    check(len(by_topic['relative']['peer_exclusions_backup']) == 3, f'{lang}: sidebar exclusion reasons')
    check('blend_value_per_share' not in peer and 'median_pb' not in peer, f'{lang}: no invented peer median')
    check(by_topic['forecast_results']['table']['rows'][0][2:] == forecast[1][1:], f'{lang}: forecast revenue source match')
    table = str(by_topic['intrinsic']['supporting_schedules'])
    for number in [f'{-pvcf:,.1f}',f'{-pvtv:,.1f}',f'{-pvri:,.1f}',f'{-pvrit:,.1f}']:
        check(number in table, f'{lang}: valuation breakdown {number}')
    complete_forecast = by_topic['forecast_results']['supporting_schedules']
    check(len(complete_forecast) >= 3, f'{lang}: all three projected statements in sidebar')
    for idx, source_idx in enumerate([3,5,6]):
        source = [[c.text for c in r.cells] for r in Document(M4).tables[source_idx].rows]
        check([complete_forecast[idx]['headers']]+complete_forecast[idx]['rows'] == source, f'{lang}: linked projected statement {idx+1} matches submitted milestone')
    check(bool(by_topic['profitability'].get('loss_chart')), f'{lang}: financial analysis chart')
    check(len(by_topic['relative']['valuation_range']) == 3, f'{lang}: valuation comparison chart')
    for old in ['15,826.5','123,678.0','92,655.4','5,969.2','19,207','30,360','4,232','9,700','8,493']:
        check(old not in path.read_text(), f'{lang}: stale value {old}')
# Revised assignment files and study guides must reconcile to the same source inputs.
saved = load_workbook(A14, data_only=True)
check(math.isclose(saved['Market Multiples']['D19'].value, expected_pb*expected_bvps), 'Workbook cached Grab benchmark')
check(math.isclose(saved['Market Multiples']['B7'].value*1e6, 4097646678), 'Workbook audited Grab shares')
check(saved['Valuation Summary']['B10'].value is None, 'No simple average valuation target')
check(round(saved['Valuation Summary']['B5'].value,1) == -121.1, 'Saved DCF output retained')
check(round(saved['Valuation Summary']['B6'].value,1) == -75.1, 'Saved RI output retained')
for sheet in saved:
    check(not any(c.data_type == 'e' for row in sheet for c in row), f'No cached Excel errors: {sheet.title}')
for path in [ROOT/'ASSIGNMENTS/ASSSIGNMENT 14/Group4_Assignment14_Valuation_Summary.docx', ROOT/'ASSIGNMENTS/ASSSIGNMENT 15/Group4_FinalReport_GOTO.docx']:
    doc = Document(path)
    text = ' '.join([p.text for p in doc.paragraphs]+[c.text for t in doc.tables for row in t.rows for c in row.cells])
    check('Rp91.0' in text, f'{path.name}: revised benchmark')
    check('3.0391x' in text, f'{path.name}: source P/B')
    for old in ['-10.90','Rp 39.8','13.25x','2.30x']:
        check(old not in text, f'{path.name}: obsolete result removed: {old}')
    if 'FinalReport' in path.name:
        check('-4.721750' in text and 'X5' in text, 'Final report uses completed Week 6 model')

def generated_strings(value):
    if isinstance(value, dict):
        for key,item in value.items():
            if key not in ['raw_text','full_text','theory_explanation']:
                yield from generated_strings(item)
    elif isinstance(value, list):
        for item in value: yield from generated_strings(item)
    elif isinstance(value, str): yield value

for name in ['all_assignments_bundle.json','all_assignments_bundle_id.json','full_slides_knowledgebase.json','supporting_tables_id.json','structured_lectures.json','fsa_knowledgebase.json']:
    guide = json.loads((DATA/name).read_text())
    text = '\n'.join(generated_strings(guide))
    for old in ['-10.90','-10,90','-2.81','-11.29','Rp 39.8','Rp 39,8','13.25x','13,25x','2.30x','2,30x']:
        check(old not in text, f'{name}: superseded generated result {old}')
    check('91.0' in text or '91,0' in text or '91.015' in text, f'{name}: current Grab benchmark')
check('-2.81' not in (ROOT/'goto-fsa-study/src/App.vue').read_text(), 'Hover formulas do not use obsolete Z')
print(f'{checks} assignment and study-guide source checks passed (read-only).')
