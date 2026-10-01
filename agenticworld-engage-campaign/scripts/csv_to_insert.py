#!/usr/bin/env python3
"""Generate a Trino INSERT file; never execute SQL or print profile values."""
import argparse,csv,re,time
from pathlib import Path

def ident(value):
 if not re.fullmatch(r'[a-z][a-z0-9_]*',value):raise ValueError('Identifiers must be lowercase SQL-safe names')
 return '"'+value+'"'
def literal(value):
 if any(c in value for c in ('\x00','\r','\n')):raise ValueError('NUL and multiline cells are unsupported')
 return "'"+value.replace("'","''")+"'"
def main():
 p=argparse.ArgumentParser();p.add_argument('--csv',required=True);p.add_argument('--table',required=True);p.add_argument('--output',required=True);p.add_argument('--database',default='agentic_world_demo');p.add_argument('--ingest-time',type=int);a=p.parse_args()
 if a.database!='agentic_world_demo':p.error('Only the workshop output database is supported')
 try:
  table=ident(a.database)+'.'+ident(a.table)
  with open(a.csv,encoding='utf-8-sig',newline='') as f:
   reader=csv.DictReader(f);fields=reader.fieldnames or [];rows=list(reader)
  if len(set(fields))!=len(fields) or 'email' not in fields:raise ValueError('Unique headers including email are required')
  if not rows:raise ValueError('No recipient rows selected')
  for key in fields:ident(key)
  stamp=a.ingest_time if a.ingest_time is not None else int(time.time())
  if stamp<0:raise ValueError('Ingest time must be nonnegative Unix seconds')
  columns=fields if 'time' in fields else ['time']+fields
  values=[];emails=set()
  for row in rows:
   if None in row or any(v is None for v in row.values()):raise ValueError('Inconsistent CSV cell count')
   email=row['email']
   if not re.fullmatch(r'[^\s@,<>]+@[^\s@,<>]+\.[^\s@,<>]+',email):raise ValueError('Invalid recipient email')
   if email.casefold() in emails:raise ValueError('Duplicate recipient email')
   emails.add(email.casefold());cells=[]
   for key in columns:
    if key=='time':
     raw=row.get('time',str(stamp))
     if not re.fullmatch(r'[0-9]+',raw):raise ValueError('time must be nonnegative Unix seconds')
     cells.append(str(int(raw)))
    else:cells.append(literal(row[key]))
   values.append('('+', '.join(cells)+')')
  sql='INSERT INTO '+table+' ('+', '.join(map(ident,columns))+')\nVALUES\n'+',\n'.join(values)+';\n'
  output=Path(a.output)
  if output.resolve()==Path(a.csv).resolve():raise ValueError('SQL output must not overwrite the CSV')
  output.parent.mkdir(parents=True,exist_ok=True)
  with output.open('x',encoding='utf-8') as f:f.write(sql)
  output.chmod(0o600)
  print(f'Prepared INSERT SQL for {len(rows)} rows and {len(columns)} columns; not executed.')
 except (ValueError,FileExistsError) as e:p.error(str(e))
if __name__=='__main__':main()
