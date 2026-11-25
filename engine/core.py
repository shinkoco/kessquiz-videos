import math, subprocess, wave, numpy as np
import os
DIR=os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
exec(open(os.path.join(DIR,'kess_draw.py')).read())   # S, z, F, kess, body, eyes...
from PIL import Image, ImageDraw
W,H,FPS=1080,1920,30
V1=(74,18,168); V2=(132,58,245); G=(134,229,139); GD=(98,190,104); RED=(255,105,105); REDD=(205,70,70); INKT=(40,40,52); GREY=(176,172,190)
def layer(fn):
    im=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); d=ImageDraw.Draw(im); fn(im,d)
    return im.resize((W,H),Image.LANCZOS)
def bg_layer(accent):
    def f(im,d):
        d.rectangle(z(0,0,1080,1920),fill=V2); d.rectangle(z(0,0,1080,700),fill=V1); d.ellipse(z(-500,520,1580,1000),fill=V1)
        for x in range(0,1080,90):
            for y in range(40,900,90): d.line(z(x,y,x+10,y+10),fill=(86,30,182),width=S*2)
        d.rounded_rectangle(z(330,1880,750,1890),5,fill=(110,40,220))
    return layer(f)
def soft(im,box,r):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle(z(box[0],box[1]+30,box[2],box[3]+30),int(r*S),fill=70)
    from PIL import ImageFilter
    sh=Image.new('RGBA',im.size,(40,6,110,0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(40*S))); im.alpha_composite(sh)
def card_base(im,d,top=540,bot=1680):
    d.rounded_rectangle(z(170,bot-20,910,bot+60),40,fill=(152,100,250)); d.rounded_rectangle(z(130,bot-20,950,bot+32),40,fill=(196,150,255))
    soft(im,[90,top,990,bot],48); d.rounded_rectangle(z(90,top,990,bot),48,fill='white')
def chip(d,x,y,txt,accent):
    w=F('Medium',30).getlength(txt)/S
    d.rounded_rectangle(z(x,y,x+w+40,y+50),25,fill=tuple(min(255,c+int((255-c)*.8)) for c in accent)); d.text(z(x+20,y+25),txt,font=F('Medium',30),fill=accent,anchor='lm')
def opt(d,y,txt,state=None,h=120):
    if state=='ok': d.rounded_rectangle(z(150,y+10,930,y+h+10),40,fill=GD); d.rounded_rectangle(z(150,y,930,y+h),40,fill=G); c='white'
    elif state=='ko': d.rounded_rectangle(z(150,y+10,930,y+h+10),40,fill=REDD); d.rounded_rectangle(z(150,y,930,y+h),40,fill=RED); c='white'
    elif state=='dim': d.rounded_rectangle(z(150,y,930,y+h),40,fill=(246,245,250)); c=(190,186,200)
    else: d.rounded_rectangle(z(150,y,930,y+h),40,outline=(234,232,240),width=3*S,fill='white'); c=INKT
    d.text(z(212,y+h/2),txt,font=F('Bold',42),fill=c,anchor='lm')
    if state=='ok': d.line(z(850,y+h/2+2,872,y+h/2+24,905,y+h/2-20),fill='white',width=8*S,joint='curve')
def sprite(mood,arms,scale=0.8):
    im=Image.new('RGBA',(400*S,460*S),(0,0,0,0)); d=ImageDraw.Draw(im); kess(d,200,270,scale,mood,arms)
    return im.resize((400,460),Image.LANCZOS)
POSES={'think':sprite('think',[((-72,15),(-115,-60)),((72,20),(100,60))]),
       'point':sprite('happy',[((72,20),(100,60)),((-72,10),(-150,10))]),
       'talk':sprite('front',[((-72,20),(-110,40)),((72,10),(115,-40))]),
       'win':sprite('happy',[((-72,10),(-120,-70)),((72,10),(120,-70))]),
       'lose':sprite('sad',[((-72,25),(-90,85)),((72,25),(90,85))])}
