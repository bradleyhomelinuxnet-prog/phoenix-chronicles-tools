import React from 'react';
import {AbsoluteFill, random, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Station} from './data';
import {T} from './theme';

/**
 * Previz ground for a station that has no Higgsfield clip yet: an obsidian field whose lines flow
 * in the station's walk direction, the blood-red body in the sky, embers rising. Replaced entirely
 * by the clip once public/clips/<ID>.mp4 exists.
 */
export const WalkField: React.FC<{station: Station; color: string}> = ({station, color}) => {
	const frame = useCurrentFrame();
	const {width: W, height: H, fps} = useVideoConfig();
	const t = frame / fps;
	const cam = station.camera;
	const horizon = cam === 'CLIMB' ? H * 0.26 : cam === 'DESCEND' ? H * 0.68 : H * 0.46;
	const speed = cam === 'DESCEND' ? 0.10 : cam === 'CLIMB' ? 0.16 : 0.13; // cycles per second
	const N = 14;
	const lines: React.ReactNode[] = [];
	if (cam === 'SIDE-LR' || cam === 'SIDE-RL') {
		const dir = cam === 'SIDE-LR' ? 1 : -1;
		for (let i = 0; i < N * 2; i++) {
			const p = (((i / (N * 2)) + dir * t * speed) % 1 + 1) % 1;
			const x = p * W;
			lines.push(<line key={i} x1={x} y1={horizon} x2={x + (x - W / 2) * 0.35} y2={H} stroke={T.line} strokeWidth={1} opacity={0.9} />);
		}
		for (let j = 1; j <= 6; j++) {
			const y = horizon + (H - horizon) * (j / 6) ** 1.8;
			lines.push(<line key={'h' + j} x1={0} y1={y} x2={W} y2={y} stroke={T.line} strokeWidth={1} opacity={0.5 + j * 0.06} />);
		}
	} else {
		const dir = cam === 'FOLLOW' ? -1 : 1; // toward viewer = lines flow down
		for (let i = 0; i < N; i++) {
			const p = (((i / N) + dir * t * speed) % 1 + 1) % 1;
			const y = horizon + (H - horizon) * p * p;
			lines.push(<line key={i} x1={0} y1={y} x2={W} y2={y} stroke={T.line} strokeWidth={1 + p * 1.5} opacity={0.5 + p * 0.5} />);
		}
		for (let j = -6; j <= 6; j++) {
			const x0 = W / 2 + j * 70;
			const x1 = W / 2 + j * 520;
			lines.push(<line key={'v' + j} x1={x0} y1={horizon} x2={x1} y2={H} stroke={T.line} strokeWidth={1} opacity={0.55} />);
		}
	}
	// embers
	const embers: React.ReactNode[] = [];
	const seed = station.id;
	for (let i = 0; i < 46; i++) {
		const rx = random(`${seed}-x${i}`);
		const ry = random(`${seed}-y${i}`);
		const rs = random(`${seed}-s${i}`);
		const rise = ((ry + t * (0.02 + rs * 0.03)) % 1);
		const x = rx * W + Math.sin(t * 0.8 + i) * 14;
		const y = H - rise * H;
		const isIce = i % 5 === 0;
		embers.push(<circle key={i} cx={x} cy={y} r={0.8 + rs * 2.4} fill={isIce ? T.ice : T.ember} opacity={0.15 + (1 - rise) * 0.5} />);
	}
	const bodyX = W * 0.74 + Math.sin(t * 0.15) * 8;
	const bodyY = H * 0.22 + Math.cos(t * 0.12) * 6;
	return (
		<AbsoluteFill style={{background: `radial-gradient(1200px 700px at 50% 110%, ${T.obsidian2}, ${T.obsidian})`}}>
			<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', inset: 0}}>
				<defs>
					<radialGradient id="body" cx="50%" cy="50%" r="50%">
						<stop offset="0%" stopColor="#c0271c" stopOpacity="0.85" />
						<stop offset="55%" stopColor="#7a1512" stopOpacity="0.55" />
						<stop offset="100%" stopColor="#7a1512" stopOpacity="0" />
					</radialGradient>
					<radialGradient id="glow" cx="50%" cy="50%" r="50%">
						<stop offset="0%" stopColor={color} stopOpacity="0.28" />
						<stop offset="100%" stopColor={color} stopOpacity="0" />
					</radialGradient>
				</defs>
				<circle cx={bodyX} cy={bodyY} r={H * 0.42} fill="url(#body)" />
				<circle cx={bodyX} cy={bodyY} r={H * 0.2} fill="#5c100d" opacity={0.8} />
				<rect x={0} y={horizon - 2} width={W} height={H - horizon + 2} fill="url(#glow)" opacity={0.5} />
				{lines}
				<line x1={0} y1={horizon} x2={W} y2={horizon} stroke={color} strokeWidth={1} opacity={0.35} />
				{embers}
			</svg>
		</AbsoluteFill>
	);
};
