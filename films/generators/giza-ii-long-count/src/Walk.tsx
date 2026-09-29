import React from 'react';
import {AbsoluteFill, Series, useVideoConfig} from 'remotion';
import {ALL, LANES, stationById} from './data';
import type {Station} from './data';
import {MONO, SERIF} from './fonts';
import {STATION_FRAMES, T} from './theme';
import {StationScene} from './StationScene';

const laneOf = (s: Station) => LANES.find((l) => l.lane === s.lane)!.stations;

/** Walks an ordered list of station ids, 15 s each. The counter rolls from the station walked from. */
export const Walk: React.FC<{ids: string[]}> = ({ids}) => {
	const seq = ids.map(stationById);
	return (
		<AbsoluteFill style={{background: T.obsidian}}>
			<Series>
				{seq.map((s, i) => {
					const prev = seq[(i - 1 + seq.length) % seq.length];
					const lane = laneOf(s);
					return (
						<Series.Sequence key={`${s.id}-${i}`} durationInFrames={STATION_FRAMES} name={`${s.id} ${s.title}`}>
							<StationScene station={s} prev={prev} laneStations={lane} first={lane[0]} lap={Math.floor(i / lane.length) + 1} />
						</Series.Sequence>
					);
				})}
			</Series>
		</AbsoluteFill>
	);
};

export const ALL_IDS = ALL.map((s) => s.id);
export const laneIds = (lane: string) => LANES.find((l) => l.lane === lane)!.stations.map((s) => s.id);

/** 138.000 s: a 3 s title card + nine stations (the three openings, the three axes, the three returns). */
export const TRAILER_IDS = ['E01', 'C04', 'K03', 'E10', 'C10', 'K10', 'E19', 'C19', 'K19'];

export const TitleCard: React.FC = () => {
	const {fps} = useVideoConfig();
	void fps;
	return (
		<AbsoluteFill style={{background: T.obsidian, justifyContent: 'center', alignItems: 'center', fontFamily: MONO}}>
			<div style={{textAlign: 'center'}}>
				<div style={{fontSize: 22, letterSpacing: '0.4em', color: T.ash}}>19138</div>
				<div style={{fontFamily: SERIF, fontSize: 150, letterSpacing: '0.16em', color: T.bone, lineHeight: 1, margin: '18px 0'}}>ERE WE WERE</div>
				<div style={{fontSize: 22, letterSpacing: '0.4em', color: T.ash}}>83191</div>
				<div style={{fontSize: 20, letterSpacing: '0.24em', color: T.ember2, marginTop: 30}}>REEL IV · THREE WALKS · FIFTY-SEVEN STATIONS</div>
			</div>
		</AbsoluteFill>
	);
};

export const Trailer: React.FC = () => (
	<AbsoluteFill style={{background: T.obsidian}}>
		<Series>
			<Series.Sequence durationInFrames={90} name="Title">
				<TitleCard />
			</Series.Sequence>
			<Series.Sequence durationInFrames={STATION_FRAMES * TRAILER_IDS.length} name="Nine stations">
				<Walk ids={TRAILER_IDS} />
			</Series.Sequence>
		</Series>
	</AbsoluteFill>
);

/** THE CHRONOLOGIST'S MACHINE — 3 s title + the twelve fires, 15 s each = 183 s = 3:03, reads the same returning. */
export const MachineTitle: React.FC = () => (
	<AbsoluteFill style={{background: T.obsidian, justifyContent: 'center', alignItems: 'center', fontFamily: MONO}}>
		<div style={{textAlign: 'center'}}>
			<div style={{fontSize: 22, letterSpacing: '0.4em', color: T.ash}}>19138</div>
			<div style={{fontFamily: SERIF, fontSize: 132, letterSpacing: '0.16em', color: T.bone, lineHeight: 1, margin: '18px 0'}}>ERE WE WERE</div>
			<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 46, color: T.ice}}>The Chronologist’s Machine</div>
			<div style={{fontSize: 22, letterSpacing: '0.4em', color: T.ash, marginTop: 18}}>83191</div>
			<div style={{fontSize: 20, letterSpacing: '0.24em', color: T.ember2, marginTop: 30}}>TWELVE FIRES · 5239 BC → 2040 AD · 3:03</div>
		</div>
	</AbsoluteFill>
);

export const Machine: React.FC = () => (
	<AbsoluteFill style={{background: T.obsidian}}>
		<Series>
			<Series.Sequence durationInFrames={90} name="Title">
				<MachineTitle />
			</Series.Sequence>
			<Series.Sequence durationInFrames={STATION_FRAMES * 12} name="Twelve fires">
				<Walk ids={laneIds('MACHINE')} />
			</Series.Sequence>
		</Series>
	</AbsoluteFill>
);

/** GIZA II · THE LONG COUNT in the Flood Chain look — 3 s title + 9 × 15 s = 138.000 s. */
export const GizaTitle: React.FC = () => {
	const {fps} = useVideoConfig();
	return (
		<AbsoluteFill style={{background: `radial-gradient(900px 620px at 71% 36%, rgba(141,26,26,.62) 0%, rgba(90,22,18,.28) 42%, rgba(21,16,12,0) 72%), ${T.obsidian}`, justifyContent: 'center', alignItems: 'center', fontFamily: MONO}}>
			<div style={{textAlign: 'center', transform: 'translateY(-60px)'}}>
				<div style={{fontSize: 20, letterSpacing: '0.34em', color: T.ash}}>ERE WE WERE  ·  THE LOST SECRETS OF GIZA  ·  II</div>
				<div style={{fontFamily: SERIF, fontSize: 118, letterSpacing: '0.05em', color: T.bone, lineHeight: 1, margin: '22px 0 26px'}}>THE LONG COUNT</div>
				<div style={{fontSize: 26, fontWeight: 600, letterSpacing: '0.18em', color: T.ember}}>5239 BC  ·  1567 BC  ·  2106 AD</div>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 38, color: T.bone2, marginTop: 22}}>7,344 years, folded in half</div>
			</div>
			<span style={{display: 'none'}}>{fps}</span>
		</AbsoluteFill>
	);
};

export const Giza: React.FC = () => (
	<AbsoluteFill style={{background: T.obsidian}}>
		<Series>
			<Series.Sequence durationInFrames={90} name="Title">
				<GizaTitle />
			</Series.Sequence>
			<Series.Sequence durationInFrames={STATION_FRAMES * 9} name="Nine stations">
				<Walk ids={laneIds('LONG COUNT')} />
			</Series.Sequence>
		</Series>
	</AbsoluteFill>
);
