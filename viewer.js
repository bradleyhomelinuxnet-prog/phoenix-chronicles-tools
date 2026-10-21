(function(){
  var stage=document.getElementById('stage');
  if(!stage) return;
  var paper=document.getElementById('paper');
  var W=+paper.dataset.w, H=+paper.dataset.h;
  var scale=1, x=0, y=0, rot=0, base=1;

  var PAGE=location.pathname.split('/').pop();

  // A link can open a plate on a given view: p014.html#redesign (or #text, #engine, #plate).
  // The index grid uses it, so a card showing the redesign opens on the redesign. The view
  // buttons arrive at different times (text loads by script), so each bindSegs() retries
  // until the wanted button exists; a plate without that view just opens as usual.
  // With no #view, a plate opens on the rebuilt version first: its interactive redesign if it
  // has one, else the engine view. Jason's original is the next button along (#plate opens it).
  var WANT=(location.hash.match(/^#(redesign|text|engine|plate)$/)||[])[1], opened=false;
  // On a text plate the "Read text" button shares data-view="redesign" with the transcription
  // pane, so buttons are found by what they say as well as by their view.
  function segButton(view){
    var bs=document.querySelectorAll('.seg button');
    for(var i=0;i<bs.length;i++){
      var t=bs[i].textContent, v=bs[i].dataset.view;
      if(view==='text' ? (v==='text' || /^Read text/.test(t))
       : view==='redesign' ? (v==='redesign' && /redesign|interactive/i.test(t))
       : v===view) return bs[i];
    }
    return null;
  }
  function openFromHash(){
    if(opened) return;
    var b=WANT ? segButton(WANT) : (segButton('redesign') || segButton('engine'));
    if(b){ opened=true; b.click(); }
  }

  // Plates drawn sideways open upright. Any plate you turn remembers its way (per browser).
  var UPRIGHT={'p017.html':90,'p029.html':90,'p030.html':90,'p038.html':90};
  var ROT_KEY='chrono-rot:'+PAGE;
  if(UPRIGHT[PAGE]) rot=UPRIGHT[PAGE];
  try{ var saved=localStorage.getItem(ROT_KEY); if(saved!==null){ saved=parseInt(saved,10); if(saved===0||saved===90||saved===180||saved===270) rot=saved; } }catch(e){}
  function saveRot(){ try{ if(rot===(UPRIGHT[PAGE]||0)) localStorage.removeItem(ROT_KEY); else localStorage.setItem(ROT_KEY,String(rot)); }catch(e){} }

  // Interactive redesigns for plates whose page has no switch of its own.
  // Generated list: tools/wire.py rewrites the REDESIGNS line from the redesign/ folder.
  var REDESIGNS={"p013.html":["chart-i.html","Chart I"],"p014.html":["p014.html","Chart I·b"],"p015.html":["p015.html","Chart I·c"],"p016.html":["p016.html","Chart I·d"],"p017.html":["ie.html","Chart I·e"],"p018.html":["p018.html","Chart II"],"p021.html":["p021.html","Chart III"],"p022.html":["p022.html","Chart III·b"],"p023.html":["p023.html","Chart IV"],"p024.html":["p024.html","Chart V"],"p025.html":["p025.html","Chart V"],"p026.html":["p026.html","Chart V"],"p027.html":["p027.html","Chart VI"],"p028.html":["p028.html","Chart VI"],"p029.html":["vic.html","Chart VI·c"],"p030.html":["vid.html","Chart VI·d"],"p038.html":["p038.html","Chart VIII"],"p039.html":["p039.html","Chart VIII·b"],"p040.html":["p040.html","Chart IX"],"p041.html":["p041.html","Chart IX·b / IX·c"],"p042.html":["p042.html","Chart X, XI, XII"],"p043.html":["p043.html","Chart X·b"],"p044.html":["p044.html","Chart X·c"],"p045.html":["p045.html","Chart XI·b"],"p046.html":["p046.html","Chart XIII–XVI"],"p047.html":["p047.html","Chart XIV·b"],"p048.html":["p048.html","Chart XIV·c"],"p053.html":["p053.html","Chart XVII"],"p054.html":["p054.html","Chart XVII"],"p055.html":["p055.html","Chart XVII"],"p059.html":["p059.html","Chart XVIII"],"p060.html":["p060.html","Chart XIX"],"p061.html":["p061.html","Chart XIX·c"],"p062.html":["p062.html","Chart XIX·d"],"p063.html":["p063.html","Chart XX / XXI"],"p064.html":["p064.html","Chart XX·b"],"p069.html":["p069.html","Chart XXII"],"p070.html":["p070.html","Chart XXI·b"],"p071.html":["p071.html","Chart XXII·c"],"p073.html":["p073.html","Chart XXIII"],"p074.html":["p074.html","Chart XXIII·b"],"p080.html":["p080.html","Chart XXIV"],"p081.html":["p081.html","Chart XXV"],"p082.html":["p082.html","Chart XXVI"],"p083.html":["p083.html","Chart XXVII"],"p084.html":["p084.html","Chart XXVIII"],"p085.html":["p085.html","Chart XXIX"],"p086.html":["p086.html","Chart XXX"],"p087.html":["p087.html","Chart XXXI"],"p088.html":["p088.html","Chart XXXII"],"p089.html":["p089.html","Chart XXXIII"],"p090.html":["p090.html","Chart XXXIV"],"p091.html":["p091.html","Chart XXXV"],"p110.html":["p110.html","Foundation of Time"],"p111.html":["p111.html","Vertical Distances"],"p112.html":["p112.html","Sloping & Horizontal Distances"],"p113.html":["p113.html","Lower Chamber Level"],"p114.html":["p114.html","Phoenix Chronometry I"],"p115.html":["p115.html","Phoenix Chronometry II"],"p116.html":["p116.html","Phoenix Chronometry III"],"p117.html":["p117.html","Phoenix Chronometry IV"],"p118.html":["p118.html","Rejected Cornerstone"]};
  var NUM=parseInt((PAGE.match(/p(\d+)\.html/)||[])[1],10);
  // Generated list: tools/wire.py rewrites the ENGINE line from redesign/data/ (plates drawn by the shared engine).
  var ENGINE=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119];
  function addEngine(wrap){
    if(!wrap || ENGINE.indexOf(NUM)<0 || wrap.querySelector('[data-view="engine"]')) return;
    var seg=wrap.querySelector('.seg');
    if(!seg){ addSeg(wrap,''); seg=wrap.querySelector('.seg'); seg.removeChild(seg.lastChild); }
    var b=document.createElement('button'); b.type='button'; b.dataset.view='engine'; b.textContent='Engine view \u25C8'; seg.appendChild(b);
    var f=document.createElement('iframe'); f.className='frame'; f.title='engine view'; f.loading='lazy'; f.dataset.pane='engine';
    f.src='../redesign/e'+('00'+NUM).slice(-3)+'.html'; f.style.display='none'; wrap.appendChild(f);
    bindSegs();
  }
  function addSeg(wrap,second){
    var seg=document.createElement('div'); seg.className='seg';
    seg.innerHTML='<button type="button" class="on" data-view="plate">Original plate</button><button type="button" data-view="redesign">'+second+'</button>';
    wrap.insertBefore(seg, wrap.firstChild);
  }
  (function wireRedesign(){
    var r=REDESIGNS[PAGE], wrap=document.getElementById('stagewrap');
    if(wrap && wrap.querySelector('.seg')) addEngine(wrap);
    if(!r || !wrap || wrap.querySelector('.seg')) return;
    addSeg(wrap,'Interactive redesign \u2726');
    var f=document.createElement('iframe'); f.className='frame'; f.title='redesign'; f.loading='lazy'; f.src='../redesign/'+r[0];
    wrap.appendChild(f); addEngine(wrap);
    var pn=document.querySelector('.tb-center .pnum');
    if(pn && !pn.querySelector('.serif')){ var s=document.createElement('span'); s.className='serif'; s.style.cssText='color:#ffcf5c;font-size:17px'; s.textContent=r[1]; pn.appendChild(document.createTextNode('\u00a0\u00b7\u00a0')); pn.appendChild(s); }
  })();

  // Text plates: a "Read text" view of the cleaned transcription in text/texts.js
  // (a script, not fetch(), so it also works when the atlas is opened from disk).
  (function wireText(){
    var wrap=document.getElementById('stagewrap');
    if(!wrap || !NUM) return;
    var chart=!!wrap.querySelector('.seg');
    var sc=document.createElement('script'); sc.src='../text/texts.js';
    sc.onload=function(){
      var t=window.CHRONO_TEXT && window.CHRONO_TEXT[NUM];
      if(!t){ addEngine(wrap); return; }
      if(!chart && wrap.querySelector('.seg')) return;
      if(chart){ var seg=wrap.querySelector('.seg'), eb=seg.querySelector('[data-view="engine"]'), tb=document.createElement('button'); tb.type='button'; tb.dataset.view='text'; tb.textContent='Read text \u00b6'; seg.insertBefore(tb,eb); }
      else addSeg(wrap,'Read text \u00b6');
      var pane=document.createElement('div'); pane.className='frame textpane'; if(chart){ pane.dataset.pane='text'; pane.style.display='none'; }
      var lines=t.split('\n'), head=lines.shift(), h2=lines.shift(), html='<div class="tp-in"><div class="tp-k">'+esc(head)+'</div>';
      if(h2) html+='<h2 class="serif">'+esc(h2)+'</h2>';
      var first=true;
      lines.join('\n').split(/\n\s*\n/).forEach(function(par){ par=par.trim(); if(!par) return;
        var t=mark(esc(par).replace(/\n/g,'<br>'));
        if(/^(\*|&gt;|-)\s/.test(par)) html+='<ul class="tp-ul">'+par.split(/\n/).map(function(l){return '<li>'+mark(esc(l.replace(/^(\*|>|-)\s*/,'')))+'</li>';}).join('')+'</ul>';
        else if(/^["“]/.test(par)&&par.length<600) html+='<blockquote>'+t+'</blockquote>';
        else if(par.length<90&&!/[.,;:]$/.test(par)&&!/\d{3,}/.test(par.slice(0,4))) html+='<h3 class="tp-h">'+t+'</h3>';
        else { html+='<p'+(first?' class="tp-first"':'')+'>'+t+'</p>'; first=false; } });
      pane.innerHTML=html+'</div>'; wrap.appendChild(pane);
      bindSegs(); addEngine(wrap);
    };
    document.head.appendChild(sc);
    function esc(x){return x.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
    // dates, Anno Mundi years and pyramid-inch figures stand out from the prose
    function mark(h){return h
      .replace(/\b(\d{1,4}(?:[.,]\d+)?)\s?(BCE|CE|AD|BC|AM|Annus Mundi|Anno Domini)\b/g,'<span class="tp-d">$1 $2</span>')
      .replace(/\b(\d{1,5}(?:\.\d+)?)\s?(P"|P″|P&quot;|Pyramid Inches)/g,'<span class="tp-p">$1 $2</span>')
      .replace(/\[\?\]/g,'<span class="tp-q">[?]</span>');}
  })();

  // Layout fixes: the redesign switch sits on the plate, not under the top bar; on phones
  // the top bar fits the screen and the hint card gives way to the ORIENT buttons.
  (function phoneStyles(){
    var st=document.createElement('style');
    // .seg is placed against #stagewrap; without this it was placed against the page and
    // hid under the sticky top bar, so the "Interactive redesign" switch could not be reached.
    st.textContent='.stagewrap{position:relative}'+
      '.textpane{overflow:auto;-webkit-overflow-scrolling:touch}.textpane .tp-in{max-width:760px;margin:0 auto;padding:84px 30px 70px;color:#dfe6f5;font-size:17px;line-height:1.75}'+
      '.textpane .tp-k{font-family:\'JetBrains Mono\',monospace;font-size:11px;letter-spacing:.3em;color:#7f8db0;text-transform:uppercase}'+
      '.textpane h2{font-size:30px;color:#ffcf5c;margin:.3em 0 .8em;line-height:1.15}.textpane p{margin:0 0 1.05em}'+
    '.textpane .tp-in{font-family:\'Cormorant Garamond\',Georgia,serif;font-size:21px;line-height:1.62;color:#e4e9f4}'+
    '.textpane .tp-in>*{max-width:680px;margin-left:auto;margin-right:auto}'+
    '.textpane .tp-first::first-letter{float:left;font-size:3.4em;line-height:.85;padding:.06em .1em 0 0;color:#ffcf5c;font-weight:700}'+
    '.textpane h2{font-family:\'Cormorant Garamond\',serif;font-weight:700;border-bottom:1px solid #26324f;padding-bottom:.35em}'+
    '.textpane .tp-h{font-family:\'JetBrains Mono\',monospace;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:#4fe3ff;margin:1.8em auto .7em;font-weight:500}'+
    '.textpane blockquote{border-left:3px solid #ffcf5c;margin:1.2em auto;padding:.3em 0 .3em 1.1em;font-style:italic;color:#cfd7e8}'+
    '.textpane .tp-ul{padding-left:1.3em}.textpane .tp-ul li{margin:.35em 0}.textpane .tp-ul li::marker{color:#ffcf5c}'+
    '.textpane .tp-d{font-family:\'JetBrains Mono\',monospace;font-size:.78em;color:#ffcf5c;white-space:nowrap}'+
    '.textpane .tp-p{font-family:\'JetBrains Mono\',monospace;font-size:.78em;color:#7fd8ff;white-space:nowrap}'+
    '.textpane .tp-q{font-family:\'JetBrains Mono\',monospace;font-size:.7em;color:#f08a4b}'+
    '.textpane .tp-k{max-width:680px;margin:0 auto}'+
      '@media(max-width:640px){'+
      '.topbar{gap:8px!important;padding-left:12px!important;padding-right:12px!important}'+
      '.topbar .brand{font-size:17px!important}.topbar .brand small{display:none!important}'+
      '.tb-center .badge{display:none!important}.tb-center .pnum{font-size:12px!important}.tb-center .serif{font-size:14px!important}'+
      '.topbar .navbtn{width:34px!important;height:34px!important}.topbar .navbtn.ghost{width:auto!important;padding:0 9px!important}'+
      '.hintbar{display:none!important}'+
      '.orient{left:12px!important;transform:none!important;max-width:calc(100% - 84px)!important;border-radius:16px!important;padding:6px 8px!important}'+
      '.orient span{display:none}'+
      '.textpane .tp-in{padding:70px 18px 50px!important;font-size:15.5px!important}'+
      '.seg{top:10px!important;max-width:calc(100% - 20px)}.seg button{padding:7px 11px!important;font-size:11.5px!important}'+
      '}';
    document.head.appendChild(st);
  })();

  function fit(){
    var sw=stage.clientWidth-80, sh=stage.clientHeight-80;
    var rw=(rot%180===0)?W:H, rh=(rot%180===0)?H:W;
    base=Math.min(sw/rw, sh/rh);
    scale=base; x=0; y=0; apply();
  }
  function apply(){
    paper.style.width=W+'px'; paper.style.height=H+'px';
    paper.style.transform='translate(-50%,-50%) translate('+x+'px,'+y+'px) scale('+scale+') rotate('+rot+'deg)';
  }
  function zoom(f){ scale=Math.max(base*0.5, Math.min(base*12, scale*f)); apply(); }
  function rotate(quarterTurns){ rot=((rot+90*quarterTurns)%360+360)%360; saveRot(); fit(); }

  stage.addEventListener('wheel',function(e){e.preventDefault();zoom(e.deltaY<0?1.12:0.89);},{passive:false});

  // Drag to pan. A press that starts on a button or link is left alone: capturing the
  // pointer there sent the release to the stage, so the button's click never fired.
  function onControl(t){ return t && t.closest && t.closest('button, a, .controls, .orient, .seg'); }
  // The plate image is not draggable: a native image drag cancelled the pan mid-way.
  var img=paper.querySelector('img');
  if(img){ img.draggable=false; img.addEventListener('dragstart',function(e){e.preventDefault();}); }
  stage.style.touchAction='none';
  var drag=false,px,py;
  stage.addEventListener('pointerdown',function(e){
    if(onControl(e.target) || e.button>0) return;
    e.preventDefault();
    drag=true;px=e.clientX;py=e.clientY;stage.classList.add('grabbing');
    try{stage.setPointerCapture(e.pointerId);}catch(err){}
  });
  stage.addEventListener('pointermove',function(e){if(!drag)return;x+=e.clientX-px;y+=e.clientY-py;px=e.clientX;py=e.clientY;apply();});
  function endDrag(){drag=false;stage.classList.remove('grabbing');}
  stage.addEventListener('pointerup',endDrag);
  stage.addEventListener('pointercancel',endDrag);
  window.addEventListener('resize',fit);

  var acts=document.querySelectorAll('[data-act]');
  for(var i=0;i<acts.length;i++){ acts[i].onclick=(function(b){return function(){
    var a=b.dataset.act;
    if(a==='in')zoom(1.25); else if(a==='out')zoom(0.8);
    else if(a==='rot')rotate(1); else if(a==='fit')fit();
  };})(acts[i]); }

  document.addEventListener('keydown',function(e){
    if(e.ctrlKey||e.metaKey||e.altKey) return;
    var t=e.target; if(t && (t.tagName==='INPUT'||t.tagName==='TEXTAREA'||t.isContentEditable)) return;
    if(e.key==='ArrowLeft'&&window.PREV)location.href=window.PREV;
    else if(e.key==='ArrowRight'&&window.NEXT)location.href=window.NEXT;
    else if(e.key==='+'||e.key==='=')zoom(1.25);
    else if(e.key==='-')zoom(0.8);
    else if(e.key==='r')rotate(1);
    else if(e.key==='R')rotate(-1);
    else if(e.key.toLowerCase()==='f')fit();
    else if(e.key==='Escape')location.href='../index.html';
  });
  fit();

  var bar=document.createElement('div');
  bar.className='orient';
  bar.setAttribute('role','group');
  bar.setAttribute('aria-label','Turn the plate');
  bar.style.cssText='position:absolute;left:50%;bottom:16px;transform:translateX(-50%);z-index:16;display:flex;flex-wrap:wrap;justify-content:center;gap:8px;align-items:center;max-width:calc(100% - 24px);background:#070d18cc;border:1px solid #26324f;border-radius:100px;padding:5px 6px 5px 14px;box-shadow:0 8px 26px -10px #000';
  var lbl=document.createElement('span');
  lbl.textContent='ORIENT';
  lbl.style.cssText='font-family:monospace;font-size:10px;letter-spacing:.18em;color:#7f8db0';
  bar.appendChild(lbl);
  function pill(txt,title,fn){
    var b=document.createElement('button');
    b.type='button';
    b.textContent=txt; b.title=title;
    b.style.cssText='font-family:monospace;font-size:12px;color:#1a1204;background:#ffce44;border:0;border-radius:100px;padding:8px 13px;cursor:pointer;font-weight:700;box-shadow:0 0 16px #ffd15c55;touch-action:manipulation';
    b.onclick=fn; bar.appendChild(b);
  }
  pill('Rotate L','Turn a quarter left (Shift+R)',function(){rotate(-1);});
  pill('Rotate R','Turn a quarter right (R)',function(){rotate(1);});
  pill('Flip 180','Turn upside down',function(){rotate(2);});
  stage.appendChild(bar);

  // Button order: the rebuilt views first, then Jason's original, then the text.
  function rank(b){ var v=b.dataset.view;
    return v==='redesign'&&/redesign|interactive/i.test(b.textContent)?0 : v==='engine'?1 : v==='plate'?2 : 3; }
  function orderSegs(){
    var seg=document.querySelector('.seg'); if(!seg) return;
    [].slice.call(seg.children).sort(function(a,b){return rank(a)-rank(b);}).forEach(function(b){seg.appendChild(b);});
  }
  function bindSegs(){
    orderSegs();
    var segs=document.querySelectorAll('.seg button');
    var wrap=document.getElementById('stagewrap');
    for(var j=0;j<segs.length;j++){ segs[j].onclick=(function(btn){return function(){
      for(var k=0;k<segs.length;k++)segs[k].classList.remove('on');
      btn.classList.add('on');
      var v=btn.dataset.view, fr=wrap.querySelectorAll('.frame');
      for(var m=0;m<fr.length;m++) fr[m].style.display=((fr[m].dataset.pane||'redesign')===v)?'':'none';
      if(v!=='plate')wrap.classList.add('redesign');
      else { wrap.classList.remove('redesign'); setTimeout(fit,30); }
    };})(segs[j]); }
    var fr=document.querySelectorAll('#stagewrap iframe');
    for(var n=0;n<fr.length;n++) linksToTop(fr[n]);
    openFromHash();
  }
  // The redesign and engine pages are also opened on their own, so their links ("← Atlas")
  // are plain relative links -- inside the frame they opened the atlas in the frame, a page
  // within a page. Send every link that leaves the page to the whole window; in-page #links
  // and links that already pick a target are left alone.
  function linksToTop(f){
    if(f.dataset.toTop) return; f.dataset.toTop='1';
    function fix(){ try{
      var a=f.contentDocument.querySelectorAll('a[href]');
      for(var i=0;i<a.length;i++){ var h=a[i].getAttribute('href'); if(!a[i].target && h.charAt(0)!=='#') a[i].target='_top'; }
    }catch(e){} }
    f.addEventListener('load',fix);
    if(f.contentDocument && f.contentDocument.readyState==='complete') fix();
  }
  bindSegs();
})();
