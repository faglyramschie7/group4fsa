"""Build editable PowerPoint slides using the web deck's green 16:9 layout.

The JSON used by FinancialSlide.vue remains the content source. Pillow previews
use the same measured lines and geometry as the editable PowerPoint shapes.
"""
from pathlib import Path
import json
import math
from copy import deepcopy
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'goto-fsa-study/src/data'
PUBLIC = ROOT / 'goto-fsa-study/public'
PREVIEW = ROOT / 'outputs/presentation-preview'
W, H = 1280, 720
SCALE = 914400 / 96
WHITE, DARK, BODY = '#ffffff', '#173d25', '#253d2d'
GREEN, PALE, RULE, MUTED = '#008c2c', '#edf6ef', '#dce8df', '#63786a'
FONT_DIR = Path('/System/Library/Fonts/Supplemental')


def emu(px): return round(px * SCALE)
def rgb(color): return RGBColor.from_string(color.lstrip('#'))
def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ('Arial Bold.ttf' if bold else 'Arial.ttf')), round(size * 2))


def measure(text, size, bold=False):
    return font(size, bold).getlength(str(text)) / 2


def lines_for(text, width, size, bold=False):
    lines = []
    for para in str(text).split('\n'):
        words = para.split()
        line = ''
        for word in words:
            candidate = f'{line} {word}'.strip()
            if line and measure(candidate, size, bold) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines


class Canvas:
    gradient_preview = None
    def __init__(self, prs):
        self.slide = prs.slides.add_slide(prs.slide_layouts[6])
        # Native, editable DrawingML gradient matching FinancialSlide.vue.
        fill = self.slide.background.fill
        fill.solid()
        fill.fore_color.rgb = rgb('#005419')
        bgpr = self.slide.background._cSld.bg.bgPr
        for node in list(bgpr): bgpr.remove(node)
        grad = OxmlElement('a:gradFill')
        stops = OxmlElement('a:gsLst')
        for pos, color in [('0', '007222'), ('100000', '005419')]:
            stop = OxmlElement('a:gs'); stop.set('pos', pos)
            c = OxmlElement('a:srgbClr'); c.set('val', color); stop.append(c); stops.append(stop)
        grad.append(stops)
        lin = OxmlElement('a:lin'); lin.set('ang', '2700000'); lin.set('scaled', '1'); grad.append(lin)
        bgpr.append(grad)
        if Canvas.gradient_preview is None:
            image = Image.new('RGB', (W*2,H*2))
            pixels=image.load()
            for yy in range(H*2):
                for xx in range(W*2):
                    t=(xx/2+yy/2)/(W+H)
                    pixels[xx,yy]=(0,round(114-30*t),round(34-9*t))
            Canvas.gradient_preview=image
        self.img=Canvas.gradient_preview.copy()
        self.draw = ImageDraw.Draw(self.img)

    def rect(self, x,y,w,h,color,stroke=None):
        sh = self.slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, emu(x),emu(y),emu(w),emu(h))
        sh.fill.solid(); sh.fill.fore_color.rgb=rgb(color)
        if stroke: sh.line.color.rgb=rgb(stroke); sh.line.width=Pt(.5)
        else: sh.line.fill.background()
        self.draw.rectangle((x*2,y*2,(x+w)*2,(y+h)*2),fill=color,outline=stroke,width=1)
        return sh

    def rule(self,x,y,w,color=RULE): self.rect(x,y,w,.65,color)

    def text(self, text,x,y,w,h,size=14,color=BODY,bold=False,align='left',min_size=None):
        if not text: return 0
        minimum = min_size or size
        while True:
            lines = lines_for(text,w,size,bold)
            leading=size*1.45
            if (len(lines)-1)*leading+size*1.1 <= h+.1 or size<=minimum: break
            size-=.5
        if (len(lines)-1)*leading+size*1.1>h+2:
            raise ValueError(f'Text overflow at ({x},{y}): {str(text)[:90]} ({len(lines)*leading:.1f}>{h})')
        for i,line in enumerate(lines):
            xx=x
            linew=measure(line,size,bold)
            if align=='right': xx=x+w-linew
            elif align=='center': xx=x+(w-linew)/2
            shape=self.slide.shapes.add_textbox(emu(xx),emu(y+i*leading),emu(max(linew+8,w if align=='left' else linew+8)),emu(leading+3))
            tf=shape.text_frame;tf.word_wrap=False
            tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
            p=tf.paragraphs[0];p.text=line;p.font.name='Arial';p.font.size=Pt(size*.75);p.font.bold=bold;p.font.color.rgb=rgb(color)
            p.space_before=p.space_after=Pt(0)
            self.draw.text((xx*2,(y+i*leading)*2),line,font=font(size,bold),fill=color,anchor='lt')
        return len(lines)*leading

    def picture(self,path,x,y,w,h):
        path=PUBLIC/str(path).lstrip('/')
        if not path.is_file(): return
        im=Image.open(path).convert('RGBA')
        scale=min(w/im.width,h/im.height); iw=im.width*scale;ih=im.height*scale
        xx=x+(w-iw)/2;yy=y+(h-ih)/2
        self.slide.shapes.add_picture(str(path),emu(xx),emu(yy),width=emu(iw),height=emu(ih))
        im=im.resize((max(1,round(iw*2)),max(1,round(ih*2))),Image.Resampling.LANCZOS)
        self.img.paste(im,(round(xx*2),round(yy*2)),im)

    def save_preview(self,lang,index):
        folder=PREVIEW/lang;folder.mkdir(parents=True,exist_ok=True)
        self.img.resize((W,H),Image.Resampling.LANCZOS).save(folder/f'{index:02}.png')


