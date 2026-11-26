"""Kess Quiz — génère N vidéos (~61 s) : python3 daily.py ../videos 1"""
import sys, os, json, random, itertools, datetime, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); __file__=os.path.join(HERE,'core.py')
exec(open(os.path.join(HERE,'core.py')).read()); exec(open(os.path.join(HERE,'bank.py')).read())
TIMER=3; L=lambda v: len(v)/SR
THEMES={'drapeaux':("Drapeaux du monde",(32,190,200)),'capitales':("Capitales",(60,130,240)),'animaux':("Animaux",(60,175,90)),
        'sciences':("Sciences",(225,150,0)),'histoire':("Histoire",(200,110,60)),'géographie':("Géographie",(30,165,140)),'actu':("Actu",(210,70,150)),'trompe':("Kess se trompe ?",(255,140,40))}
MUSIC=[(122,220.0,[0,8,3,10],[0,None,7,None,12,10,7,None]),(126,246.9,[0,5,9,7],[0,4,7,None,9,7,4,None]),
       (118,196.0,[0,7,9,5],[7,None,4,None,0,2,4,None]),(128,233.1,[0,3,8,10],[0,3,7,10,7,3,None,None])]
HYPE=["Premier drapeau, on s'échauffe !","Et celui-ci ?","Attention, il y a un piège !","Et ce drapeau-là ?","Un grand classique !",
      "Celui-là, tu le connais ?","Ne confonds pas !","On accélère !","Pas si simple, celui-ci !","Et celui-là ?"]
NUM=["zéro","un","deux","trois","quatre","cinq","six","sept","huit","neuf","dix"]
HIST=os.path.join(HERE,'history.json')
hist=json.load(open(HIST)) if os.path.exists(HIST) else {'used':[],'videos':[]}
# ---------- dessin ----------
def draw_flag(d,code,x,y,w,h):
    if code not in FLAGS: return
    _,_,k,c,_=FLAGS[code]
    if k=='v':
        for i,col in enumerate(c): d.rectangle(z(x+i*w/3,y,x+(i+1)*w/3,y+h),fill=col)
    elif k=='h':
        for i,col in enumerate(c): d.rectangle(z(x,y+i*h/len(c),x+w,y+(i+1)*h/len(c)),fill=col)
    elif k=='co':
        d.rectangle(z(x,y,x+w,y+h/2),fill=c[0]); d.rectangle(z(x,y+h/2,x+w,y+3*h/4),fill=c[1]); d.rectangle(z(x,y+3*h/4,x+w,y+h),fill=c[2])
    elif k in('disc','disc_off'):
        d.rectangle(z(x,y,x+w,y+h),fill=c[0]); r=h*(0.3 if k=='disc' else 0.32); cx=x+w/2 if k=='disc' else x+w*0.45
        d.ellipse(z(cx-r,y+h/2-r,cx+r,y+h/2+r),fill=c[1])
    elif k=='swiss':
        s_=h; x0=x+(w-s_)/2; d.rectangle(z(x0,y,x0+s_,y+s_),fill=c[0]); a=s_*0.2; b=s_*0.6
        d.rectangle(z(x0+s_/2-a/2,y+s_/2-b/2,x0+s_/2+a/2,y+s_/2+b/2),fill=c[1]); d.rectangle(z(x0+s_/2-b/2,y+s_/2-a/2,x0+s_/2+b/2,y+s_/2+a/2),fill=c[1])
    elif k=='nordic':
        d.rectangle(z(x,y,x+w,y+h),fill=c[0]); t=h*0.2; cx=x+w*0.37
        d.rectangle(z(cx-t/2,y,cx+t/2,y+h),fill=c[1]); d.rectangle(z(x,y+h/2-t/2,x+w,y+h/2+t/2),fill=c[1])
    elif k=='nordic2':
        d.rectangle(z(x,y,x+w,y+h),fill=c[0]); t=h*0.25; t2=h*0.12; cx=x+w*0.37
        d.rectangle(z(cx-t/2,y,cx+t/2,y+h),fill=c[1]); d.rectangle(z(x,y+h/2-t/2,x+w,y+h/2+t/2),fill=c[1])
        d.rectangle(z(cx-t2/2,y,cx+t2/2,y+h),fill=c[2]); d.rectangle(z(x,y+h/2-t2/2,x+w,y+h/2+t2/2),fill=c[2])
