"""Prepare upload copies by editing Office package metadata directly."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
from datetime import datetime, timezone
import re

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'goto-fsa-study/public'
DEST=ROOT/'ASSIGNMENTS/ASSSIGNMENT 16'
AUTHOR='Fagly Ramschie'
CP='http://schemas.openxmlformats.org/package/2006/metadata/core-properties'
DC='http://purl.org/dc/elements/1.1/'
DCT='http://purl.org/dc/terms/'
EP='http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
for prefix,uri in [('cp',CP),('dc',DC),('dcterms',DCT),('xsi','http://www.w3.org/2001/XMLSchema-instance')]:E.register_namespace(prefix,uri)

def setval(root,ns,key,value):
 node=root.find('{'+ns+'}'+key)
 if node is None:node=E.SubElement(root,'{'+ns+'}'+key)
 node.text=str(value)
 return node

def prepare(path):
 with ZipFile(path) as z:
  assert z.testzip() is None
  entries=[(info,z.read(info.filename)) for info in z.infolist()]
 stamp=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
 slidecount=sum(bool(re.fullmatch(r'ppt/slides/slide\d+\.xml',info.filename)) for info,_ in entries)
 revised=[]
 for info,data in entries:
  if info.filename=='docProps/core.xml':
   root=E.fromstring(data)
   setval(root,DC,'creator',AUTHOR);setval(root,CP,'lastModifiedBy',AUTHOR)
   setval(root,DC,'description','GoTo financial statement analysis. Prepared by Fagly Ramschie.')
   setval(root,DC,'subject','Financial Statement Analysis: GoTo')
   for key in ['created','modified']:
    node=setval(root,DCT,key,stamp)
    node.set('{http://www.w3.org/2001/XMLSchema-instance}type','dcterms:W3CDTF')
   data=E.tostring(root,encoding='utf-8',xml_declaration=True)
  elif info.filename=='docProps/app.xml':
   root=E.fromstring(data)
   # Optional software-version fields are not relevant to submission authorship.
   for child in list(root):
    if child.tag in ['{'+EP+'}Application','{'+EP+'}AppVersion']:root.remove(child)
   if path.suffix=='.pptx':
    setval(root,EP,'Slides',slidecount)
    setval(root,EP,'Notes',sum(bool(re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',i.filename)) for i,_ in entries))
    setval(root,EP,'PresentationFormat','On-screen Show (16:9)')
   data=E.tostring(root,encoding='utf-8',xml_declaration=True)
  revised.append((info,data))
 temp=path.with_name(path.name+'.metadata-tmp')
 with ZipFile(temp,'w',ZIP_DEFLATED) as z:
  for info,data in revised:z.writestr(info,data)
 with ZipFile(temp) as z:
  assert z.testzip() is None
  for name in z.namelist():
   if name.endswith('.xml'):
    data=z.read(name).decode('utf-8')
    assert not re.search(r'python-pptx|pypptx|openpyxl|Steve Canny',data,re.I),(path,name)
  core=E.fromstring(z.read('docProps/core.xml'))
  assert core.find('{'+DC+'}creator').text==AUTHOR
  assert core.find('{'+CP+'}lastModifiedBy').text==AUTHOR
 temp.replace(path)
 return path.read_bytes()

if __name__=='__main__':
 DEST.mkdir(parents=True,exist_ok=True)
 for filename in ['Group4_Presentation_GOTO.pptx','Group4_Presentation_GOTO_ID.pptx','appendix.xlsx']:
  data=prepare(PUBLIC/filename)
  if filename=='Group4_Presentation_GOTO.pptx':
   (DEST/'Fagly_Ramschie_GOTO_Presentation.pptx').write_bytes(data)
  elif filename=='appendix.xlsx':
   (DEST/'Fagly_Ramschie_GOTO_Appendix.xlsx').write_bytes(data)
 print('Verified metadata and saved the English presentation and appendix in Assignment 16.')