def logo(c,x,y,w=102,h=59):
    c.rect(x,y,w,h,WHITE);c.picture('/goto_logo.png',x+12,y+9,w-24,h-18)


def frame(c,s,total,is_id,title=None,folio=None):
    section=s.get('section_name') or s.get('section_tag','')
    c.text(section.upper(),51,35,1000,20,11,'#c5f1cb',True)
    c.text(title or s.get('display_title') or s['title'],51,65,975,105,35,WHITE,True,min_size=25)
    logo(c,1127,35)
    c.rule(51,670,1178,'#4d8b5c')
    c.text('GROUP 4 / IDX: GOTO',51,683,145,18,8,WHITE,True)
    c.text(s.get('source_footer',''),205,683,940,24,8,'#d9f0df')
    c.text(folio or f"{s['slide_num']:02} / {total}",1150,683,78,18,8,'#d9f0df',align='right')


def notes(c,s):
    parts=[s.get('speaker_notes','')]
    if s.get('study_explanation'):parts.append(s['study_explanation'])
    if s.get('calculation_notes'):
        parts.append('\nFORMULAS AND CALCULATIONS')
        for n in s['calculation_notes']:
            parts.append('\n'.join(str(n.get(k,'')) for k in ['label','formula','substitution','result','note','source']))
    c.slide.notes_slide.notes_text_frame.text='\n\n'.join(p for p in parts if p)


def cover(prs,s,total,is_id):
    c=Canvas(prs)
    logo(c,64,50,141,77)
    c.text('Pembukaan' if is_id else 'Opening',1060,86,155,22,13,WHITE,True,align='right')
    c.text('PT GoTo Gojek Tokopedia Tbk',64,167,680,26,16,'#edffeb')
    c.text('GoTo',60,208,700,116,92,WHITE,True)
    c.text('Analisis ekuitas' if is_id else 'Equity analysis',64,325,700,70,43,WHITE,True)
    c.text('Gojek · GoTo Financial · 24,99% Tokopedia' if is_id else 'Gojek · GoTo Financial · 24.99% Tokopedia',64,404,680,30,14,WHITE,True)
    c.text('Dari model bisnis hingga arus kas, valuasi, dan keputusan.' if is_id else 'From the business model to cash flow, value, and a decision.',64,452,640,80,17,'#e7f5ea')
    c.rect(806,158,.8,472,'#4d8b5c')
    items=[('UNTUK SIAPA' if is_id else 'OUR USER','Investor saham publik jangka pendek' if is_id else 'Short-term public equity investor'),('HARGA ACUAN TUGAS' if is_id else 'ASSIGNMENT REFERENCE PRICE','Rp 25 per saham' if is_id else 'Rp 25 per share'),('CAKUPAN ANALISIS' if is_id else 'ANALYSIS SCOPE','Model bisnis, industri, hasil keuangan, kualitas akuntansi, proyeksi dan valuasi.' if is_id else 'Business model, industry, financial results, accounting quality, forecasts and valuation.')]
    yy=172
    for i,(label,value) in enumerate(items):
        if i:c.rule(833,yy-19,382,'#4d8b5c')
        c.text(label,833,yy,382,20,10,'#c5e8ce',True)
        ht=c.text(value,833,yy+30,376,105,27 if i==1 else 15,WHITE,i==1)
        yy+=max(114,ht+66)
    c.text('Aktual 2023–2025 · Proyeksi 2026–2028' if is_id else '2023–2025 actuals · 2026–2028 forecasts',833,yy-6,375,32,10,'#c5e8ce')
    c.text('GROUP 4',64,581,650,18,10,WHITE,True)
    c.text('Fagly Ramschie · Anggreini Ruitan · Galatia Rompas\nMagister Manajemen, Universitas Klabat',64,606,680,42,12,WHITE)
    c.rule(51,670,1178,'#4d8b5c')
    c.text('IDX: GOTO',51,683,90,18,8,WHITE,True)
    c.text(s.get('source_footer',''),155,683,960,24,8,'#d9f0df')
    c.text(f'01 / {total}',1150,683,78,18,8,'#d9f0df',align='right')
    notes(c,s);return c


