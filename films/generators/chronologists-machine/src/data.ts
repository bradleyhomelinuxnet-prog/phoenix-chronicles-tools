import raw from './data/stations.json';

export type Station = {
	id: string;
	k: number;
	lane: string;
	camera: 'FRONT' | 'FOLLOW' | 'SIDE-LR' | 'SIDE-RL' | 'CLIMB' | 'DESCEND';
	cameraGlyph: string;
	cameraWalk: string;
	when: string;
	date: string;
	sortYear: number;
	place: string;
	title: string;
	claim: string;
	anchor: string;
	fact?: string; // layer 9 — 12–22 words, one number where one exists, written from anchor + the two manuscripts
	check: string;
	setting: string;
	hook: string;
	natori: string;
	rogue: string;
	score: string;
	sfx: {t: number; text: string}[];
	axis?: boolean;
	mirror: number;
	promptA: string;
	promptB: string;
	promptC: string;
	ending: string;
	index: number;
	clip?: string;
	voice?: {nIn: number; nOut: number; rIn: number; rOut: number}; // measured voice spans, override the clock
};

export type Lane = {lane: string; subtitle: string; stations: Station[]};

type Compiled = {
	meta: {title: string; reel: string; built: string; negative: string; secondsPerStation: number};
	lanes: Lane[];
};

export const DATA = raw as unknown as Compiled;
export const LANES = DATA.lanes;
export const ALL: Station[] = LANES.flatMap((l) => l.stations);

export const laneByName = (name: string): Lane => {
	const l = LANES.find((x) => x.lane === name);
	if (!l) throw new Error(`No lane ${name}`);
	return l;
};

export const stationById = (id: string): Station => {
	const s = ALL.find((x) => x.id === id);
	if (!s) throw new Error(`No station ${id}`);
	return s;
};

/** Chronicon Annus Mundi for a display year (AM 1 = 3895 BC; AD = AM − 3894 by the book's own rule). */
export const annusMundi = (sortYear: number): number => {
	const y = Math.round(sortYear);
	if (y === -3895) return 1; // the book labels Year One itself 1 AM
	return y < 0 ? 3895 + y : y + 3894; // Chronicon's own table: 3757 BC = 138 AM, 2239 BC = 1656 AM, AD = AM − 3894
};

export const fmtYear = (y: number): string => {
	const r = Math.round(y);
	return r < 0 ? `${Math.abs(r)} BC` : `${r} AD`;
};