def header(fr,n,total,secs,accent,prog):
    d=ImageDraw.Draw(fr)
    d.text((540,222),f"{n:02d} / {total:02d}" if n else "KESS QUIZ",font=ImageFont.truetype(P+'Bold.ttf',44),fill='white',anchor='mm')
    d.rounded_rectangle((90,390,740,418),14,fill=(44,10,100)); d.rounded_rectangle((90,390,90+max(28,int(650*prog)),418),14,fill=accent)
    if secs is not None:
        hot=secs<=1
        d.rounded_rectangle((760,170,1000,272),51,fill=(255,90,90) if hot else V2)
        d.ellipse((780,186,850,256),fill=(255,110,80)); d.ellipse((789,195,841,247),fill='white')
        d.text((925,221),f"00:0{secs}",font=ImageFont.truetype(P+'Bold.ttf',46),fill='white',anchor='mm')
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def back(t):
    t=max(0,min(1,t)); c=1.7; return 1+(c+1)*(t-1)**3+c*(t-1)**2
# ---------------- audio ----------------
SR=44100
def env(n,a=0.005,r=0.2):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/r)
def tone(f,dur,kind='tri',vol=.3,r=.25):
    n=int(dur*SR); t=np.arange(n)/SR
    w=2/np.pi*np.arcsin(np.sin(2*np.pi*f*t)) if kind=='tri' else np.sin(2*np.pi*f*t)
    return w*env(n,r=r)*vol
def music(dur,root,bpm,prog,seed):
    rng=np.random.default_rng(seed); out=np.zeros(int(dur*SR)+SR); beat=60/bpm; step=beat/2
    scale=[0,2,4,7,9,12]
    i=0; t=0.0
    while t<dur:
        bar=int(t/(beat*4))%len(prog); ch=prog[bar]
        notes=[root*2**((ch+k)/12) for k in (0,4,7,12)]
        f=notes[i%4] if rng.random()>.25 else root*2**((ch+rng.choice(scale)+12)/12)
        s=int(t*SR); x=tone(f*2,step*1.6,'tri',.07,.18); out[s:s+len(x)]+=x
        if i%8==0: x=tone(root*2**(ch/12)/2,beat*3.5,'sine',.12,.9); out[s:s+len(x)]+=x
        if i%4==2: n=int(.04*SR); out[s:s+n]+=rng.normal(0,.03,n)*np.exp(-np.arange(n)/300)
        i+=1; t+=step
    return out[:int(dur*SR)]
def sfx(kind):
    if kind=='tick': return tone(1800,.05,'sine',.25,.012)
    if kind=='ding': return tone(1318,.6,'sine',.3,.25)+tone(1760,.6,'sine',.2,.3)
    if kind=='buzz':
        n=int(.35*SR); t=np.arange(n)/SR; return np.sign(np.sin(2*np.pi*110*t))*.15*np.minimum(1,(.35-t)*20)
    if kind=='whoosh':
        n=int(.3*SR); x=np.random.default_rng(1).normal(0,1,n); x=np.convolve(x,np.ones(40)/40,'same'); return x*np.sin(np.linspace(0,np.pi,n))*.25
    if kind=='yay': return sum(tone(f,.25,'tri',.12,.12) for f in (784,988,1175))
def mix(base,events):
    for t,k in events:
        x=sfx(k); s=int(t*SR); e=min(len(base),s+len(x)); base[s:e]+=x[:e-s]
    base=np.clip(base,-1,1); return (base*32767).astype(np.int16)
def write_wav(path,a):
    with wave.open(path,'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
def encode(frames_gen,nframes,wav,out):
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',wav,
        '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',out],stdin=subprocess.PIPE)
    for i in range(nframes): p.stdin.write(frames_gen(i).convert('RGB').tobytes())
    p.stdin.close(); p.wait()

