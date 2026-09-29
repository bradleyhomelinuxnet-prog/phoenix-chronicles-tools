import {getStaticFiles, staticFile} from 'remotion';

/**
 * Anything dropped into public/ is picked up by name, no code changes:
 *   public/clips/E01.mp4                the Higgsfield clip for station E01 (mp4 / webm / mov)
 *   public/audio/E01.mp3                a finished 15 s dialogue bed, already cut to the clock
 *   public/audio/E01-natori.mp3         Vesper's line alone   → placed at 2.4 s
 *   public/audio/E01-rogue.mp3          Wilder's line alone   → placed at 8.6 s
 *   public/audio/E01-score.mp3          a per-station 15 s cue
 *   public/audio/score-EVIDENCE.mp3     a per-lane cue (looped under every station of that lane)
 *   public/audio/score.mp3              a global cue
 */
const files = () => getStaticFiles().map((f) => f.name);

const find = (candidates: string[]): string | null => {
	const all = files();
	for (const c of candidates) {
		if (all.includes(c)) return staticFile(c);
	}
	return null;
};

const vext = ['mp4', 'webm', 'mov'];
const aext = ['mp3', 'wav', 'm4a', 'aac', 'ogg'];

export const clipFor = (id: string) => find(vext.map((e) => `clips/${id}.${e}`));
export const bedFor = (id: string) => find(aext.map((e) => `audio/${id}.${e}`));
export const natoriFor = (id: string) => find(aext.map((e) => `audio/${id}-natori.${e}`));
export const rogueFor = (id: string) => find(aext.map((e) => `audio/${id}-rogue.${e}`));
export const scoreFor = (id: string, lane: string) =>
	find([
		...aext.map((e) => `audio/${id}-score.${e}`),
		...aext.map((e) => `audio/score-${lane}.${e}`),
		...aext.map((e) => `audio/score.${e}`),
	]);