def wrap(txt,font,maxw):
    out=[];line=""
    for w in txt.split():
        t=(line+" "+w).strip()
        if font.getlength(t)/S>maxw and line: out.append(line); line=w
        else: line=t
    return out+[line]
def timebar(fr,p,y=1575):
    d=ImageDraw.Draw(fr); x0,x1=150,930
    d.rounded_rectangle((x0,y,x1,y+22),11,fill=(236,233,245))
    c=(66,190,120) if p>0.5 else ((255,190,40) if p>0.25 else (255,90,90))
    if p>0.01: d.rounded_rectangle((x0,y,x0+int((x1-x0)*p),y+22),11,fill=c)
# ---------- items ----------
def flag_items(rng):
    codes=[c for c in FLAGS if 'f_'+c not in hist['used']] or list(FLAGS)
    rng.shuffle(codes); out=[]
    for i,c in enumerate(codes):
        opts=[FLAGS[c][0]]+[flag_name(x) for x in rng.sample(FLAG_DECOYS[c],2)]; rng.shuffle(opts)
        out.append(dict(id='f_'+c,flag=c,q="À quel pays est ce drapeau ?",opts=opts,ans=opts.index(FLAGS[c][0]),
                        say_q=HYPE[min(i,len(HYPE)-1)],say_a=f"C'est {FLAGS[c][1]} !",fact=FLAGS[c][4]))
    return out
def qcm_items(rng,theme):
    pool=[q for q in QCM if q[1]==theme and q[0] not in hist['used']] or [q for q in QCM if q[1]==theme]
    rng.shuffle(pool); out=[]
    for id_,th,q,o,sa,fact in pool:
        opts=list(o); rng.shuffle(opts)
        out.append(dict(id=id_,flag=None,q=q,opts=opts,ans=opts.index(o[0]),say_q=q,say_a=sa,fact=fact))
    return out
def trompe_items(rng):
    pool=[t for t in TROMPE if t[0] not in hist['used']] or list(TROMPE); rng.shuffle(pool)
    return [dict(id=t[0],q=t[1],disp=t[2],say=t[3],ok=t[4],say_a=t[5],expl=t[6]) for t in pool]
# ---------- plan (ajustement ~61 s) ----------
def fit(items,kind,intro_v,outro_fn):
    best=None
    for it in items:
        if kind=='trompe':
            it['vq']=tts(it['q'],0.8); it['vk']=tts("Kess répond : "+it['say']+" Il a raison ?",0.8); it['va']=tts(it['say_a'],0.8)
        else:
            it['vq']=tts(it['say_q'],0.8); it['va']=tts(it['say_a'],0.8); it['vf']=tts("Le savais-tu ? "+it['fact'],0.82) if it['fact'] else None
    def build(n,facts):
        t=L(intro_v)+0.6; segs=[]
        for i,it in enumerate(items[:n]):
            if kind=='trompe':
                talk=0.4+L(it['vq'])+0.1; ts=talk+L(it['vk'])+0.1; te=ts+TIMER; ra=te+0.2; end=ra+L(it['va'])+0.4
                segs.append(dict(s=t,talk=talk,ts=ts,te=te,ra=ra,fs=end,fe=end,fact=False,end=end))
            else:
                ts=0.4+L(it['vq'])+0.1; te=ts+TIMER; ra=te+0.2; fs=ra+L(it['va'])+0.35
                fe=fs+(0.3+L(it['vf'])+0.4 if i in facts else 0)
                segs.append(dict(s=t,ts=ts,te=te,ra=ra,fs=fs,fe=fe,fact=i in facts,end=fe))
            t+=segs[-1]['end']
        return segs,t
    for n in range(min(10,len(items)),1,-1):
        vo=outro_fn(n,items[:n])
        cand=[i for i in range(n) if kind!='trompe' and items[i]['fact']]
        for k in range(len(cand),-1,-1):
            for facts in itertools.combinations(cand,k):
                segs,tend=build(n,set(facts)); tot=tend+L(vo)+1.0
                if 59.5<=tot<=63.5:
                    sc=(n,k,-abs(61-tot))
                    if best is None or sc>best[0]: best=(sc,n,segs,tend,vo)
        if best: break
    if best is None:  # repli : le plus proche au-dessus de 60 s
        n=min(10,len(items)); segs,tend=build(n,set()); best=(None,n,segs,tend,outro_fn(n,items[:n]))
    return best[1:]
