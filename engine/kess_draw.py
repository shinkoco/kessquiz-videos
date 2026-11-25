# Dessin de Kess (mascotte)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P='/usr/share/fonts/truetype/google-fonts/Poppins-'; S=2
F=lambda w,s:ImageFont.truetype(P+w+'.ttf',int(s*S))
def z(*a): return [int(v*S) for v in a]
INK=(30,30,40)
def eyes(d,cx,cy,s,mood,white=True,big=22):
    for ex in(-34,34):
        x=cx+ex*s
        if mood=='happy': d.arc(z(x-18*s,cy-14*s,x+18*s,cy+14*s),200,340,fill=INK,width=int(6*s*S)); continue
        if white: d.ellipse(z(x-big*s,cy-big*s,x+big*s,cy+big*s),fill='white')
        py=-6 if mood=='think' else 0
        d.ellipse(z(x-9*s,cy-9*s+py*s,x+9*s,cy+9*s+py*s),fill=INK); d.ellipse(z(x-3*s,cy-7*s+py*s,x+3*s,cy-1*s+py*s),fill='white')
def mouth(d,cx,cy,s,mood,col):
    if mood=='happy': d.chord(z(cx-28*s,cy-14*s,cx+28*s,cy+22*s),0,180,fill=col)
    elif mood=='sad': d.arc(z(cx-20*s,cy,cx+20*s,cy+24*s),200,340,fill=col,width=int(6*s*S))
    else: d.ellipse(z(cx-8*s,cy-2*s,cx+8*s,cy+14*s),fill=col)
def body(d,cx,cy,s,c,o=None,fat=1.0,hook=55):
    bw=int(62*fat)
    if o: d.arc(z(cx-88*s,cy-178*s,cx+88*s,cy-2*s),185,80,fill=o,width=int((hook+14)*s*S))
    d.arc(z(cx-85*s,cy-175*s,cx+85*s,cy-5*s),185,80,fill=c,width=int(hook*s*S))
    if o: d.rounded_rectangle(z(cx-bw*s-7*s,cy-47*s,cx+bw*s+7*s,cy+77*s),int(55*s),fill=o)
    d.rounded_rectangle(z(cx-bw*s,cy-40*s,cx+bw*s,cy+70*s),int(50*s),fill=c)
    if o: d.ellipse(z(cx-33*s,cy+88*s,cx+33*s,cy+154*s),fill=o)
    d.ellipse(z(cx-26*s,cy+95*s,cx+26*s,cy+147*s),fill=c)
def kessA(d,cx,cy,s,mood):
    body(d,cx,cy,s,(255,95,140)); eyes(d,cx,cy+2*s,s,mood,big=20); mouth(d,cx,cy+36*s,s,mood,(130,30,60))
def kessB(d,cx,cy,s,mood):
    c=(255,110,150)
    for sx in(-1,1): d.line(z(cx+sx*70*s,cy+20*s,cx+sx*100*s,cy-5*s),fill=c,width=int(14*s*S)); d.ellipse(z(cx+sx*100*s-11*s,cy-16*s,cx+sx*100*s+11*s,cy+6*s),fill=c)
    body(d,cx,cy,s,c,fat=1.25,hook=62)
    d.ellipse(z(cx-55*s,cy-30*s,cx-25*s,cy-12*s),fill=(255,175,200)); d.arc(z(cx-75*s,cy-160*s,cx-20*s,cy-110*s),200,290,fill=(255,175,200),width=int(10*s*S))
    eyes(d,cx,cy+2*s,s,mood,big=24); mouth(d,cx,cy+38*s,s,mood,(130,30,60))
    d.ellipse(z(cx-68*s,cy+20*s,cx-46*s,cy+34*s),fill=(255,160,185)); d.ellipse(z(cx+46*s,cy+20*s,cx+68*s,cy+34*s),fill=(255,160,185))
def kessC(d,cx,cy,s,mood):
    o=(40,20,90); body(d,cx,cy,s,(110,225,150),o=o)
    d.chord(z(cx-70*s,cy-205*s,cx+40*s,cy-125*s),180,360,fill=(255,200,40)); d.rounded_rectangle(z(cx+15*s,cy-170*s,cx+90*s,cy-155*s),int(8*s),fill=(230,170,20))
    eyes(d,cx,cy+2*s,s,mood); mouth(d,cx,cy+36*s,s,mood,o)

C=(255,110,150)
def arm(d,x0,y0,x1,y1,s):
    d.line(z(x0,y0,x1,y1),fill=C,width=int(15*s*S),joint='curve'); d.ellipse(z(x1-12*s,y1-12*s,x1+12*s,y1+12*s),fill=C)
def kess(d,cx,cy,s,mood,arms):
    for (a,b) in arms: arm(d,cx+a[0]*s,cy+a[1]*s,cx+b[0]*s,cy+b[1]*s,s)
    body(d,cx,cy,s,C,fat=1.25,hook=62)
    d.arc(z(cx-75*s,cy-160*s,cx-20*s,cy-110*s),200,290,fill=(255,175,200),width=int(10*s*S))
    eyes(d,cx,cy+2*s,s,mood,big=24); mouth(d,cx,cy+38*s,s,mood,(130,30,60))
    d.ellipse(z(cx-68*s,cy+20*s,cx-46*s,cy+34*s),fill=(255,160,185)); d.ellipse(z(cx+46*s,cy+20*s,cx+68*s,cy+34*s),fill=(255,160,185))
