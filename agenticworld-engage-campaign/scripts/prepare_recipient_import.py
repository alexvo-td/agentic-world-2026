#!/usr/bin/env python3
"""Convert an already selected delivery CSV to the required physical email column.
This helper does not choose recipients, import tables, or send email.
"""
import argparse,csv,os,tempfile
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 source=Path(a.input).resolve();target=Path(a.output).resolve()
 if source==target:p.error('Preserve the source CSV; use a distinct output path')
 with source.open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f);fields=reader.fieldnames or []
  if 'email_address' not in fields and 'email' not in fields:p.error('CSV needs email_address or email')
  rows=list(reader)
 for n,row in enumerate(rows,2):
  old=(row.get('email_address') or '').strip();email=(row.get('email') or '').strip()
  if email and old and email.casefold()!=old.casefold():p.error(f'Conflicting email columns at row {n}')
  row['email']=email or old
  if not row['email']:p.error(f'Missing email at row {n}')
 fields=['email']+[x for x in fields if x not in ('email','email_address')]
 for row in rows:row.pop('email_address',None)
 target.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(dir=target.parent,prefix='.recipients-',suffix='.csv')
 try:
  with os.fdopen(fd,'w',encoding='utf-8',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
  os.replace(tmp,target)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 print(f'Prepared {len(rows)} selected rows with physical email column; source preserved.')
if __name__=='__main__':main()