# ---------- rendu ----------
def render(kind,theme,out_path,seed):
    rng=random.Random(seed); label,ACC=THEMES[theme]
    if kind=='drapeaux': items=flag_items(rng)
    elif kind=='qcm': items=qcm_items(rng,theme)
    else: items=trompe_items(rng)
    if kind=='trompe':
        intro_v=tts("Kess se trompe ! Vrai ou faux, à toi de juger !",0.8)
        outro_fn=lambda n,its: tts(f"Kess s'est trompé {sum(not i['ok'] for i in its)} fois sur {n} ! Tu les avais toutes ? Dis-le en commentaire, et abonne-toi !",0.8)
    else:
        intro_v=tts(("Défi drapeaux ! " if kind=='drapeaux' else f"Spécial {label.lower()} ! ")+"Trois secondes par question. Tu en trouves combien ?",0.8)
        outro_fn=lambda n,its: tts("Ton score ? Dis-le en commentaire, et abonne-toi !",0.8)
    NQ,SEGS,T_END,V_OUT=fit(items,kind,intro_v,outro_fn); items=items[:NQ]
    T_OUT=L(V_OUT)+1.0; TOTAL=T_END+T_OUT; N=int(TOTAL*FPS); T_INTRO=SEGS[0]['s']
    BG=bg_layer(ACC); ERR=sum(not i['ok'] for i in items) if kind=='trompe' else 0
    def intro_l():
        def f(im,d):
            card_base(im,d,600,1500)
            d.text(z(540,760),"NOUVEAU DÉFI" if kind=='trompe' else "DÉFI",font=F('Bold',56),fill=ACC,anchor='mm')
            title=label if kind=='trompe' else (f"{NQ} drapeaux" if kind=='drapeaux' else f"Spécial {label.lower()}")
            fo=F('Bold',84 if len(title)>12 else 96); d.text(z(540,905),title,font=fo,fill=INKT,anchor='mm')
            d.text(z(540,1020),f"{NQ} questions · vrai ou faux" if kind=='trompe' else f"{NQ} questions · 3 secondes chacune",font=F('Medium',42),fill=GREY,anchor='mm')
            d.text(z(540,1300),"Repère toutes ses erreurs" if kind=='trompe' else "Tu en trouves combien ?",font=F('Bold',50),fill=INKT,anchor='mm')
        return layer(f)
    def outro_l():
        def f(im,d):
            card_base(im,d,600,1500)
            if kind=='trompe':
                d.text(z(540,760),"BILAN",font=F('Bold',56),fill=ACC,anchor='mm'); d.text(z(540,900),"Kess s'est trompé",font=F('Bold',66),fill=INKT,anchor='mm')
                d.text(z(540,1050),f"{ERR} fois sur {NQ}",font=F('Bold',100),fill=(230,80,80),anchor='mm')
                d.text(z(540,1250),"Tu les avais toutes vues ?",font=F('Bold',50),fill=INKT,anchor='mm'); d.text(z(540,1330),"Dis-le en commentaire",font=F('Medium',42),fill=GREY,anchor='mm')
            else:
                d.text(z(540,760),"C'EST FINI !",font=F('Bold',60),fill=ACC,anchor='mm'); d.text(z(540,930),"Ton score ?",font=F('Bold',100),fill=INKT,anchor='mm')
                d.text(z(540,1060),"Dis-le en commentaire",font=F('Medium',46),fill=GREY,anchor='mm')
                for i,(sc,lb) in enumerate([(f"{NQ}/{NQ}","génie"),(f"{max(1,NQ-2)}-{NQ-1}","solide"),(f"0-{max(0,NQ-3)}","Kess te bat")]):
                    x=240+i*300; d.rounded_rectangle(z(x-125,1180,x+125,1380),36,fill=(244,238,255))
                    d.text(z(x,1250),sc,font=F('Bold',58),fill=V2,anchor='mm'); d.text(z(x,1325),lb,font=F('Medium',30),fill=GREY,anchor='mm')
            d.text(z(540,1440),"Abonne-toi pour le prochain défi !",font=F('Bold',36),fill=V2,anchor='mm')
        return layer(f)
    def qcard(it,reveal):
        def f(im,d):
            card_base(im,d); chip(d,150,580,label,ACC)
            if it['flag']:
                x,y,w,h=290,660,500,300; d.rounded_rectangle(z(x-8,y-8,x+w+8,y+h+8),24,fill=(234,232,240)); draw_flag(d,it['flag'],x,y,w,h)
                d.text(z(540,1025),it['q'],font=F('Bold',46),fill=INKT,anchor='mm')
            else:
                fo=F('Bold',58); ls=wrap(it['q'],fo,760); yy=850-len(ls)*40
                for l in ls: d.text(z(540,yy),l,font=fo,fill=INKT,anchor='mm'); yy+=80
            for i,o in enumerate(it['opts']):
                y0=1100+i*150; st=('ok' if i==it['ans'] else 'dim') if reveal else None
                opt(d,y0,"      "+o,st,125); lc=(214,210,224) if st=='dim' else V2
                d.ellipse(z(180,y0+30,245,y0+95),fill=GD if st=='ok' else lc); d.text(z(212,y0+63),"ABC"[i],font=F('Bold',36),fill='white',anchor='mm')
        return layer(f)
    def fcard(it):
        def f(im,d):
            card_base(im,d,640,1560)
            d.rounded_rectangle(z(150,690,520,750),30,fill=(255,243,200)); d.text(z(335,720),"Le savais-tu ?",font=F('Bold',34),fill=(200,140,0),anchor='mm')
            if it['flag']:
                x,y,w,h=650,690,240,144; d.rounded_rectangle(z(x-6,y-6,x+w+6,y+h+6),16,fill=(234,232,240)); draw_flag(d,it['flag'],x,y,w,h)
            fo=F('Bold',52); yy=900
            for l in wrap(it['fact'],fo,760): d.text(z(160,yy),l,font=fo,fill=INKT); yy+=76
        return layer(f)
    def tcard(it,stage):
        def f(im,d):
            card_base(im,d); chip(d,150,580,label,ACC)
            fo=F('Bold',54); yy=660
            for l in wrap(it['q'],fo,760): d.text(z(150,yy),l,font=fo,fill=INKT); yy+=74
            if stage>=1:
                d.rounded_rectangle(z(150,900,930,1070),40,fill=(255,240,225)); d.polygon(z(820,900,880,900,905,840),fill=(255,240,225))
                d.text(z(200,945),"Kess répond :",font=F('Medium',32),fill=(200,130,70),anchor='lm'); d.text(z(200,1012),it['disp'],font=F('Bold',60),fill=INKT,anchor='lm')
                d.text(z(540,1140),"Il a raison ?",font=F('Bold',46),fill=INKT,anchor='mm'); sv=sf=None
                if stage==2: sv='ok' if it['ok'] else 'dim'; sf='dim' if it['ok'] else 'ok'
                opt(d,1200,"VRAI",sv,125); opt(d,1345,"FAUX",sf,125)
            if stage==2: d.text(z(540,1520),it['expl'],font=F('Bold',46),fill=(66,170,100) if it['ok'] else (230,80,80),anchor='mm')
        return layer(f)
    INTRO,OUTRO=intro_l(),outro_l()
    if kind=='trompe': C=[[tcard(it,s) for s in (0,1,2)] for it in items]; TBY=1505
    else: C=[[qcard(it,False),qcard(it,True),fcard(it) if SEGS[i]['fact'] else None] for i,it in enumerate(items)]; TBY=1575
    n=NQ
    def frame(i):
        t=i/FPS; fr=BG.copy()
        if t<T_INTRO:
            k=back(t/0.5); fr.alpha_composite(INTRO,(0,int((1-k)*900)))
            fr.alpha_composite(POSES['talk'],(340,int(1340+20*math.sin(t*12)))); header(fr,0,n,None,ACC,0); return fr
        if t>=T_END:
            tt=t-T_END; k=back(tt/0.5); fr.alpha_composite(OUTRO,(0,int((1-k)*900)))
            fr.alpha_composite(POSES['lose' if kind=='trompe' else 'point'],(710,int(330+12*math.sin(tt*5)))); header(fr,0,n,None,ACC,1); return fr
        q=max(j for j,s in enumerate(SEGS) if s['s']<=t); S_=SEGS[q]; tt=t-S_['s']; it=items[q]
        if tt<S_['te']:
            k=back(tt/0.45)
            if kind=='trompe':
                st=0 if tt<S_['talk'] else 1; fr.alpha_composite(C[q][st],(int((1-k)*1100),0))
                talking=(0.4<tt<S_['talk']-0.1) or (S_['talk']<=tt<S_['ts']-0.1); show_bar=st==1
            else:
                fr.alpha_composite(C[q][0],(int((1-k)*1100),0)); talking=0.4<tt<S_['ts']-0.1; show_bar=True
            shake=0
            if show_bar and tt>0.45:
                p=max(0,1-(tt-S_['ts'])/TIMER) if tt>=S_['ts'] else 1; timebar(fr,p,TBY)
                if p<0.25: shake=int(4*math.sin(tt*60))
            fr.alpha_composite(POSES['talk' if talking else 'think'],(710+shake,300+int(10*math.sin(tt*(13 if talking else 5)))))
            secs=TIMER if tt<S_['ts'] else max(1,TIMER-int(tt-S_['ts'])); header(fr,q+1,n,secs,ACC,(q+0.5)/n)
        elif tt<S_['fs'] or not S_['fact']:
            rt=tt-S_['te']; good=it['ok'] if kind=='trompe' else True
            fr.alpha_composite(C[q][2 if kind=='trompe' else 1])
            if kind!='trompe': timebar(fr,0,TBY)
            pose=('point' if rt<1 else 'win') if kind!='trompe' else ('win' if good else 'lose')
            fr.alpha_composite(POSES[pose],(710,int(300-30*abs(math.sin(rt*7))*(rt<1 and good))))
            header(fr,q+1,n,0,ACC,(q+1)/n)
        else:
            ft=tt-S_['fs']; k=back(ft/0.45)
            fr.alpha_composite(C[q][1],(int(-k*1100),0)); fr.alpha_composite(C[q][2],(int((1-k)*1100),0))
            talking=0.35<ft<S_['fe']-S_['fs']-0.5
            fr.alpha_composite(POSES['talk' if talking else 'win'],(340+int((1-k)*1100),int(1090+10*math.sin(ft*(12 if talking else 4)))))
            header(fr,q+1,n,None,ACC,(q+1)/n)
        return fr
    # audio
    def tick(f,v): return tone(f,.03,'sine',v,.006)
    def impact(good):
        m=int(.6*SR); tt=np.arange(m)/SR
        boom=np.sin(2*np.pi*np.cumsum(45+160*np.exp(-tt*30))/SR)*np.exp(-tt*6)*.8
        nz=_hp(np.random.default_rng(5).normal(0,1,m),2500)*np.exp(-tt*14)*.25
        fs=(523.3,659.3,784,1046.5) if good else (311.1,370,440)
        return boom+nz+_lp(sum(saw(f,m) for f in fs)*np.exp(-tt*5)*.07,5000)
    voice=np.zeros(int(TOTAL*SR)+SR); fx=np.zeros_like(voice); gate=np.ones_like(voice)
    def put(arr,t,x): s=int(t*SR); e=min(len(arr),s+len(x)); arr[s:e]+=x[:e-s]
    place_voice(voice,0.3,intro_v); place_voice(voice,T_END+0.4,V_OUT); put(fx,0.05,sfx('whoosh')); put(fx,T_END,sfx('whoosh')); put(fx,T_END+0.2,sfx('yay'))
    for q,S_ in enumerate(SEGS):
        s=S_['s']; it=items[q]; put(fx,s,sfx('whoosh')); place_voice(voice,s+0.4,it['vq']); place_voice(voice,s+S_['ra'],it['va'])
        if kind=='trompe': place_voice(voice,s+S_['talk'],it['vk']); put(fx,s+S_['talk'],sfx('whoosh')*.4)
        if S_['fact']: place_voice(voice,s+S_['fs']+0.3,it['vf']); put(fx,s+S_['fs'],sfx('whoosh')*.6)
        tt=0.0
        while tt<TIMER-0.02:
            pr=tt/TIMER; put(fx,s+S_['ts']+tt,tick(2400 if int(tt*5)%2 else 2900,.18+.25*pr)); tt+=0.2 if pr<0.7 else 0.1
        good=it['ok'] if kind=='trompe' else True
        put(fx,s+S_['te'],impact(good))
        if not good: put(fx,s+S_['te']+0.05,sfx('buzz')*.6)
        gate[int((s+S_['ts']-0.05)*SR):int((s+S_['te'])*SR)]=0
    gate=np.convolve(gate,np.ones(int(.12*SR))/(.12*SR),'same')
    bpm,root,prog,lead=MUSIC[rng.randrange(len(MUSIC))]
    mus=pop_music(TOTAL,bpm,root,prog,seed%1000,lead)*gate[:int(TOTAL*SR)]
    act=np.clip(np.convolve((abs(voice)>0.02).astype(float),np.ones(int(.25*SR))/(.25*SR),'same')*3,0,1)[:len(mus)]
    out=mus*(1-0.65*act)+voice[:len(mus)]+fx[:len(mus)]
    wav=out_path.replace('.mp4','.wav'); write_wav(wav,(np.clip(out,-1,1)*32767).astype(np.int16))
    raw=out_path.replace('.mp4','_raw.mp4'); encode(frame,N,wav,raw)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',raw,'-c:v','copy','-af','loudnorm=I=-14:TP=-1.5','-c:a','aac','-b:a','160k','-ar','44100',out_path],check=True)
    os.remove(raw); os.remove(wav)
    return items,NQ,ERR,TOTAL