def analysis(c,s,x,w,is_id):
    points=s.get('analysis_points',[])[:3]
    gap=22
    heights=[]
    # The web uses open white paragraphs on the green canvas, no UI cards.
    size=14
    while True:
        heights=[28+len(lines_for(p.get('text',''),w,size))*size*1.5 for p in points]
        if sum(heights)+gap*(len(points)-1)<=450 or size<=12:break
        size-=.5
    spare=max(0,452-sum(heights)-gap*(len(points)-1))
    yy=190
    for i,(p,hh) in enumerate(zip(points,heights)):
        if i:c.rule(x,yy-13,w,'#4d8b5c')
        c.text(p.get('heading',''),x,yy,w,28,15,WHITE,True,min_size=13)
        c.text(p.get('text',''),x,yy+29,w,hh-25,size,'#f1f8f3')
        yy+=hh+gap+(spare/2 if i<2 else 0)


def table(c,headers,rows,x,y,w,maxh,font_size=14,widths=None,padding=20,center=False):
    n=len(headers)
    widths=widths or ([.34]+[(1-.34)/(n-1)]*(n-1) if n>1 else [1])
    # Measure all cells to allocate natural row heights rather than fixed boxes.
    size=font_size
    while True:
        hh=max(len(lines_for(v,w*widths[i]-18,size-1,True))*(size-1)*1.4+padding for i,v in enumerate(headers))
        heights=[max(len(lines_for(str(row[i]) if i<len(row) else '',w*widths[i]-18,size,i==0))*size*1.4+padding for i in range(n)) for row in rows]
        if hh+sum(heights)<=maxh or size<=8:break
        size-=.5
    if hh+sum(heights)>maxh:raise ValueError('Table does not fit: '+str(headers))
    if center:y+=(maxh-hh-sum(heights))/2
    xx=x
    for i,v in enumerate(headers):
        cw=w*widths[i];c.rect(xx,y,cw,hh,PALE)
        c.text(v,xx+9,y+padding/2,cw-18,hh-padding/2,size-1,GREEN,True)
        xx+=cw
    yy=y+hh
    for ri,row in enumerate(rows):
        xx=x; rh=heights[ri]
        for i in range(n):
            cw=w*widths[i]
            c.text(str(row[i]) if i<len(row) else '',xx+9,yy+padding/2,cw-18,rh-padding/2,size,DARK if i==0 else BODY,i==0)
            xx+=cw
        if ri<len(rows)-1:c.rule(x,yy+rh,w)
        yy+=rh
    return yy


def editorial(c,rows,x,y,w,h):
    for i,row in enumerate(rows):
        yy=y+i*h/3;hh=h/3
        image=row.get('img');ix=0
        if image:
            c.picture(image,x+12,yy+(hh-86)/2,104,86);ix=124
        val=str(row.get('value',''))
        vw=max(100,min(220,measure(val,23,True)+4))
        tw=w-ix-vw-42
        c.text(row.get('name',''),x+16+ix,yy+34,tw,42,19,DARK,True,min_size=16)
        c.text(row.get('text',''),x+16+ix,yy+82,tw+14,hh-87,14,MUTED,min_size=12)
        c.text(val,x+w-vw-16,yy+(hh-34)/2,vw,70,23,GREEN,True,align='right',min_size=18)
        if i<len(rows)-1:c.rule(x+16,yy+hh,w-32)


