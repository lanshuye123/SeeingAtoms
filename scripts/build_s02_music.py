#!/usr/bin/env python3
"""Compose and render the S02 music bed with MIDI + LMMS + SF2.

The composition is original. The instruments come from the GeneralUser GS
SoundFont (S. Christian Collins), played through LMMS's SF2 Player. No audio
samples from commercial recordings are used.

Outputs (chapters/s02/assets/music/):
  s02_theme.mid   Standard MIDI file, editable in any DAW
  s02_theme.mmp   LMMS 1.2 project with four SF2 Player tracks
  s02_theme.wav   48 kHz stereo render, -23 LUFS bed level

Run:
  source scripts/env.sh
  .venv/bin/python scripts/build_s02_music.py --render
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chapters" / "s02" / "assets" / "music"
SF2 = Path("/home/lanshuye/文档/lmms/samples/soundfonts/GeneralUser-GS.sf2")

BPM = 68
TPB = 192          # ticks per bar (LMMS convention, 4/4)
BEAT = TPB // 4    # 48 ticks per quarter note

# (bar index from 0, chord name, MIDI notes for piano voicing)
CHORDS = [
    # A: 8 bars
    ("Am9",   [45, 52, 59, 60, 67]),
    ("Am9",   [45, 52, 59, 60, 67]),
    ("Fmaj7", [41, 48, 52, 57, 67]),
    ("Fmaj7", [41, 48, 52, 57, 67]),
    ("Cmaj7", [48, 55, 59, 64, 67]),
    ("Cmaj7", [48, 55, 59, 64, 67]),
    ("G6",    [43, 50, 59, 64, 67]),
    ("G6",    [43, 50, 59, 64, 67]),
    # B: 8 bars
    ("Dm9",   [50, 57, 60, 64, 65]),
    ("Dm9",   [50, 57, 60, 64, 65]),
    ("Am9",   [45, 52, 59, 60, 67]),
    ("Am9",   [45, 52, 59, 60, 67]),
    ("Fmaj7", [41, 48, 52, 57, 67]),
    ("Fmaj7", [41, 48, 52, 57, 67]),
    ("Esus4", [40, 47, 52, 57, 64]),
    ("E7sus4",[40, 47, 50, 57, 62]),
    # A': 8 bars
    ("Am9",   [45, 52, 59, 60, 67]),
    ("Fmaj7", [41, 48, 52, 57, 67]),
    ("Cmaj7", [48, 55, 59, 64, 67]),
    ("G6",    [43, 50, 59, 64, 67]),
    ("Am9",   [45, 52, 59, 60, 67]),
    ("Fmaj7", [41, 48, 52, 57, 67]),
    ("Cmaj7", [48, 55, 59, 64, 67]),
    ("G6",    [43, 50, 59, 64, 67]),
    # tail: 4 bars
    ("Am9",   [45, 52, 59, 60, 67]),
    ("Fmaj7", [41, 48, 52, 57, 67]),
    ("Am9",   [45, 52, 59, 60, 67]),
    ("Am9",   [45, 52, 59, 60, 67]),
]

# Piano arpeggio shape: indexes into the voicing, per eighth note.
ARP = [0, 2, 1, 4, 3, 2, 1, 0]

# Bell entries: bar index -> [midi notes]
BELLS = {
    0: [81, 88],
    4: [76, 84],
    8: [81, 88],
    12: [79, 86],
    16: [81, 84],
    20: [79, 86],
    24: [81, 88],
}


def humanize(seed: int, amount: int = 6) -> int:
    # Deterministic pseudo-random timing jitter in ticks.
    x = (seed * 1103515245 + 12345) & 0x7FFFFFFF
    return (x % (2 * amount + 1)) - amount


def piano_events() -> list[tuple[int, int, int, int]]:
    """Return (pos, len, key, velocity) in ticks."""
    events = []
    for bar, (_, notes) in enumerate(CHORDS):
        base = bar * TPB
        for step, idx in enumerate(ARP):
            pos = base + step * (BEAT // 2) + humanize(bar * 17 + step, 5)
            key = notes[min(idx, len(notes) - 1)]
            # Leave some air: drop the 6th eighth in every other bar.
            if step == 5 and bar % 2 == 1:
                continue
            length = BEAT * (2 if step in (0, 4) else 1) - 6
            vel = 68 + (bar % 4) * 4 + (step % 3) * 5
            events.append((max(0, pos), length, key, min(105, vel)))
    return events


def pad_events() -> list[tuple[int, int, int, int]]:
    events = []
    for bar, (_, notes) in enumerate(CHORDS):
        if bar % 2:
            continue
        base = bar * TPB
        for i, key in enumerate(notes[1:4]):
            events.append((base, TPB * 2 - 8, key, 48 + i * 3))
    return events


def cello_events() -> list[tuple[int, int, int, int]]:
    events = []
    for bar, (_, notes) in enumerate(CHORDS):
        if bar % 2:
            continue
        base = bar * TPB
        root = notes[0] - 12
        events.append((base, TPB * 2 - 12, root, 60))
        if bar in (8, 16, 24):
            events.append((base + TPB, TPB - 12, root + 7, 48))
    return events


def bell_events() -> list[tuple[int, int, int, int]]:
    events = []
    for bar, keys in BELLS.items():
        for i, key in enumerate(keys):
            events.append((bar * TPB + i * 12, BEAT * 3, key, 46 + i * 5))
    return events


def write_midi(path: Path) -> None:
    mid = MidiFile(ticks_per_beat=BEAT)
    tempo = mido.bpm2tempo(BPM)

    def add_track(name: str, channel: int, program: int, events):
        track = MidiTrack()
        track.append(MetaMessage("track_name", name=name, time=0))
        track.append(MetaMessage("set_tempo", tempo=tempo, time=0))
        track.append(Message("program_change", channel=channel, program=program, time=0))
        for pos, length, key, vel in sorted(events):
            track.append(Message("note_on", channel=channel, note=key, velocity=vel, time=pos))
            track.append(Message("note_off", channel=channel, note=key, velocity=0, time=length))
        mid.tracks.append(track)

    add_track("Piano", 0, 0, piano_events())
    add_track("Pad", 1, 89, pad_events())
    add_track("Cello", 2, 42, cello_events())
    add_track("Bell", 3, 9, bell_events())
    mid.save(path)


def xml_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def track_xml(name: str, patch: int, events, total_ticks: int, gain: float = 2.0, pan: int = 0) -> str:
    notes = "\n".join(
        f'            <note len="{length}" key="{key}" vol="{vel}" pos="{pos}" pan="0"/>'
        for pos, length, key, vel in sorted(events)
    )
    return f'''      <track name="{xml_escape(name)}" type="0" muted="0" solo="0">
        <instrumenttrack usemasterpitch="1" pan="{pan}" pitchrange="1" fxch="0" pitch="0" basenote="57" vol="100">
          <instrument name="sf2player">
            <sf2player reverbOn="1" reverbDamping="0.55" chorusNum="0.7" chorusDepth="4.25" bank="0" reverbRoomSize="0.5" chorusSpeed="0.29" patch="{patch}" reverbLevel="0.28" src="{xml_escape(str(SF2))}" gain="{gain}" reverbWidth="0.8" chorusOn="0" chorusLevel="0.6"/>
          </instrument>
          <eldata fres="0.5" fwet="0" fcut="14000" ftype="0">
            <elvol att="0" lspd_numerator="4" sustain="0.5" lspd="0.1" x100="0" lpdel="0" ctlenvamt="0" hold="0.5" rel="0.1" userwavefile="" lspd_syncmode="0" lamt="0" latt="0" dec="0.5" lshp="0" pdel="0" lspd_denominator="4" amt="0"/>
            <elcut att="0" lspd_numerator="4" sustain="0.5" lspd="0.1" x100="0" lpdel="0" ctlenvamt="0" hold="0.5" rel="0.1" userwavefile="" lspd_syncmode="0" lamt="0" latt="0" dec="0.5" lshp="0" pdel="0" lspd_denominator="4" amt="0"/>
            <elres att="0" lspd_numerator="4" sustain="0.5" lspd="0.1" x100="0" lpdel="0" ctlenvamt="0" hold="0.5" rel="0.1" userwavefile="" lspd_syncmode="0" lamt="0" latt="0" dec="0.5" lshp="0" pdel="0" lspd_denominator="4" amt="0"/>
          </eldata>
          <chordcreator chordrange="1" chord-enabled="0" chord="0"/>
          <arpeggiator arpskip="0" arpmiss="0" arpdir="0" arptime_numerator="4" arptime_denominator="4" arptime="200" arp="0" arpgate="100" arptime_syncmode="0" arpmode="0" arp-enabled="0" arprange="1" arpcycle="0"/>
          <midiport outputchannel="1" fixedinputvelocity="-1" outputprogram="1" fixedoutputvelocity="-1" inputchannel="0" outputcontroller="0" basevelocity="63" readable="0" fixedoutputnote="-1" writable="0" inputcontroller="0"/>
          <fxchain enabled="0" numofeffects="0"/>
        </instrumenttrack>
        <pattern len="{total_ticks}" muted="0" name="{xml_escape(name)}" steps="16" pos="0" type="1">
{notes}
        </pattern>
      </track>
'''


def write_lmms(path: Path) -> None:
    total = len(CHORDS) * TPB
    tracks = "".join([
        track_xml("Piano", 0, piano_events(), total, gain=2.6, pan=-14),
        track_xml("Pad", 89, pad_events(), total, gain=2.0, pan=18),
        track_xml("Cello", 42, cello_events(), total, gain=2.2, pan=0),
        track_xml("Bell", 9, bell_events(), total, gain=2.0, pan=26),
    ])
    xml = f'''<?xml version="1.0"?>
<!DOCTYPE lmms-project>
<lmms-project creator="LMMS" version="1.0" type="song" creatorversion="1.2.2">
  <head timesig_numerator="4" bpm="{BPM}" timesig_denominator="4" mastervol="100" masterpitch="0"/>
  <song>
    <trackcontainer type="song" visible="1" maximized="0" minimized="0" height="500" width="900" x="5" y="5">
{tracks}    </trackcontainer>
  </song>
</lmms-project>
'''
    path.write_text(xml, encoding="utf-8")


def render(lmms: Path, wav: Path) -> None:
    import os
    env = dict(os.environ)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    subprocess.run(["lmms", "render", str(lmms), "-o", str(wav)],
                   check=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav),
        "-af", "highpass=f=35,lowpass=f=12000,afade=t=in:st=0:d=2,afade=t=out:st="
               f"{max(0.0, len(CHORDS) * 4 * 60 / BPM - 4):.2f}:d=4,"
               "loudnorm=I=-23:TP=-2.5:LRA=9",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(wav.with_suffix(".norm.wav")),
    ], check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    write_midi(OUT / "s02_theme.mid")
    write_lmms(OUT / "s02_theme.mmp")
    print(f"bars={len(CHORDS)} bpm={BPM} duration={len(CHORDS)*4*60/BPM:.1f}s")
    if args.render:
        render(OUT / "s02_theme.mmp", OUT / "s02_theme.wav")
        print(f"rendered {OUT / 's02_theme.wav'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
