"""Generate appendix.xlsx with sheets Apx A1..A6 from presentation_deck.json."""
from pathlib import Path
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'goto-fsa-study' / 'src' / 'data'
PUBLIC = ROOT / 'goto-fsa-study' / 'public'

FILL_HDR = PatternFill('solid', fgColor='006B23')
FILL_ALT = PatternFill('solid', fgColor='F6F9F6')
FILL_WHITE = PatternFill('solid', fgColor='FFFFFF')

FONT_TITLE = Font(name='Calibri', size=13, bold=True, color='005419')
FONT_SEC = Font(name='Calibri', size=11, bold=True, color='006B23')
FONT_HDR = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
FONT_BODY = Font(name='Calibri', size=10, color='1F2937')
FONT_BOLD = Font(name='Calibri', size=10, bold=True, color='153B22')
FONT_NOTE = Font(name='Calibri', size=9, italic=True, color='5F7265')

THIN = Side(border_style='thin', color='DCE7DF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def write_table_block(ws, start_row, title, headers, rows, note=None):
    r = start_row
    ws.cell(r, 1, title).font = FONT_SEC
    r += 1

    if headers:
        for c_idx, h in enumerate(headers, start=1):
            cell = ws.cell(r, c_idx, h)
            cell.font = FONT_HDR
            cell.fill = FILL_HDR
            cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            cell.border = BORDER
        ws.row_dimensions[r].height = 22
        r += 1

    for idx, row in enumerate(rows):
        fill = FILL_WHITE if idx % 2 == 0 else FILL_ALT
        for c_idx, val in enumerate(row, start=1):
            cell = ws.cell(r, c_idx, val)
            cell.font = FONT_BOLD if c_idx == 1 else FONT_BODY
            cell.fill = fill
            cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            cell.border = BORDER
        r += 1

    if note:
        ws.cell(r, 1, note).font = FONT_NOTE
        r += 1

    return r + 1


def build_appendix_xlsx(json_path, out_path):
    deck = json.loads(json_path.read_text(encoding='utf-8'))
    apx_slides = [s for s in deck if s.get('is_appendix')]

    wb = Workbook()
    wb.properties.creator = 'Fagly Ramschie'
    wb.properties.lastModifiedBy = 'Fagly Ramschie'
    wb.properties.title = 'GoTo FSA Presentation Appendix Schedules (Apx A1–A6)'

    default_ws = wb.active

    for idx, s in enumerate(apx_slides, start=1):
        ws = wb.create_sheet(title=f'Apx A{idx}')
        ws.views.sheetView[0].showGridLines = True

        ws.cell(1, 1, s.get('display_title') or s.get('title', f'Appendix A{idx}')).font = FONT_TITLE
        ws.cell(2, 1, f"Author: Fagly Ramschie  |  Source: {s.get('source_footer', '')}").font = FONT_NOTE

        cur_row = 4
        if s.get('table'):
            tbl = s['table']
            cur_row = write_table_block(
                ws,
                cur_row,
                tbl.get('title', f'Appendix A{idx} Primary Schedule'),
                tbl.get('headers', []),
                tbl.get('rows', []),
                tbl.get('note'),
            )

        for sched in s.get('supporting_schedules', []):
            cur_row = write_table_block(
                ws,
                cur_row,
                sched.get('title', 'Supporting Schedule'),
                sched.get('headers', []),
                sched.get('rows', []),
                sched.get('note'),
            )

        if s.get('calculation_notes'):
            calc_headers = ['Metric', 'Result', 'Formula Used', 'Calculation', 'Source', 'Note']
            calc_rows = [
                [
                    c.get('label', ''),
                    c.get('result', ''),
                    c.get('formula', ''),
                    c.get('substitution', ''),
                    c.get('source', ''),
                    c.get('note', ''),
                ]
                for c in s['calculation_notes']
            ]
            cur_row = write_table_block(
                ws,
                cur_row,
                'Excel Workbook Calculations & Formula Audit',
                calc_headers,
                calc_rows,
            )

        for col in ws.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = 12
            for cell in col:
                if cell.row <= 2 or cell.value is None:
                    continue
                val_len = max((len(line) for line in str(cell.value).splitlines()), default=0)
                if val_len > max_len:
                    max_len = val_len
            ws.column_dimensions[col_letter].width = min(max_len + 4, 46)

    wb.remove(default_ws)
    wb.save(str(out_path))
    print(f'Generated {out_path} ({len(wb.sheetnames)} sheets: {", ".join(wb.sheetnames)})')


if __name__ == '__main__':
    build_appendix_xlsx(DATA / 'presentation_deck.json', PUBLIC / 'appendix.xlsx')
