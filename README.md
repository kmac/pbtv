# pbtv - a client for watching pickleballtv

This is a set of scripts and a [streamlink](https://streamlink.github.io/) plugin, allowing viewing of pickleballtv in a video player (e.g.
mpv or vlc). You can also record to file for timeshifting purposes.

This project is in no way associated with pickleballtv.com, and is only intended for local consumption.
I only use it to view live games before they are posted to youtube.


## Prerequisites

Ensure the following packages are installed on your system:
- streamlink

For converting the .ts files into mp4 format (via tsmerge):
- ffmpeg
- lsof
- fzf (optional: used as a file picker for manual selection of .ts files)


## Installation

Clone this repository onto your local file system.

Run `pbtv --install` to install the streamlink pickleballtv plugin into ~/.local/share/streamlink/plugins/pickleballtv.py
Alternatively, you can manually install the plugin from this repo into the above location.

Check the install using `streamlink --plugins`. The list should include `pickleballtv`.


## Using pbtv

Use `pbtv --help` for full help and usage examples.

By default, the pbtv script launches pickleballtv using `mpv` as its default player.
Options also exist to record to file.

You can switch the player using either the `-p/--player` option, or by setting the
`PBTV_DEFAULT_PLAYER` environment variable to the player command of your choice (e.g. vlc)

You can select the video quality using either the `-q/--quality` option, or by setting the
`PBTV_DEFAULT_QUALITY` environment variable.


### Recording

Record the stream to file using the `-r/--record` flag. By default, the recording continues indefinitely (until Control-c is pressed).
Use the `-d/--duration` option to stop the recording after the given number of minutes.

When recording to file, the stream is saved to raw `.ts` (mpeg-ts) transparent stream format. These files can be played by mpv or vlc, or
you can remux it to mp4 (see tsmerge below).

#### -s / --sleep-until

For convenience, use the `-s/--sleep-until` option to wait until a given time before starting to play or record. This argument takes a
flexible string argument, specifying the date/time when you want to start. Examples: '3pm', '16:30', '4:30pm', '2am tomorrow', '3pm monday',
'monday 3pm'. See the `DATE STRING` section of `man date` for full documentation on this argument.


#### streamlink behaviour over commercial break:

streamlink doesn't handle the stream switchover which happens on every commercial break. You'll see that the stream is interrupted on every
commercial break.

When this happens, streamlink exits. We handle this by restarting streamlink. A new .ts file is created, and we use an
increasing index to identify each file.

Example output:
```
[stream.hls][warning] Encountered a stream discontinuity. This is unsupported and will result in incoherent output data.
[stream.hls][warning] No new segments in playlist for more than 6.00s. Stopping...
[cli][info] Stream ended
[cli][info] Closing currently open stream...
streamlink exited with code: 0
2024-09-25 21:25:28 Starting streamlink quality=480p -> pbtv-20240925-2125-1.ts
```

The .ts files can be viewed by mpv or vlc, or you can use the `tsmerge` script to combine the .ts files while converting to the mp4 format.

This is an example of the output you will see over a commercial break:


## Using tsmerge

The `tsmerge` script merges multiple .ts files into a single mp4 file. You can use this script to combine the .ts files created by `pbtv`.

If you don't supply any .ts files, `fzf` is used to select files from the current directory.

Examples, from `tsmerge --help`:
```
  tsmerge                               # Invokes fzf to select .ts files for merge
  tsmerge file1.ts file2.ts file3.ts    # Merge given .ts files
  tsmerge *.ts                          # Merge all .ts files
  tsmerge -d *.ts                       # As above, but delete the original .ts files
  tsmerge -d -o /media/merged.mp4 *.ts  # As above, but delete the .ts
                                        # files, and write output to path /media/merged.mp4
```
