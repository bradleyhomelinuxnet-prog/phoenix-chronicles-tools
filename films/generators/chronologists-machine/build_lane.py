import json
d=json.load(open('/home/claude/cs/m12.json'))
clips={1:'7b96b61f',2:'3bb91363',3:'d11132fe',4:'f6474698',5:'1cc817ae',6:'0c4e4283',7:'8786f10c',8:'35e96632',9:'93aebf4e',10:'837075f1',11:'37c527a2',12:'5ffe62eb'}
meta={ # date label, sortYear, place, camera
1:('5239 BC',-5239,'the sky over the first sea','CLIMB'),
2:('4309 BC',-4309,'the ring of standing stones','SIDE-RL'),
3:('3895 BC',-3895,'the gate of Eden','FOLLOW'),
4:('3439 BC',-3439,'the line of light','SIDE-LR'),
5:('2239 BC',-2239,'the field of luminous dots','FRONT'),
6:('2239 BC',-2239,'the stone plain','FOLLOW'),
7:('2239 BC',-2239,'the suspended sea','FRONT'),
8:('2239 BC',-2239,'the stone plain, after','FOLLOW'),
9:('1687 BC',-1687,'under the darkened sun','FRONT'),
10:('583 BC',-583,'the Halys river, Anatolia','FRONT'),
11:('1902 AD',1902,'the ring of standing stones','SIDE-LR'),
12:('2040 AD',2040,'the lit coastline','DESCEND')}
glyph={'FRONT':('⇩','walking toward you'),'FOLLOW':('⇧','walking away from you'),'SIDE-LR':('⇨','left to right'),'SIDE-RL':('⇦','right to left'),'CLIMB':('⬈','climbing toward you'),'DESCEND':('⬊','descending below you')}
fact={ # quick facts, trimmed for the 4.4 s window — arithmetic kept exact
1:'5239 − 3895 = 1,344. From 5239 BC to 2106 AD is 7,344 years: 5239 + 2106 − 1.',
2:'5239 − 4309 = 930, the years of Adam\'s life in Genesis 5:5.',
3:'3895 BC is Anno Mundi 1, and AD = AM − 3894. Ussher says 4004 BC; the Hebrew calendar, 3761.',
4:'2239 − 792 = 1447 BC, the early Exodus. 2239 + 1200 = 3439 BC. Both struck from AM 1656.',
5:'3895 − 1656 = 2239 BC. 2239 − 1656 = 583 BC. 1,656 = 138 × 12.',
6:'Genesis 7:11–12: forty days of rain. AM 1656 = 138 × 12, the twelfth Phoenix.',
7:'AM 1656 is one of only 43 years in six thousand that sit on a multiple of 138.',
8:'Genesis 8:14: the earth was dry 370 days after the rain began.',
9:'AM 2208 = 138 × 16. 2239 − 1687 = 552 = 138 × 4: the second link of the flood chain.',
10:'AM 3312 = 138 × 24. Herodotus I.74: day became night mid-battle. Astronomers say 28 May 585 BC.',
11:'AM 5796 = 138 × 42. 8 May 1902: Mont Pelée destroys Saint-Pierre. 1902 + 138 = 2040.',
12:'1902 + 138 = 2040 = AM 5934 = 138 × 43. The Codex: "as early as 2039, as late as 2046."'}
st=[]
for k in range(1,13):
    x=d[str(k)]; date,sy,place,cam=meta[k]
    nIn=2.4; nOut=nIn+x['durN']; rIn=max(8.6,nOut+0.35); rOut=rIn+x['durR']
    if rOut>13.9: rIn=max(nOut+0.35,13.9-x['durR']); rOut=rIn+x['durR']
    st.append(dict(id=f'M{k:02d}',k=k,lane='MACHINE',camera=cam,cameraGlyph=glyph[cam][0],cameraWalk=glyph[cam][1],
      when=date,date=date,sortYear=sy,place=place,title=x['TITLE'],claim=x['CLAIM'],anchor=x['FACT'],fact=fact[k],
      check=x['CHECK'],setting='',hook='',natori=x['NATORI'],rogue=x['ROGUE'],score='',sfx=[],mirror=13-k,
      promptA='',promptB='',promptC='',ending='',index=k-1,clip=clips[k],
      voice=dict(nIn=round(nIn,2),nOut=round(nOut,2),rIn=round(rIn,2),rOut=round(rOut,2))))
    print(k, st[-1]['voice'], len(fact[k]))
json.dump({'meta':{'title':'ERE WE WERE','reel':'The Chronologist\'s Machine','built':'2026-09-29','negative':'','secondsPerStation':15},
  'lanes':[{'lane':'MACHINE','subtitle':'twelve fires, in the order the chart keeps them','stations':st}]},
  open('/home/claude/rem-machine/src/data/stations.json','w'),ensure_ascii=False,indent=1)