EMO={'drapeaux':["🌍","🚩","🗺️","🏳️"],'capitales':["🏙️","🗺️","📍","🌆"],'animaux':["🐾","🦁","🐙","🦒"],'sciences':["🔬","🚀","🧪","🪐"],
     'histoire':["🏛️","⏳","📜","👑"],'géographie':["🌋","🗺️","🏔️","🌊"],'trompe':["❓","🤔","😏","🧐"]}
HASHPOOL=["#quizz","#quiztime","#quizchallenge","#culturegenerale","#defi","#challenge","#jeu","#questionreponse",
          "#testtonniveau","#cerveau","#enigme","#trivia","#quizfr","#jeuxdereflexion"]
CREDIT="Voix : SIWIS (licence CC-BY)"
_META={}
def _meta(kind,theme,seed):
    if (kind,theme,seed) not in _META:
        r=random.Random(seed*7+len(theme)); e=r.sample(EMO.get(theme,["🧠","🎯","🏆"]),2)
        _META[(kind,theme,seed)]=(e,"#quiz "+" ".join(r.sample(HASHPOOL,2)))
    return _META[(kind,theme,seed)]
def caption(kind,theme,n,err,seed=0):
    e,tags=_meta(kind,theme,seed)
    if kind=='trompe': head=f"{e[0]} Kess s'est trompé {err} fois sur {n}… tu les as toutes repérées ? Vrai ou faux, dis-le en commentaire 👇"
    elif kind=='drapeaux': head=f"{e[0]} {n} drapeaux, 3 secondes chacun : tu en trouves combien ? Ton score en commentaire 👇"
    else: head=f"{e[0]} Spécial {THEMES[theme][0].lower()} : {n} questions, 3 secondes chacune. Ton score en commentaire 👇"
    return head+"\n"+tags+"\n"+CREDIT
