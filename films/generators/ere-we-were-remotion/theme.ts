// Ember-and-ice on warm obsidian — Bee's house palette for designed video (rogue-render brand.json values).
export const T = {
	obsidian: '#15100c',
	obsidian2: '#1c1510',
	panel: '#231a14',
	line: '#3b2d24',
	bone: '#efe4d3',
	bone2: '#d8cbb8',
	ash: '#a1927f',
	ash2: '#6f6355',
	ember: '#f2701d',
	ember2: '#ffb057',
	ice: '#8fd0ff',
	ice2: '#77a8dd',
	gold: '#e2c069',
	red: '#8d1a1a',
};

export const LANE_COLOR: Record<string, string> = {
	EVIDENCE: T.ice,
	CHRONICON: T.ember2,
	CIPHER: T.gold,
	FLOOD: T.ember, // the 552-year chain — every fourth Phoenix
};

export const FPS = 30;
export const STATION_SECONDS = 15;
export const STATION_FRAMES = FPS * STATION_SECONDS; // 450

// The 15-second clock (hf-scriptwriter): hook by 1.9, speech done by 13.8, settle, exit at 14.5.
export const CLOCK = {
	hook: 1.9,
	natoriIn: 2.4,
	natoriOut: 7.8,
	rogueIn: 8.6,
	rogueOut: 13.6,
	speechDone: 13.8,
	exit: 14.5,
	out: 15.0,
	// layer 9 — quick fact window: in during voice 1's tail, out before the check line (9.0)
	fact: {in: 4.6, out: 9.0},
};