def bars(c,series,x,y,w,h,title,unit='',formula='',provisions=False):
    c.text(title,x,y,w,38,12,DARK,True)
    if unit:c.text(unit,x,y+27,w,20,10,MUTED)
    start=y+58;maxval=max(abs(r['value']) for r in series)*1.1
    step=min(48,(h-75)/max(1,len(series)))
    for i,r in enumerate(series):
        yy=start+i*step
        label=r.get('label',r.get('period',''))
        val=r['value'];value=f'{abs(val):,}' if isinstance(val,int) else f'{val:.2f}'
        if val<0:value='−'+value
        if provisions:
            c.text(label,x,yy,w*.18,20,12,MUTED)
            tx=x+w*.2;tw=w*.60
            c.rect(tx,yy+3,tw,14,PALE);c.rect(tx,yy+3,tw*abs(val)/maxval,14,GREEN if i==len(series)-1 else '#9ecbaa')
            c.text(value,x+w*.82,yy,w*.18,22,13,DARK,True,align='right')
        else:
            c.text(label,x,yy,w-65,25,11,MUTED)
            c.text(value,x+w-70,yy,70,22,14,DARK,True,align='right')
            c.rect(x,yy+25,w,10,PALE);c.rect(x,yy+25,w*abs(val)/maxval,10,GREEN if i==0 else DARK)
    if formula:c.text(formula,x,y+h-25,w,30,9,MUTED)


def valuation(c,s,x,y,w,h):
    c.text('Hasil Valuasi (Rp/saham)' if s.get('_is_id') else 'Valuation Results (Rp/share)',x,y,w,24,12,DARK,True)
    left=x+123;right=x+w-67;span=right-left
    def pos(v):return left+(v+140)/260*span
    c.rect(pos(0),y+34,.7,112,'#a4bfae');c.rect(pos(25),y+34,.7,112,DARK)
    c.text('Rp25',pos(25)-30,y+18,60,18,9,MUTED,align='center')
    for i,r in enumerate(s['valuation_range']):
        yy=y+48+i*34;v=r['value']
        c.text(r['label'],x,yy,115,22,12,DARK)
        c.rect(min(pos(v),pos(0)),yy,max(1,abs(pos(v)-pos(0))),20,'#a8cdb3' if v<0 else GREEN)
        c.text(('−' if v<0 else '+')+f'{abs(v):.1f}',right+7,yy,60,22,13,DARK,True,align='right')
    if s.get('chart_formula'):c.text(s['chart_formula'],x,y+h-25,w,30,9,MUTED)


def main_slide(prs,s,total,is_id):
    c=Canvas(prs);frame(c,s,total,is_id)
    # Coordinates reproduce the Vue grid: evidence left, open analysis right.
    x,y,w,h=51,180,716,468
    if s.get('topic_id')=='business':w=657
    right=x+w+38;rw=1229-right
    c.rect(x,y,w,h,WHITE)
    analysis(c,s,right,rw,is_id)
    if s.get('visual_rows'):
        editorial(c,s['visual_rows'],x+14,y+7,w-28,h-14)
    elif s.get('five_forces'):
        headers=['Kekuatan','Penilaian','Dasar penilaian'] if is_id else ['Force','Rating','Basis for assessment']
        end=table(c,headers,s['five_forces'],x+15,y+15,w-30,260,12,widths=[.21,.25,.54])
        cy=max(end+25,y+270);cw=(w-65)/2
        c.rule(x+18,cy-15,w-36)
        sc=s.get('competitive_spending_chart',{})
        spending=deepcopy(sc.get('series',[]))
        if is_id:
            for r in spending:r['label']=r.get('label_id',r['label'])
        bars(c,spending,x+20,cy,cw,h-(cy-y)-8,'Belanja untuk bersaing' if is_id else 'Spending to compete','2025 · Rp triliun' if is_id else '2025 · Rp trillion')
        cc=s.get('competition_chart',{})
        bars(c,cc.get('series',[]),x+45+cw,cy,cw,h-(cy-y)-8,'Provisi kerugian kredit' if is_id else 'Credit-loss provisions','Rp miliar · +134%' if is_id else 'Rp billion · +134%',cc.get('formula',''),True)
    elif s.get('table'):
        tbl=s['table'];tx=x+16;tw=w-32
        if s.get('loss_chart'):
            end=table(c,tbl['headers'],tbl['rows'],tx,y+17,tw,230,13)
            cy=end+26;c.rule(tx,cy-12,tw)
            bars(c,s['loss_chart']['series'],tx,cy,tw,h-(cy-y)-9,s['loss_chart']['title'],'',s.get('chart_formula',''),True)
        elif s.get('valuation_range'):
            end=table(c,tbl['headers'],tbl['rows'],tx,y+13,tw,165,11,widths=[.64,.36])
            cy=end+15;c.rule(tx,cy-5,tw)
            valuation(c,{**s,'_is_id':is_id},tx,cy,tw,170)
            yy=cy+173
            c.rule(tx,yy,tw)
            for p in s.get('peer_exclusions',[]):
                c.text(p['company'],tx,yy+9,107,30,11,DARK,True)
                ht=c.text(p['reason'],tx+112,yy+9,tw-112,58,10,MUTED,min_size=9)
                yy+=max(36,ht+14)
        else:
            widths=None
            if s.get('topic_id')=='wacc': widths=[.33,.16,.51]
            table(c,tbl['headers'],tbl['rows'],tx,y+24,tw,h-48,14,widths,center=True)
    notes(c,s);return c


