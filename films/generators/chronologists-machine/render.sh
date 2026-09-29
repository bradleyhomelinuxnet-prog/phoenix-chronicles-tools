#!/bin/bash
cd /home/claude/rem-machine
export REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
npx remotion render src/index.ts Machine out/Machine_raw.mp4 --muted --log=error > render.log 2>&1 && echo RENDERDONE >> render.log || echo RENDERFAIL >> render.log