# ---------- v2 : horloge + musique moderne ----------
from scipy.signal import lfilter, butter
_CLK={}
def clock_icon(sec):
    if sec in _CLK: return _CLK[sec]
    s=4; im=Image.new('RGBA',(90*s,90*s),(0,0,0,0)); d=ImageDraw.Draw(im)
    c=45*s; R=34*s
    d.rounded_rectangle((c-9*s,2*s,c+9*s,12*s),3*s,fill=(255,110,80))                     # bouton haut
    d.line((c+24*s,14*s,c+31*s,8*s),fill=(255,110,80),width=6*s)                          # bouton côté
    d.ellipse((c-R,c-R+6*s,c+R,c+R+6*s),fill=(255,110,80)); d.ellipse((c-R+7*s,c-R+13*s,c+R-7*s,c+R-1*s),fill='white')
    cy=c+6*s
    for k in range(12):
        a=k*math.pi/6; r1=22*s if k%3 else 19*s
        d.line((c+r1*math.sin(a),cy-r1*math.cos(a),c+24*s*math.sin(a),cy-24*s*math.cos(a)),fill=(200,196,215),width=2*s)
    a=(4-sec)/4*2*math.pi*0.75
    d.line((c,cy,c+18*s*math.sin(a),cy-18*s*math.cos(a)),fill=(255,90,90),width=4*s)
    d.line((c,cy,c,cy-12*s),fill=(60,60,80),width=4*s); d.ellipse((c-4*s,cy-4*s,c+4*s,cy+4*s),fill=(60,60,80))
    _CLK[sec]=im.resize((90,90),Image.LANCZOS); return _CLK[sec]
def header(fr,n,total,secs,accent,prog):
    d=ImageDraw.Draw(fr)
    d.text((540,222),f"{n:02d} / {total:02d}" if n else "KESS QUIZ",font=ImageFont.truetype(P+'Bold.ttf',44),fill='white',anchor='mm')
    d.rounded_rectangle((90,390,740,418),14,fill=(44,10,100)); d.rounded_rectangle((90,390,90+max(28,int(650*prog)),418),14,fill=accent)
    if secs is not None:
        d.rounded_rectangle((760,170,1000,272),51,fill=(255,90,90) if secs<=1 else V2)
        fr.alpha_composite(clock_icon(secs),(770,170))
        d.text((928,221),f"00:0{secs}",font=ImageFont.truetype(P+'Bold.ttf',46),fill='white',anchor='mm')
def _lp(x,fc): b,a=butter(2,fc/(SR/2)); return lfilter(b,a,x)
def _hp(x,fc): b,a=butter(2,fc/(SR/2),'high'); return lfilter(b,a,x)
def saw(f,n): t=np.arange(n)/SR; return 2*((f*t)%1)-1
def pop_music(dur,bpm,root,prog,seed,lead_pat):
    rng=np.random.default_rng(seed); n=int(dur*SR)+SR*2; beat=60/bpm
    drums=np.zeros(n); syn=np.zeros(n); side=np.ones(n)
    # kick
    kn=int(.28*SR); kt=np.arange(kn)/SR; kick=np.sin(2*np.pi*np.cumsum(50+110*np.exp(-kt*35))/SR)*np.exp(-kt*9)*.9
    cn=int(.18*SR); clap=_hp(rng.normal(0,1,cn),900)*np.exp(-np.arange(cn)/SR*22)*.35
    hn=int(.05*SR); hat=_hp(rng.normal(0,1,hn),7000)*np.exp(-np.arange(hn)/SR*80)*.18
    nb=int(dur/beat)+2
    for b in range(nb):
        s=int(b*beat*SR)
        if s+kn<n: drums[s:s+kn]+=kick; side[s:s+int(.22*SR)]=np.minimum(side[s:s+int(.22*SR)],1-.6*np.exp(-np.arange(int(.22*SR))/SR*14))
        if b%2==1 and s+cn<n: drums[s:s+cn]+=clap
        for h in (0.5,0.75) if b%4==3 else (0.5,):
            hs=int((b+h)*beat*SR)
            if hs+hn<n: drums[hs:hs+hn]+=hat
    bars=int(dur/(beat*4))+2
    for br in range(bars):
        ch=prog[br%len(prog)]; base=root*2**(ch/12)
        for b in range(4):
            s=int((br*4+b+0.5)*beat*SR); ln=int(beat*0.45*SR)
            if s+ln>=n: continue
            e=np.exp(-np.arange(ln)/SR*6)
            bass=(saw(base/2,ln)*.5+np.sin(2*np.pi*base/2*np.arange(ln)/SR))*e*.25
            syn[s:s+ln]+=bass
            stab=sum(saw(base*2**(k/12)*m,ln) for k in (0,4,7) for m in (1,1.006))*e*.035
            syn[s:s+ln]+=stab
        for j,step in enumerate(lead_pat):
            if step is None: continue
            s=int((br*4+j*0.5)*beat*SR); ln=int(beat*0.4*SR)
            if s+ln>=n: continue
            f=root*2*2**((ch+step)/12); t=np.arange(ln)/SR
            syn[s:s+ln]+=np.sign(np.sin(2*np.pi*f*t))*np.exp(-t*9)*.045
    syn=_lp(syn,4200)*side
    out=(drums+syn)[:int(dur*SR)]
    fade=int(1.2*SR); out[-fade:]*=np.linspace(1,0,fade); out[:int(.05*SR)]*=np.linspace(0,1,int(.05*SR))
    return out*.6