def appendix(prs,s,total,is_id):
    # Preserve the established grouping of the exported workbook schedules.
    schedules=([s['table']] if s.get('table') else [])+s.get('supporting_schedules',[])
    pages=[];page=[];used=0
    for schedule in schedules:
        est=min(5.4,.45+.32*(1+len(schedule.get('rows',[])))+(.25 if schedule.get('note') else 0))
        if page and used+est>5.4:
            pages.append(page);page=[];used=0
        page.append((schedule,est));used+=est+.2
    if page:pages.append(page)
    output=[]
    for pi,page in enumerate(pages):
        c=Canvas(prs)
        # Short section heading keeps the appendix title clear above its tables.
        title=s.get('display_title') or s['title']
        title=title.split(': ',1)[-1]
        frame(c,s,total,is_id,title=title,folio=f"A{s['slide_num']-12} · {pi+1}/{len(pages)}")
        c.rect(51,180,1178,468,WHITE)
        available=440
        estimates=sum(est for _,est in page)+.2*(len(page)-1)
        yy=192
        for schedule,est in page:
            height=available*est/estimates
            c.text(schedule.get('title',''),69,yy,1140,35,12,GREEN,True,min_size=10)
            th=height-43-(23 if schedule.get('note') else 0)
            headers=schedule.get('headers',[])
            widths=None
            if len(headers)==7:widths=[.18,.08,.24,.08,.17,.08,.17]
            elif len(headers)==6:widths=[.28,.15,.15,.14,.12,.16]
            elif len(headers)==3:widths=[.28,.18,.54]
            table(c,headers,schedule.get('rows',[]),69,yy+36,1142,th,12,widths,padding=10)
            if schedule.get('note'):
                c.text(schedule['note'],69,yy+height-25,1142,25,8,MUTED,min_size=7)
            yy+=height+8
        notes(c,s);output.append(c)
    return output


def generate(json_path,out,is_id):
    deck=json.loads(json_path.read_text())
    prs=Presentation();prs.slide_width=emu(W);prs.slide_height=emu(H)
    prs.core_properties.author='Group 4';prs.core_properties.title='GoTo Equity Analysis';prs.core_properties.subject='Web presentation design, editable PowerPoint export'
    canvases=[]
    for s in deck:
        if s['slide_num']==1:canvases.append(cover(prs,s,len(deck),is_id))
        elif s.get('is_appendix'):canvases.extend(appendix(prs,s,len(deck),is_id))
        else:canvases.append(main_slide(prs,s,len(deck),is_id))
    out.parent.mkdir(parents=True,exist_ok=True);prs.save(out)
    lang='id' if is_id else 'en'
    for i,c in enumerate(canvases,1):c.save_preview(lang,i)
    # Visual contact sheet for all exported pages.
    cols=4;thumbw=400;thumbh=225
    sheet=Image.new('RGB',(cols*thumbw,math.ceil(len(canvases)/cols)*(thumbh+28)),'#14251b')
    dr=ImageDraw.Draw(sheet)
    for i,c in enumerate(canvases):
        xx=(i%cols)*thumbw;yy=(i//cols)*(thumbh+28)
        sheet.paste(c.img.resize((thumbw,thumbh),Image.Resampling.LANCZOS),(xx,yy))
        dr.text((xx+10,yy+thumbh+5),f'{i+1:02}',fill='white')
    sheet.save(PREVIEW/f'contact-{lang}.jpg')
    print(f'Generated {out}: {len(prs.slides)} slides; editable text, tables and charts; previews {PREVIEW/lang}')


if __name__=='__main__':
    generate(DATA/'presentation_deck.json',PUBLIC/'Group4_Presentation_GOTO.pptx',False)
    generate(DATA/'presentation_deck_id.json',PUBLIC/'Group4_Presentation_GOTO_ID.pptx',True)
    # The assignment folder is also a user-facing copy of this same deck.
    import shutil
    shutil.copy2(PUBLIC/'Group4_Presentation_GOTO.pptx',ROOT/'ASSIGNMENTS/ASSSIGNMENT 16/Group4_Presentation_GOTO.pptx')
