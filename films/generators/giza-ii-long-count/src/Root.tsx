import React from 'react';
import {Composition, Folder} from 'remotion';
import {LANES, stationById} from './data';
import {FPS, STATION_FRAMES} from './theme';
import {ALL_IDS, Giza, Machine, Trailer, Walk, laneIds, TRAILER_IDS} from './Walk';
import {StationScene} from './StationScene';

const W = 1920;
const H = 1080;

const OneStation: React.FC<{id: string}> = ({id}) => {
	const s = stationById(id);
	const lane = LANES.find((l) => l.lane === s.lane)!.stations;
	const prev = lane[(s.k - 2 + lane.length) % lane.length];
	return <StationScene station={s} prev={prev} laneStations={lane} first={lane[0]} />;
};

export const RemotionRoot: React.FC = () => {
	return (
		<>
			<Composition id="EreWeWere" component={Walk} durationInFrames={STATION_FRAMES * ALL_IDS.length} fps={FPS} width={W} height={H} defaultProps={{ids: ALL_IDS}} />
			<Folder name="Lanes">
				{LANES.map((l) => (
					<Composition key={l.lane} id={`Lane-${l.lane.replace(/\s+/g, "-")}`} component={Walk} durationInFrames={STATION_FRAMES * l.stations.length} fps={FPS} width={W} height={H} defaultProps={{ids: laneIds(l.lane)}} />
				))}
			</Folder>
			<Composition id="Giza" component={Giza} durationInFrames={90 + STATION_FRAMES * 9} fps={FPS} width={W} height={H} />
			<Composition id="Machine" component={Machine} durationInFrames={90 + STATION_FRAMES * 12} fps={FPS} width={W} height={H} />
			<Composition id="Trailer138" component={Trailer} durationInFrames={90 + STATION_FRAMES * TRAILER_IDS.length} fps={FPS} width={W} height={H} />
			<Composition id="Station" component={OneStation} durationInFrames={STATION_FRAMES} fps={FPS} width={W} height={H} defaultProps={{id: 'G01'}} />
		</>
	);
};
