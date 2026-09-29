// Web build: media are plain URLs under the page's ENGINE_BASE (default /media/engine/). No getStaticFiles in the browser.
const BASE: string = (typeof window !== 'undefined' && (window as any).ENGINE_BASE) || '/media/engine/';
export const clipFor = (id: string) => `${BASE}clips/${id}.mp4`;
export const bedFor = (_id: string): string | null => null;
export const natoriFor = (id: string) => `${BASE}audio/${id}-natori.mp3`;
export const rogueFor = (id: string) => `${BASE}audio/${id}-rogue.mp3`;
export const scoreFor = (id: string, _lane: string) => `${BASE}audio/${id}-score.mp3`;
