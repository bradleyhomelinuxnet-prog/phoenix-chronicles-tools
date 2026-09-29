import glob, json, os
from faster_whisper import WhisperModel
out=json.load(open('transcripts.json'))
files = sorted(glob.glob('/home/claude/src/*.mp4')) + sorted(glob.glob('/mnt/user-data/uploads/PlanetWalker/hf_*.mp4'))
todo=[]; seen=set(out)
for f in files:
    k=os.path.basename(f)
    if k not in seen: todo.append(f); seen.add(k)
print('todo',len(todo),flush=True)
m = WhisperModel('base.en', device='cpu', compute_type='int8')
for f in todo:
    k=os.path.basename(f)
    segs,_ = m.transcribe(f, language='en', vad_filter=True, beam_size=1)
    out[k]=[{'s':round(s.start,2),'e':round(s.end,2),'t':s.text.strip()} for s in segs]
    json.dump(out,open('transcripts.json','w'),indent=0)
    print('ok',k[:26],len(out[k]),flush=True)
print('ALL',len(out))
