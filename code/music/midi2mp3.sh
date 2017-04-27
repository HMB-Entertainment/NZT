#!/bin/bash
    timidity right.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 2 right.mp3
    timidity wrong.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 2 wrong.mp3
    timidity delta.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 2 delta.mp3
    timidity empty.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 0.5 empty.mp3
    timidity x.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 0.5 x.mp3
    timidity y.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 0.5 y.mp3
    timidity xy.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 0.5 xy.mp3
    timidity z.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 0.5 z.mp3
    timidity zx.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 0.5 zx.mp3
    timidity zy.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 0.5 zy.mp3
    timidity xyz.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k -t 0.5 xyz.mp3
