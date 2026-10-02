#!/usr/bin/env python3
"""Generate fictional workshop profiles and idempotently upsert a participant.
This helper does not import, select delivery recipients, or send email.
"""
import argparse,csv,hashlib,json,random,re,tempfile,os
from pathlib import Path
FIELDS='customer_id app_user_id email_address first_name last_name customer_status days_since_last_purchase expected_repurchase_days purchase_window_status purchased_in_last_30_days purchased_in_last_90_days purchased_in_last_120_days completed_orders_12m average_order_value_12m net_sales_12m preferred_channel next_best_channel next_best_product_id propensity_to_churn propensity_to_convert email_consent_status push_consent_status sms_consent_status in_app_consent_status loyalty_status loyalty_tier points_balance postal_code record_role'.split()
NAMES=[('Avery','Carter'),('Jordan','Bennett'),('Riley','Reed'),('Reese','Sutton'),('Morgan','Morgan'),('Casey','Brooks'),('Skyler','Marlow'),('Parker','Ellis'),('Quinn','Parker'),('Taylor','Hayes')]
def profile(index,rng,participant=False):
 days=180 if participant else rng.choice([22,42,76,130,184,267,299]); expected=90 if participant else rng.choice([60,75,90,120]);orders=rng.randint(1,8);aov=rng.randint(60,450)
 enrolled=rng.choice([True,False]); channel='email' if participant else rng.choice(['email','push','sms','in_app'])
 row=dict.fromkeys(FIELDS,'');row.update(record_role='business_customer',customer_id=f'WS-C{index:06d}',app_user_id=f'WS-APP{index:06d}',email_address=f'success+sample{index:03d}@simulator.amazonses.com',first_name=NAMES[(index-1)%10][0],last_name=NAMES[(index-1)%10][1],customer_status='active',days_since_last_purchase=days,expected_repurchase_days=expected,purchase_window_status='overdue' if days>expected else 'on_track',completed_orders_12m=orders,average_order_value_12m=f'{aov:.2f}',net_sales_12m=f'{orders*aov:.2f}',preferred_channel=channel,next_best_channel=channel,propensity_to_churn=0.75 if participant else round(rng.uniform(.15,.9),2),propensity_to_convert=.6 if participant else round(rng.uniform(.2,.85),2),loyalty_status='enrolled' if enrolled else 'not_enrolled',loyalty_tier=rng.choice(['bronze','silver','gold']) if enrolled else 'none',points_balance=rng.randint(0,5000) if enrolled else 0,postal_code=f'{rng.randint(0,99999):05d}')
 for n in (30,90,120): row[f'purchased_in_last_{n}_days']='Y' if days<=n else 'N'
 for channel in ['email','push','sms','in_app']: row[channel+'_consent_status']=('GRANTED' if channel=='email' else 'DENIED') if participant else rng.choice(['GRANTED','DENIED'])
 # Curated fictional fixture: both workshop targeting strategies have sample
 # evidence even when the participant is a separate identity-only QA row.
 if not participant and index in (1,2,3):
  days=150+30*index
  row.update(days_since_last_purchase=days,expected_repurchase_days=90,purchase_window_status='overdue',propensity_to_churn={1:.72,2:.81,3:.88}[index],email_consent_status='GRANTED')
  for n in (30,90,120):row[f'purchased_in_last_{n}_days']='N'
 return row
