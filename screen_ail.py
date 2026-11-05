import pandas as pd, re
d=pd.read_csv('/mnt/user-data/uploads/merged_records_1.csv')
d['title']=d['title'].fillna(''); d['abstract']=d['abstract'].fillna('')
T=d.title.str.lower(); A=d.abstract.str.lower(); TA=T+' '+A
lit=r"(ai literacy|artificial intelligence literacy|a\.i\. literacy|generative ai literacy|genai literacy|chatgpt literacy|ai competenc|artificial intelligence competenc|ai fluency|critical ai literacy)"
he=r"(higher education|universit|undergraduate|college student|postgraduate|graduate student|tertiary|pre-service teacher|preservice teacher|medical student|nursing student|bachelor)"
iv=r"(intervention|course|workshop|training|module|program|curricul|instruction|teaching unit|lesson|bootcamp|micro-credential|pedagogical design|learning activit)"
ev=r"(pre-?tests?|post-?tests?|pre- ?and post|pre/post|pretest-posttest|quasi-experiment|experimental group|control group|randomi[sz]ed|comparison group|before and after the|one-group|single-group|paired[- ]samples?|ancova|repeated[- ]measures|effect sizes?|pre- ?(and|to) post-?(intervention|course|training))"
nonen=r"\b(pelatihan|untuk|meningkatkan|mahasiswa|dalam|pada|dan|yang|estudiantes|alfabetizaci|inteligencia|literacia|para el|de la|des |und |der |kecerdasan|siswa|pengaruh)\b"
staff=r"\b(lecturers?|faculty members?|instructors?'|academic staff|librarians?)\b"
rev=r"(systematic review|scoping review|literature review|meta-analy|bibliometric|a review of|review of the literature|state of the art|editorial|protocol|framework proposal|position paper)"
k12=r"(k-12|primary school|elementary school|secondary school|high school|middle school|kindergarten|children)"
def decide(i):
    t,a,ta=T[i],A[i],TA[i]; v=str(d.venue[i]).lower(); ty=str(d.type[i]).lower(); vt=str(d.venue_type[i]).lower()
    if re.search(rev,t) or 'review' in ty: return 'EC4 review/editorial/protocol'
    if 'arxiv' in v or vt=='repository' or 'preprint' in ty or 'ssrn' in v or 'research square' in v: return 'EC4 non-peer-reviewed'
    if not re.search(lit,ta): return 'EC1 not AI literacy/competence'
    if not re.search(he,ta): return 'EC1 not higher education'
    if re.search(k12,t) and not re.search(he,t): return 'EC1 school-level'
    if re.search(nonen,t): return 'EC5 non-English'
    if re.search(staff,t) and not re.search(r'student',t): return 'EC1 staff, not students'
    if not re.search(iv,ta): return 'EC2 no educational intervention'
    if a and not re.search(ev,a): return 'EC3 no evaluated outcome (descriptive/survey)'
    if not a and not re.search(r'(effect|impact|evaluat|experiment|interven)',t): return 'EC3 no evaluated outcome (no abstract)'
    return 'INCLUDE'
d['ta_decision']=[decide(i) for i in range(len(d))]
print(d.ta_decision.value_counts())
inc=d[d.ta_decision=='INCLUDE']; print(inc.year.value_counts().sort_index()); print('oa',(inc.oa_url.fillna('')!='').sum(),'doi',(inc.doi.fillna('')!='').sum())
d.to_csv('screened_ail.csv',index=False)
for _,r in inc.sample(min(25,len(inc)),random_state=3).iterrows(): print('-',r.year,r.title[:120])