_PILL={}
def pill(hot):
    if hot in _PILL: return _PILL[hot]
    im=Image.new('RGBA',(320*S,124*S),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,320*S-1,124*S-1),62*S,fill=(255,90,90) if hot else V2); _PILL[hot]=im.resize((320,124),Image.LANCZOS); return _PILL[hot]
_AV=None
def mini_avatar():
    global _AV
    if _AV is None:
        im=Image.new('RGBA',(124*S*4,124*S*4),(0,0,0,0)); d=ImageDraw.Draw(im); s4=S*4
        d.ellipse((0,0,124*s4-1,124*s4-1),fill=(132,58,245)); d.ellipse((6*s4,6*s4,118*s4,118*s4),fill=(244,238,255))
        sp=sprite('think',[],0.8).resize((124*s4//2*2,int(124*s4*460/400)),Image.LANCZOS)
        _AV=im.resize((124,124),Image.LANCZOS)
        k=POSES_HEAD
        _AV.alpha_composite(k,(0,0))
    return _AV
def _head():
    im=Image.new('RGBA',(600*S,600*S),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse(z(0,0,599,599),fill=(132,58,245)); d.ellipse(z(16,16,584,584),fill=(244,238,255))
    kess(d,300,316,1.5,'think',[])
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse((0,0)+im.size,fill=255); im.putalpha(m)
    return im.resize((124,124),Image.LANCZOS)
HEAD=_head()
def header(fr,n,total,secs,accent,prog):
    d=ImageDraw.Draw(fr)
    fr.alpha_composite(HEAD,(80,160))
    d.text((222,200),"KESS QUIZ",font=ImageFont.truetype(P+'Bold.ttf',34),fill='white',anchor='lm')
    d.text((222,244),f"Question {n} / {total}" if n else "Le défi du jour",font=ImageFont.truetype(P+'Medium.ttf',30),fill=(200,185,250),anchor='lm')
    d.rounded_rectangle((90,390,740,418),14,fill=(44,10,100)); d.rounded_rectangle((90,390,90+max(28,int(650*prog)),418),14,fill=accent)
    if secs is not None:
        fr.alpha_composite(pill(secs<=1),(670,160))
        fr.alpha_composite(clock_icon(secs),(692,175))
        d.text((878,222),f"0:0{secs}",font=ImageFont.truetype(P+'Bold.ttf',52),fill='white',anchor='mm')

# ---------- voix Siwis ----------
import subprocess as _sp, os as _os, hashlib as _hashlib
from scipy.signal import resample_poly
def tts(text,speed=0.9):
    key=_hashlib.md5((text+str(speed)).encode()).hexdigest()[:12]; p=f'/tmp/kq_voice_cache_{key}.wav'
    if not _os.path.exists(p):
        _sp.run(['python3','-m','piper','-m',os.environ.get('KQ_VOICE','/tmp/voices/fr.onnx'),'--length-scale',str(speed),'-f',p],input=text.encode(),capture_output=True)
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),np.int16)/32767; sr=w.getframerate()
    a=resample_poly(a,SR,sr); return a/ (abs(a).max()+1e-9)*0.85
def place_voice(track,t,a): s=int(t*SR); e=min(len(track),s+len(a)); track[s:e]+=a[:e-s]
def final_mix(music_arr,voice,events):
    act=np.convolve((abs(voice)>0.02).astype(float),np.ones(int(.25*SR))/(.25*SR),'same'); act=np.clip(act*3,0,1)
    m=music_arr*(1-0.7*act)
    return mix(m+voice,events)
