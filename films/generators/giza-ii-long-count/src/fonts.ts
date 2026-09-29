import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Self-hosted (public/fonts) so a render needs no network. Latin subset, downloaded from Google Fonts.
const faces: [string, string, string, string][] = [
	['Cormorant Garamond', '500', 'normal', 'CormorantGaramond-500-normal.woff2'],
	['Cormorant Garamond', '600', 'normal', 'CormorantGaramond-600-normal.woff2'],
	['Cormorant Garamond', '700', 'normal', 'CormorantGaramond-700-normal.woff2'],
	['Cormorant Garamond', '500', 'italic', 'CormorantGaramond-500-italic.woff2'],
	['Cormorant Garamond', '600', 'italic', 'CormorantGaramond-600-italic.woff2'],
	['IBM Plex Mono', '400', 'normal', 'IBMPlexMono-400-normal.woff2'],
	['IBM Plex Mono', '500', 'normal', 'IBMPlexMono-500-normal.woff2'],
	['IBM Plex Mono', '600', 'normal', 'IBMPlexMono-600-normal.woff2'],
];

for (const [family, weight, style, file] of faces) {
	loadFont({family, url: staticFile(`fonts/${file}`), weight, style, format: 'woff2'}).catch(() => {
		// A missing file falls back to the system stack below; the render still completes.
	});
}

export const SERIF = `"Cormorant Garamond", Georgia, "Times New Roman", serif`;
export const MONO = `"IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace`;
