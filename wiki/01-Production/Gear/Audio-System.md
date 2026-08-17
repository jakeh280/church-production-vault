---
title: Audio System (Auditorium)
type: gear
tags: [production, audio, gear]
updated: 2026-08-04
status: active
verified:
source: example content, fictional
---
> [!example] Example content, delete this page during setup
> Fictional content about a made-up church (Northgate Church, Springfield), shipped so the conventions are visible by imitation rather than only described. **Not a real configuration, and nothing here is verified.** The setup interview deletes every page carrying this banner.

# Audio System (Auditorium)

The main auditorium audio rig. One console at front of house drives both the room and the stream feed; there is no separate broadcast mix.

## Signal flow

Stage boxes → console → house PA, with a matrix send feeding the stream encoder. The wireless receivers land on the console's first eight inputs; see [[Handheld-Wireless-TX]] for the transmitter units.

The stream send is a **post-fader matrix**, not an aux, which means anything muted in the house is also gone from the stream. That is deliberate, and it is the cause of most stream audio complaints. See [[No-Audio-In-Stream]].

## Configuration

Scenes are saved per service type. The Sunday scene is the baseline; anything changed during a service gets reverted at load-out rather than saved over the baseline.

Channel naming follows the pattern `<position>-<source>` so the stage plot and the console agree, `SL-Gtr`, `DR-OH-L`.

## Known quirks

The console takes about ninety seconds from power-on before it passes audio. Starting it late is the single most common reason the room isn't ready at call time, which is why it's step one in [[Sunday-Startup]].

## Links

- [[Sunday-Startup]]: the weekend runbook
- [[No-Audio-In-Stream]]: the most common failure
- [[Riverbend-AV]]: installed the system
