#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request,urlopen
import hashlib,json,os,shutil
BASE='https://uns-website-1.vercel.app';FORM='https://form.jotform.com/262473510150043';ROOT=Path(__file__).parent.resolve();OUT=ROOT/'dist'
LEADERSHIP='''<section class="section neutral" id="leadership"><div class="container"><div class="section-heading"><p class="eyebrow">University leadership</p><h2>Leadership team</h2><p>The officers serving the University of Northeastern Somalia.</p></div><div class="opportunity-grid"><article class="simple-card"><p class="eyebrow">President</p><h3>Prof. Abdiqani Ashkir</h3></article><article class="simple-card"><p class="eyebrow">Academic Director</p><h3>Abdulahi Mohamed Said</h3></article><article class="simple-card"><p class="eyebrow">Academic Advisor</p><h3>Abdulahi A. Hasan</h3></article><article class="simple-card"><p class="eyebrow">Operations Director</p><h3>Ahmed A. Osman</h3></article><article class="simple-card"><p class="eyebrow">Students Affairs Administrator</p><h3>Sakarie Abdulahi Said</h3></article></div></div></section>'''
FILES={'index.html':'/','about/index.html':'/about/','academics/index.html':'/academics/','admissions/index.html':'/admissions/','learning-options/index.html':'/learning-options/','research/index.html':'/research/','career-development/index.html':'/career-development/','news-events/index.html':'/news-events/','contact/index.html':'/contact/','assets/styles.css':'/assets/styles.css','assets/site.js':'/assets/site.js','assets/uns-logo.jpg':'/assets/uns-logo.jpg','assets/uns-map.png':'/assets/uns-map.png','robots.txt':'/robots.txt','sitemap.xml':'/sitemap.xml'}
def fetch(r):
 with urlopen(Request(BASE+r,headers={'User-Agent':'UNS-Vercel-build/1.0'}),timeout=30)as x:return x.read()
def main():
 url=os.getenv('SUPABASE_URL','').rstrip('/');key=os.getenv('SUPABASE_PUBLISHABLE_KEY','')
 if not url.startswith('https://')or not key.startswith('sb_publishable_'):raise RuntimeError('Supabase build variables missing')
 if OUT.exists():shutil.rmtree(OUT)
 links=0
 for f,r in FILES.items():
  data=fetch(r)
  if f.endswith('.html'):
   t=data.decode().replace('href="/admissions/#apply"',f'href="{FORM}"').replace('href="mailto:info@uns.edu.so?subject=Student%20Portal%20Access"','href="/student/"')
   if f=='about/index.html'and'id="leadership"'not in t:t=t.replace('</main>',LEADERSHIP+'</main>')
   if f=='admissions/index.html':t=t.replace('Contact the Admissions team to begin your application and confirm current requirements.','Complete the official UNS online application form to begin your application.')
   data=t.encode();links+=t.count(FORM)
  p=OUT/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 if links!=56:raise RuntimeError(f'Expected 56 form links, found {links}')
 shutil.copytree(ROOT/'portal',OUT/'portal',ignore=shutil.ignore_patterns('config.js','__pycache__'));shutil.copytree(ROOT/'admin',OUT/'admin');shutil.copytree(ROOT/'student',OUT/'student')
 (OUT/'portal'/'config.js').write_text('window.UNS_PORTAL_CONFIG = '+json.dumps({'url':url,'publishableKey':key},separators=(',',':'))+';\n')
if __name__=='__main__':main()
