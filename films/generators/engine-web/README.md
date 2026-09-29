# The engine in the browser — node-bradley.w3spaces.com/engine

The same station code, played live with `@remotion/player` instead of rendered: visitors pick the whole film or one
station and scrub it; counter, title, quick fact, captions, check line and rail are drawn over the real clips, timed
to the voices.

    esbuild src/web.tsx --bundle --minify --format=iife --jsx=automatic --target=es2019 \
      --define:process.env.NODE_ENV=\"production\" --outfile=dist/js/engine.js

`src/media.ts` and `src/fonts.ts` are the web versions (plain URLs under `window.ENGINE_BASE`, default
`/media/engine/`; fonts via `@font-face` in `site/engine.css`). Media on the site: `public/media/engine/` —
`clips/M01–M12.mp4` (1280 wide, silent), `audio/Mxx-natori|rogue|score.mp3`, `fonts/`, `poster.jpg`.
Page: `site/engine.html` → `public/engine.html`; the home page's Apps section links to `/engine`.
Rendering MP4s stays off the Space; the page only plays.