def yt_meta(kind,theme,n,err,seed=0):
    e,tags=_meta(kind,theme,seed)
    if kind=='trompe': title=f"Kess s'est trompé {err} fois sur {n}… tu les vois toutes ? {e[1]}"
    elif kind=='drapeaux': title=f"{n} drapeaux en 3 secondes : combien tu en trouves ? {e[1]}"
    else: title=f"Spécial {THEMES[theme][0].lower()} : {n} questions, combien tu en trouves ? {e[1]}"
    desc=(f"{e[0]} Nouveau défi Kess Quiz !\n\nPenses-tu trouver toutes les bonnes réponses ? Note ton score en commentaire et défie tes amis.\n\n"
          "🏆 Bats Kess si tu peux ! Abonne-toi pour un nouveau défi chaque jour.\n\n"+tags+"\n\n"+CREDIT)
    return title[:100],desc
def pick(rng):
    last=[v['theme'] for v in hist['videos'][-4:]]; lastk=[v['kind'] for v in hist['videos'][-1:]]
    opts=[('drapeaux','drapeaux'),('trompe','trompe')]+[('qcm',t) for t in ('capitales','animaux','sciences','histoire','géographie','actu') if enough(t)]  # il faut assez de questions pour 60 s
    w=[]
    for k,t in opts:
        x=0 if t in last else 1.0
        if k in lastk: x*=0.3
        if k=='qcm': x*=0.6
        w.append(x)
    if sum(w)==0: w=[1]*len(opts)
    return rng.choices(opts,w)[0]
