# AGENTS.md — pbtv

## Project overview
A set of scripts and a streamlink plugin for watching/recording pickleballtv.com streams.

## Key scripts

- **`pbtv`** (bash) — main entrypoint. Play/record streams via streamlink.
- **`tsmerge`** (bash) — merge `.ts` recording files into `.mp4` via ffmpeg.
- **`pbtv-schedule`** (python3) — fetch and display the pickleballtv.com schedule.
- **`streamlink/plugins/pickleballtv.py`** — streamlink plugin (resolves HLS URL from JW Player API).
- **`pbtv.m3u8`** — static playlist with a direct stream URL (fallback/alternative).

## Commands

```bash
# Install the streamlink plugin (required once)
./pbtv --install

# Check plugin is registered
streamlink --plugins | grep pickleballtv

# Play in mpv (default player)
./pbtv

# Record indefinitely (Ctrl-C to stop)
./pbtv -r

# Record for 3 hours
./pbtv -r -d 180

# Sleep until a specific time, then record
./pbtv -s 'saturday 10am' -r -d 300 -q 720p

# Merge .ts recordings into .mp4
./tsmerge *.ts        # all .ts files
./tsmerge -d *.ts     # merge and delete originals
./tsmerge             # interactive fzf picker

# Show schedule for next N days
python3 pbtv-schedule -d 3

# Generate XMLTV EPG XML (for IPTV channel guide)
python3 pbtv-schedule --epg -d 7
python3 pbtv-schedule --epg -d 7 --tvg-id "pickleball.tv" --tvg-name "Pickleball TV" --epg-timezone "America/New_York"
```

## Environment variables

| Variable                | Default                             | Description                                                               |
| ----------------------- | ----------------------------------- | ------------------------------------------------------------------------- |
| `PBTV_DEFAULT_PLAYER`   | `mpv`                               | Video player command                                                      |
| `PBTV_DEFAULT_QUALITY`  | `best`                              | Stream quality (`240p`, `360p`, `480p`, `720p`, `1080p`, `best`, `worst`) |
| `STREAMLINK_PLUGIN_DIR` | `~/.local/share/streamlink/plugins` | Plugin install path (override for testing)                                |

## Python script dependencies

`pbtv-schedule` needs these pip packages (no `requirements.txt`):
- `requests`
- `bs4` (BeautifulSoup4)

## Recording behavior (streamlink)

Streamlink exits on every commercial break because the HLS stream switches. The `pbtv` script handles this by restarting streamlink in a loop, creating sequentially-numbered `.ts` files (`pbtv-YYYYMMDD-HHMM-1.ts`, `-2.ts`, etc.). Use `tsmerge` to combine them into one `.mp4`.

## Runtime state files

- `/tmp/pbtv.pid` — PID lock (prevents multiple concurrent runs)
- `/tmp/pbtv.recording` — recording semaphore (controls the retry loop)
- `/tmp/pbtv.log` — all output is tee'd here by the `pbtv` script
- `pbtv.html` — cached schedule HTML (created by `pbtv-schedule -D`)

## No build/tooling

No `package.json`, `Makefile`, CI, tests, linter config, or formatter. Check for syntax errors manually:
```bash
shellcheck pbtv tsmerge
python3 -c "import py_compile; py_compile.compile('pbtv-schedule', dfile='pbtv-schedule')"
```
