import React from 'react';
import {
	AbsoluteFill,
	Audio,
	Easing,
	OffthreadVideo,
	Sequence,
	interpolate,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';
import type {Station} from './data';
import {annusMundi, fmtYear} from './data';
import {bedFor, clipFor, natoriFor, rogueFor, scoreFor} from './media';
import {MONO, SERIF} from './fonts';
import {CLOCK, LANE_COLOR, T} from './theme';
import {WalkField} from './WalkField';

type Props = {
	station: Station;
	prev: Station; // the station walked from — its year is where the counter starts rolling
	laneStations: Station[];
	first: Station; // station 01 of the lane — station 19 returns to its frame
	lap?: number;
};

const Caption: React.FC<{who: 'NATORI' | 'ROGUE'; text: string; tIn: number; tOut: number; color: string}> = ({who, text, tIn, tOut, color}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	if (t < tIn || t > tOut + 0.7) return null;
	const words = text.split(' ');
	const revealEnd = tIn + (tOut - tIn) * 0.86;
	const shown = Math.min(words.length, Math.floor(interpolate(t, [tIn, revealEnd], [1, words.length + 0.99], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})));
	const opacity = interpolate(t, [tIn, tIn + 0.25, tOut + 0.2, tOut + 0.7], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<div style={{position: 'absolute', left: 0, right: 0, bottom: 210, display: 'flex', justifyContent: 'center', opacity}}>
			<div style={{maxWidth: 1320, display: 'grid', gridTemplateColumns: '120px 1fr', gap: 18, alignItems: 'baseline'}}>
				<div style={{fontFamily: MONO, fontSize: 18, letterSpacing: '0.22em', color, textAlign: 'right', paddingTop: 10}}>{who}</div>
				<div style={{fontFamily: SERIF, fontSize: 44, lineHeight: 1.22, color: T.bone, textShadow: '0 2px 18px rgba(0,0,0,.85)'}}>
					{words.map((w, i) => (
						<span key={i} style={{opacity: i < shown ? 1 : 0, transition: 'none'}}>
							{w}{' '}
						</span>
					))}
				</div>
			</div>
		</div>
	);
};