if __name__=='__main__':
    outdir=sys.argv[1]; count=int(sys.argv[2]) if len(sys.argv)>2 else 1
    force=os.environ.get('KQ_FORMAT')  # ex. "qcm:animaux"
    manifest=[]; now=datetime.datetime.now()
    for v in range(count):
        seed=int(now.strftime('%Y%m%d'))*10+v+len(hist['videos']); rng=random.Random(seed)
        kind,theme=(force.split(':') if force else pick(rng))
        name=f"kq_{now.strftime('%Y%m%d')}_{v+1}_{kind}_{theme}.mp4".replace('é','e')
        items,n,err,tot=render(kind,theme,os.path.join(outdir,name),seed)
        hist['used']+= [i['id'] for i in items]; hist['videos'].append(dict(file=name,kind=kind,theme=theme,n=n,date=now.isoformat()[:16],ids=[i['id'] for i in items]))
        manifest.append(dict(file=name,kind=kind,theme=theme,n=n,duration=round(tot,1),caption=caption(kind,theme,n,err,seed),yt_title=yt_meta(kind,theme,n,err,seed)[0],yt_desc=yt_meta(kind,theme,n,err,seed)[1]))
        json.dump(hist,open(HIST,'w'),ensure_ascii=False,indent=1); print(name,round(tot,1),n)
    json.dump(manifest,open(os.path.join(outdir,'manifest.json'),'w'),ensure_ascii=False,indent=1)
