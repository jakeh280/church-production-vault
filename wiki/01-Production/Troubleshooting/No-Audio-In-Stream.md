---
title: No audio in the stream
type: troubleshooting
tags: [production, audio, troubleshooting]
updated: 2026-08-04
status: active
verified:
source: example content, fictional
---
> [!example] Example content, delete this page during setup
> Fictional content about a made-up church (Northgate Church, Springfield), shipped so the conventions are visible by imitation rather than only described. **Not a real configuration, and nothing here is verified.** The setup interview deletes every page carrying this banner.

# No audio in the stream

## Symptom

The room sounds fine. The stream has nothing, or has music but no speaking.

## Most likely cause

Something is muted in the house that the stream also depends on. The stream feed is a **post-fader matrix** off the main console ([[Audio-System]]), so it inherits every mute and fader move made for the room. A mic pulled down because it was feeding back in the room is equally gone online.

## Fix

1. Look at what's muted on the console. Unmute, or route around it.
2. If everything looks right at the console, check that the encoder is actually seeing level, a meter at the encoder, not just at the console.

## If that isn't it

- Encoder input set to the wrong source after someone changed it mid-week
- A cable pulled during a midweek event and not put back
- The stream platform itself dropping the audio track, which looks identical from the booth and isn't

## History

- **2026-05-17**: no speech audio for the first six minutes. Pastor's channel had been muted at the end of rehearsal and never unmuted. Root cause of the post-fader design being noticed at all.
- **2026-07-26**: reported again; turned out to be the platform, not us. Worth ruling out our side quickly rather than assuming.
