import React, {useMemo, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Player, PlayerRef} from '@remotion/player';
import {LANES} from './data';
import {FPS, STATION_FRAMES} from './theme';
import {Machine} from './Walk';
import {StationScene} from './StationScene';

const lane = LANES[0];
const OneStation: React.FC<{id: string}> = ({id}) => {
	const i = lane.stations.findIndex((s) => s.id === id);
	const s = lane.stations[i];
	const prev = lane.stations[(i - 1 + lane.stations.length) % lane.stations.length];
	return <StationScene station={s} prev={prev} laneStations={lane.stations} first={lane.stations[0]} />;
};

const App: React.FC = () => {
	const [mode, setMode] = useState<'film' | string>('film');
	const ref = useRef<PlayerRef>(null);
	const film = mode === 'film';
	const cur = film ? null : lane.stations.find((s) => s.id === mode)!;
	const props = useMemo(() => (film ? {} : {id: mode}), [mode, film]);
	return (
		<div className="eng">
			<div className="eng-stage">
				<Player
					key={mode}
					ref={ref}
					component={(film ? Machine : OneStation) as any}
					inputProps={props}
					durationInFrames={film ? 90 + STATION_FRAMES * lane.stations.length : STATION_FRAMES}
					fps={FPS}
					compositionWidth={1920}
					compositionHeight={1080}
					controls
					clickToPlay
					doubleClickToFullscreen
					allowFullscreen
					acknowledgeRemotionLicense
					style={{width: '100%', aspectRatio: '16 / 9'}}
				/>
			</div>
			<div className="eng-rail" role="tablist" aria-label="Choose what to play">
				<button role="tab" aria-selected={film} className={film ? 'on' : ''} onClick={() => setMode('film')}>
					<b>Whole film</b>
					<span>3:03 · 12 stations</span>
				</button>
				{lane.stations.map((s) => (
					<button key={s.id} role="tab" aria-selected={mode === s.id} className={mode === s.id ? 'on' : ''} onClick={() => setMode(s.id)}>
						<b>{s.id} · {s.date}</b>
						<span>{s.title}</span>
					</button>
				))}
			</div>
			{cur ? (
				<dl className="eng-sheet">
					<dt>Claim</dt><dd>{cur.claim}</dd>
					<dt>Quick fact</dt><dd>{cur.fact}</dd>
					<dt>Natori</dt><dd>{cur.natori}</dd>
					<dt>Rogue</dt><dd>{cur.rogue}</dd>
					<dt>Check</dt><dd>{cur.check}</dd>
				</dl>
			) : null}
		</div>
	);
};

const mount = document.getElementById('engine-root');
if (mount) createRoot(mount).render(<App />);
