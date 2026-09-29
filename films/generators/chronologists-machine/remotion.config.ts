import {Config} from '@remotion/cli/config';

// ERE WE WERE — render defaults. Change codec/crf here, not in the compositions.
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(90);
Config.setCodec('h264');
Config.setCrf(18);
Config.setOverwriteOutput(true);
Config.setConcurrency(2);

// On a machine where Remotion's own headless Chrome download is blocked, point it at an
// installed Chromium/Chrome by setting REMOTION_BROWSER (any path to a chrome binary).
if (process.env.REMOTION_BROWSER) {
	Config.setBrowserExecutable(process.env.REMOTION_BROWSER);
}