def main():
 p=argparse.ArgumentParser();p.add_argument('--csv',required=True);p.add_argument('--email',required=True);p.add_argument('--first-name',required=True);p.add_argument('--last-name',required=True);p.add_argument('--seed',type=int,default=2026);p.add_argument('--workshop-data',action='store_true',help='Confirm existing CSV provenance permits fictional sample replenishment');p.add_argument('--participant-role',choices=['business_customer','workshop_self_test'],default='business_customer');p.add_argument('--self-test-output');a=p.parse_args()
 email=a.email.strip()
 if not re.fullmatch(r'[^\s@,<>]+@[^\s@,<>]+\.[^\s@,<>]+',email):p.error('Provide a valid participant email')
 if re.fullmatch(r'success(?:\+[A-Za-z0-9_-]+)?@simulator\.amazonses\.com',email,re.I):p.error('Participant must supply their own email, not the shared simulator address')
 if not a.first_name.strip() or not a.last_name.strip():p.error('Both names are required')
 if a.participant_role=='workshop_self_test':
  if not a.self_test_output:p.error('QA role requires a separate --self-test-output CSV')
  if Path(a.self_test_output).resolve()==Path(a.csv).resolve():p.error('QA CSV must be separate from the business source')
 path=Path(a.csv);rng=random.Random(a.seed);rows=[];fields=FIELDS[:]
 if path.exists():
  with path.open(encoding='utf-8-sig',newline='') as f:
   reader=csv.DictReader(f)
   if not reader.fieldnames or 'email_address' not in reader.fieldnames:p.error('Existing CSV must contain email_address')
   fields=list(dict.fromkeys(reader.fieldnames+FIELDS));rows=list(reader)
 # Generate the full baseline even on continuation so missing samples are stable
 # for a given seed, regardless of which rows already exist.
 samples=[profile(i,rng) for i in range(1,31)]
 if not path.exists():rows=samples
 elif a.workshop_data:
  existing_ids=[r.get('customer_id','') for r in rows]
  for sample in samples:
   sample_id=sample['customer_id']
   if existing_ids.count(sample_id)>1:p.error('Duplicate workshop sample IDs; reconcile before replenishing')
   if sample_id not in existing_ids:
    if any(r.get('email_address','').strip().casefold()==sample['email_address'].casefold() for r in rows):p.error('Sample address belongs to a different row; reconcile before replenishing')
    rows.append({**dict.fromkeys(fields,''),**sample})
 for row in rows:
  if a.workshop_data and re.fullmatch(r'WS-C[0-9]{6}',row.get('customer_id','')) and (row.get('email_address','').endswith('@northstar.example') or re.fullmatch(r'success(?:\+[A-Za-z0-9_-]+)?@simulator\.amazonses\.com',row.get('email_address',''),re.I)):
   row['email_address']=f"success+sample{int(row['customer_id'][4:]):03d}@simulator.amazonses.com"
 matches=[r for r in rows if r.get('email_address','').strip().casefold()==email.casefold()]
 if len(matches)>1:p.error('Duplicate participant emails in existing CSV; reconcile before updating')
 if a.participant_role=='workshop_self_test':
  if matches and any(r.get('email_consent_status','')=='DENIED' for r in matches):p.error('Existing DENIED consent must be resolved explicitly; QA cannot bypass it')
  # Identity-only QA artifact: do not invent purchase/churn signals or modify
  # a matching business customer to satisfy audience eligibility.
  qa=dict.fromkeys(fields,'');digest=hashlib.sha256(email.casefold().encode()).hexdigest()[:16]
  qa.update(customer_id='WS-QA-'+digest,app_user_id='WS-QA-APP-'+digest,email_address=email,first_name=a.first_name.strip(),last_name=a.last_name.strip(),record_role='workshop_self_test',email_consent_status='GRANTED')
 elif matches:
  row=matches[0];row.update(email_address=email,first_name=a.first_name.strip(),last_name=a.last_name.strip())
 else:
  row=profile(31,rng,True);digest=hashlib.sha256(email.casefold().encode()).hexdigest()[:16];row.update(customer_id='WS-P-'+digest,app_user_id='WS-APP-'+digest,email_address=email,first_name=a.first_name.strip(),last_name=a.last_name.strip());rows.append(row)
 path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.audience-',suffix='.csv')
 try:
  with os.fdopen(fd,'w',encoding='utf-8',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
  os.replace(tmp,path)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 if a.participant_role=='workshop_self_test':
  qa_path=Path(a.self_test_output);qa_path.parent.mkdir(parents=True,exist_ok=True)
  fd,tmp=tempfile.mkstemp(dir=qa_path.parent,prefix='.self-test-',suffix='.csv')
  try:
   with os.fdopen(fd,'w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerow(qa)
   os.replace(tmp,qa_path)
  finally:
   if os.path.exists(tmp):os.unlink(tmp)
 print(json.dumps({'profiles':len(rows),'participant_rows':1 if a.participant_role=='business_customer' else 0,'qa_rows':1 if a.participant_role=='workshop_self_test' else 0,'csv':str(path),'self_test_csv':a.self_test_output if a.participant_role=='workshop_self_test' else None,'status':'saved','behavioral_defaults':'fictional business samples; QA has identity only; existing attributes preserved'}))
if __name__=='__main__':main()