export const StationScene: React.FC<Props> = ({station, prev, laneStations, first, lap = 1}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const color = LANE_COLOR[station.lane] ?? T.ice;

	const clip = clipFor(station.id);
	const bed = bedFor(station.id);
	const nat = natoriFor(station.id);
	const rog = rogueFor(station.id);
	const score = scoreFor(station.id, station.lane);
	const hasVoice = Boolean(bed || nat || rog);

	// rolling counter: previous year → this year across the hook (0 → 1.9 s)
	const rolled = interpolate(t, [0, CLOCK.hook], [prev.sortYear, station.sortYear], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: Easing.out(Easing.cubic),
	});
	const dateLabel = t >= CLOCK.hook ? station.date.split(' · ')[0] : fmtYear(rolled);
	const am = annusMundi(t >= CLOCK.hook ? station.sortYear : rolled);

	const fadeIn = interpolate(frame, [0, 6], [0, 1], {extrapolateRight: 'clamp'});
	const n = laneStations.length; // lane length — 19 for the three Reel IV lanes, any count for an adapted show
	const isLast = station.k === n;
	const exitP = interpolate(t, [CLOCK.exit, CLOCK.out], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const titleIn = interpolate(t, [CLOCK.hook, CLOCK.hook + 0.5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const titleY = interpolate(t, [CLOCK.hook, CLOCK.hook + 0.6], [18, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.quad)});
	const checkIn = interpolate(t, [9.0, 9.5, CLOCK.speechDone, CLOCK.exit], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	// layer 9 — QUICK FACT: rises during Natori's tail, holds through the inter-speaker silence, clears before the check line lands at 9.0
	const factIn = interpolate(t, [CLOCK.fact.in, CLOCK.fact.in + 0.4, CLOCK.fact.out - 0.4, CLOCK.fact.out], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const factY = interpolate(t, [CLOCK.fact.in, CLOCK.fact.in + 0.6], [14, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.quad)});
	const axisIn = station.axis ? interpolate(t, [CLOCK.speechDone, CLOCK.speechDone + 0.3, CLOCK.exit, CLOCK.out], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
	const clockP = Math.min(1, t / CLOCK.out);

	return (
		<AbsoluteFill style={{background: T.obsidian, opacity: fadeIn, fontFamily: MONO, color: T.bone}}>
			{clip ? (
				<AbsoluteFill>
					<OffthreadVideo src={clip} volume={hasVoice ? 0.12 : 1} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
				</AbsoluteFill>
			) : (
				<WalkField station={station} color={color} />
			)}
			{/* legibility vignette */}
			<AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(21,16,12,.55) 0%, rgba(21,16,12,0) 26%, rgba(21,16,12,0) 58%, rgba(21,16,12,.88) 100%)'}} />
			{/* side shades: the title block reads on the left, the quick fact on the right, on any plate */}
			<AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(21,16,12,.78) 0%, rgba(21,16,12,.55) 34%, rgba(21,16,12,0) 60%)'}} />
			<AbsoluteFill style={{background: 'linear-gradient(270deg, rgba(21,16,12,.62) 0%, rgba(21,16,12,.3) 24%, rgba(21,16,12,0) 42%)'}} />

			{/* eyebrow */}
			<div style={{position: 'absolute', left: 72, top: 54, display: 'flex', gap: 22, fontSize: 19, letterSpacing: '0.2em', color: T.ash}}>
				<span style={{color, fontWeight: 600}}>{station.id}</span>
				<span>{station.lane}</span>
				<span>STATION {station.k} / {n}</span>
				<span>↔ {station.mirror}{station.axis ? ' · AXIS' : ''}</span>
				<span>{station.cameraGlyph} {station.camera}</span>
				<span>LAP {lap}</span>
			</div>

			{/* rolling counter */}
			<div style={{position: 'absolute', right: 72, top: 34, textAlign: 'right'}}>
				<div style={{fontFamily: SERIF, fontSize: 118, fontWeight: 500, lineHeight: 1, color: T.bone, fontVariantNumeric: 'tabular-nums', textShadow: '0 2px 24px rgba(0,0,0,.8)'}}>{dateLabel}</div>
				<div style={{fontSize: 20, letterSpacing: '0.18em', color: T.ash, marginTop: 6}}>
					{Math.round(am)} AM · {station.place.toUpperCase()}
				</div>
			</div>

			{/* title block */}
			<div style={{position: 'absolute', left: 72, top: 300, maxWidth: 980, opacity: titleIn, transform: `translateY(${titleY}px)`}}>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 34, color: T.bone2}}>{station.place}</div>
				<div style={{fontFamily: SERIF, fontWeight: 700, fontSize: 76, lineHeight: 1.02, letterSpacing: '0.03em', color, textShadow: '0 2px 22px rgba(0,0,0,.85)', marginTop: 8}}>{station.title}</div>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 30, lineHeight: 1.3, color: T.bone2, marginTop: 14, maxWidth: 900}}>{station.claim}</div>
			</div>

			{/* layer 9 — quick fact · right-aligned in the empty mid-right band (x 1100–1848, y 380–700) */}
			{station.fact ? (
				<div style={{position: 'absolute', right: 72, top: 392, maxWidth: 620, textAlign: 'right', opacity: factIn, transform: `translateY(${factY}px)`}}>
					<div style={{marginLeft: 'auto', width: 200, height: 1, background: color, opacity: 0.4}} />
					<div style={{fontFamily: MONO, fontWeight: 600, fontSize: 17, letterSpacing: '0.22em', color, marginTop: 15}}>QUICK FACT</div>
					<div style={{fontFamily: SERIF, fontWeight: 500, fontSize: 34, lineHeight: 1.32, color: T.bone2, marginTop: 10, textShadow: '0 2px 16px rgba(0,0,0,.8)', textWrap: 'balance' as any}}>{station.fact}</div>
				</div>
			) : null}

			{/* captions */}
			<Caption who="NATORI" text={station.natori} tIn={station.voice?.nIn ?? CLOCK.natoriIn} tOut={station.voice?.nOut ?? CLOCK.natoriOut} color={T.ember2} />
			<Caption who="ROGUE" text={station.rogue} tIn={station.voice?.rIn ?? CLOCK.rogueIn} tOut={station.voice?.rOut ?? CLOCK.rogueOut} color={T.ice} />

			{/* check footnote */}
			<div style={{position: 'absolute', left: 72, bottom: 132, maxWidth: 1500, fontSize: 18, lineHeight: 1.45, color: T.ash, opacity: checkIn}}>
				<span style={{color: T.bone2, letterSpacing: '0.18em'}}>CHECK</span> · {station.check}
			</div>

			{/* axis card */}
			{station.axis ? (
				<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: axisIn}}>
					<div style={{background: 'rgba(21,16,12,.78)', border: `1px solid ${color}`, padding: '26px 44px', textAlign: 'center'}}>
						<div style={{fontFamily: SERIF, fontSize: 64, letterSpacing: '0.18em', color: T.bone}}>ERE WE WERE</div>
						<div style={{fontSize: 18, letterSpacing: '0.3em', color, marginTop: 8}}>READS THE SAME RETURNING · 19138 · 83191</div>
					</div>
				</AbsoluteFill>
			) : null}

			{/* clock bar + ribbon */}
			<div style={{position: 'absolute', left: 72, right: 72, bottom: 96, height: 4, background: 'rgba(255,255,255,.08)'}}>
				<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${clockP * 100}%`, background: color, opacity: 0.9}} />
				{[CLOCK.hook, CLOCK.speechDone, CLOCK.exit].map((m) => (
					<div key={m} style={{position: 'absolute', left: `${(m / CLOCK.out) * 100}%`, top: -4, width: 1, height: 12, background: T.bone2, opacity: 0.6}} />
				))}
			</div>
			<div style={{position: 'absolute', left: 72, right: 72, bottom: 40, display: 'grid', gridTemplateColumns: `repeat(${n}, 1fr)`, gap: 4}}>
				{laneStations.map((s) => {
					const now = s.k === station.k;
					const mirror = s.k === station.mirror && !now;
					return (
						<div key={s.id} style={{borderTop: `2px solid ${now ? color : mirror ? T.bone2 : T.line}`, boxShadow: now ? `0 0 14px ${color}` : 'none', paddingTop: 6, fontSize: 12.5, letterSpacing: '0.08em', color: now ? color : mirror ? T.bone2 : T.ash2, whiteSpace: 'nowrap', overflow: 'hidden'}}>
							{s.id} <span style={{opacity: 0.7}}>{s.date.split(' · ')[0].replace(' AD', '').replace(' BC', ' BC')}</span>
						</div>
					);
				})}
			</div>

			{/* exit: dip to black, or return to the first station's frame on 19 */}
			{isLast ? (
				<AbsoluteFill style={{opacity: exitP, background: T.obsidian, justifyContent: 'center', alignItems: 'center'}}>
					<div style={{textAlign: 'center'}}>
						<div style={{fontFamily: SERIF, fontSize: 118, color: T.bone, lineHeight: 1}}>{first.date.split(' · ')[0]}</div>
						<div style={{fontFamily: SERIF, fontWeight: 700, fontSize: 56, color, letterSpacing: '0.04em', marginTop: 10}}>{first.title}</div>
						<div style={{fontSize: 18, letterSpacing: '0.3em', color: T.ash, marginTop: 12}}>RETURN TO START FRAME</div>
					</div>
				</AbsoluteFill>
			) : (
				<AbsoluteFill style={{opacity: exitP, background: T.obsidian, pointerEvents: 'none'}} />
			)}

			{/* audio */}
			{bed ? <Audio src={bed} /> : null}
			{!bed && nat ? (
				<Sequence from={Math.round((station.voice?.nIn ?? CLOCK.natoriIn) * fps)}>
					<Audio src={nat} />
				</Sequence>
			) : null}
			{!bed && rog ? (
				<Sequence from={Math.round((station.voice?.rIn ?? CLOCK.rogueIn) * fps)}>
					<Audio src={rog} />
				</Sequence>
			) : null}
			{score ? <Audio src={score} volume={0.5} /> : null}
		</AbsoluteFill>
	);
};
