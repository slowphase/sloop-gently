"""The three approved page compositions (14, 18, 23) as section strings. No build dependencies."""
import interior as I, art

PIN = '<svg viewBox="0 0 12 12"><circle cx="6" cy="6" r="2.2" fill="currentColor"/><circle cx="6" cy="6" r="4.6" fill="none" stroke="currentColor" stroke-width="1.1"/></svg>'
SPARK = '<svg viewBox="0 0 12 12"><path d="M6,0 C6.6,4 8,5.4 12,6 C8,6.6 6.6,8 6,12 C5.4,8 4,6.6 0,6 C4,5.4 5.4,4 6,0Z" fill="currentColor"/></svg>'
UNDO = '<svg viewBox="0 0 12 12"><path d="M3.2,4.2 H7.6 A3.1,3.1 0 0 1 7.6,10.4 H4.4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M5,1.6 L2.2,4.2 L5,6.8" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PLAY = '<svg viewBox="0 0 12 12"><path d="M3,1.8 L10,6 L3,10.2Z" fill="currentColor"/></svg>'
W = art.wave_icon()

def hear(t): return f'<div class="hear">{W}<div><div class="label">{PLAY}you should now be hearing</div><p>{t}</p></div></div>'

# ============================================================== PAGE 14 · Shaping a sound
p14 = f'''
<section class="page r2 trk1 odd" id="l2" data-part="Part 1 · Atmosphere">
  <div class="runhead"><span>L2 · shaping a sound</span><span class="trk">track 1</span></div>
  <div class="kicker"><span class="chno">L2</span><span>Lesson two · Atmosphere</span></div>
  <h1 style="font-size:30pt;margin:0 0 3mm;">Shaping a sound</h1>
  <div class="row" style="grid-template-columns:1fr 1fr;gap:9mm;">
    <p class="lead">Three ideas, envelope, LFO and filter, are most of what "synthesis" means. Each is one page of four knobs, and each makes immediate sense on a pad.</p>
    <div class="start" style="margin:0;"><div class="label">{PIN}starting from here</div>
      <ul>
        <li>Track <span class="tt t1">1</span> selected, a pad loaded (WARM PAD is perfect), some reverb on it, as in Lesson&nbsp;1.</li>
        <li>HOLD can be on or off; off is less confusing while you experiment.</li>
      </ul>
    </div>
  </div>

  <h2 style="margin-top:5mm;">The envelope: how a note fades in and out</h2>
  <p style="max-width:150mm;">Tap <kbd>ENV</kbd> (the page titled <span class="v">ENV</span>; tap again if ENV&nbsp;DEST shows instead). Four dials: <span class="v">ATK</span> (attack), <span class="v">DEC</span> (decay), <span class="v">SUS</span> (sustain) and <span class="v">REL</span> (release). Together they draw the shape of every note's loudness:</p>
  <figure style="margin:0 auto .5mm;width:142mm;">{I.envelope_big()}</figure>
  <div class="row" style="grid-template-columns:1fr 1fr;gap:9mm;">
    <div class="annot a1"><span class="n">1</span><p><b>Raise ATK</b> well up and play a chord: it now blooms instead of starting. This single move turns almost any sound into a pad.</p></div>
    <div class="annot a4"><span class="n">2</span><p><b>Raise REL</b> too: when you let go, the chord exhales slowly rather than stopping. Long attack, long release, and you can play lazily; the sound smooths everything over.</p></div>
  </div>

  <h2 style="margin-top:3mm;">The filter: one knob of brightness</h2>
  <div class="row" style="grid-template-columns:1fr 1.3fr;gap:8mm;align-items:start;">
    <figure style="margin:2mm 0 0;width:100%;">{I.filter_dial()}</figure>
    <div>
      <p style="margin:0;">Hold <kbd>FX</kbd> and turn <kbd class="knob">KNOB 4</kbd>: this is the track's filter on one dial. Left of centre it is a <b>low-pass</b>, closing the sound down to something dark and distant; right of centre a <b>high-pass</b>, thinning it to a whisper; centre is off. To sweep it while a chord sounds, let the chord hold itself first (KBD&nbsp;HOLD from Lesson&nbsp;1), since one hand is on FX and the other on the knob; then sweep slowly and you will hear why filters are the most loved control in electronic music. It stays where you leave it, even when you change sounds.</p>
      <div class="gb" style="margin-top:2mm;"><div class="label">GarageBand translation</div>
  <p>A low-pass filter is the "cutoff" dial on GarageBand's synth Smart Controls, or an EQ with the treble pulled right down: the tone control of the synth world. <b>Cutoff</b> just means the point where brightness stops.</p></div>
    </div>
  </div>
  <div class="folio"><span class="n">14</span><span class="t">SLOOP, Gently</span></div>
</section>'''

# ============================================================== PAGE 18 · Weather
p18 = f'''
<section class="page r2 trk2 even" id="l4" data-part="Part 1 · Atmosphere">
  <div class="runhead"><span>L4 · weather</span><span class="trk">any track</span></div>
  <div class="kicker"><span class="chno">L4</span><span>Lesson four · Atmosphere</span></div>
  <div class="row" style="grid-template-columns:1fr 1fr;gap:9mm;align-items:end;"><h1 style="font-size:30pt;margin:0;">Weather:<br>textures and dust</h1><p class="lead" style="margin:0;">The secret glue of ambient and lo-fi records is a quiet bed of noise underneath everything: rain, tape hiss, vinyl crackle. SLOOP generates these for you, without using up a track.</p></div>
  <figure style="margin:2.5mm 0 1.5mm;width:100%;">{I.weather_hero()}</figure>
  <figure style="margin:0 0 1.5mm;width:100%;">{I.weather_strip()}</figure>

  <div class="row" style="grid-template-columns:1.2fr 1fr;gap:9mm;align-items:start;">
    <div>
      <div class="start" style="margin-bottom:2.5mm;"><div class="label">{PIN}starting from here</div>
        <ul><li>Any loop playing (Lesson&nbsp;3's, ideally), or even just a held pad. Any track can be selected; this lesson's settings are global.</li></ul></div>
      <ol class="steps">
        <li><p>Tap <kbd>GLO</kbd> repeatedly until the <span class="v">TEXTURE</span> page shows.</p></li>
        <li><p>Turn <span class="v">SRC</span> to <span class="v">RAIN</span>. Bring <span class="v">LEVEL</span> up until it sits just under the music. Try the other weathers: <span class="v">VINYL</span> (hiss, rumble and crackle), <span class="v">TAPE</span>, <span class="v">WIND</span>, <span class="v">RADIO</span>, <span class="v">ROOM</span>.</p></li>
        <li><p><span class="v">TONE</span> darkens (left) or thins (right) the bed; <span class="v">MOVE</span> makes it breathe, swelling and receding. On the next page, <b>TEXTURE&nbsp;2</b>, <span class="v">RATE</span> sets how long each breath takes, 1 to 16 bars of your tempo.</p></li>
      </ol>
      <p class="note"><b>GLO → TEXTURE</b> is where all of this lives; the texture is saved with your project, and each song section can carry its own.</p>
    </div>
    <div>
      <ol class="steps" style="counter-reset:st 3;margin-top:0;">
        <li><p>One more colour: hold <kbd>FX</kbd> and turn <kbd class="knob">KNOB 2</kbd>, <span class="v">DUST</span>. It runs the whole mix through an old sampler and a worn record: softly driven, fewer bits, a little hiss and crackle while the music plays. A small amount warms everything.</p></li>
      </ol>
      <figure style="margin:0;">{I.dust_meter()}<figcaption style="margin-top:.5mm;">What DUST does to a clean wave as you turn it up: a coarser sample rate, fewer bits, a closing low-pass.</figcaption></figure>
    </div>
  </div>
  {hear("Your loop sitting inside weather: rain breathing beneath it, a little dust on top. It instantly sounds like a finished record.")}
  <div class="row" style="grid-template-columns:1fr 1fr;gap:9mm;">
    <div class="try"><div class="label">{SPARK}try this</div><p>Set TEXTURE&nbsp;2's <span class="v">WHEN</span> to <i>PLAY</i> so the weather fades in and out with the transport: press <kbd>PLAY</kbd> to stop and the rain politely stops with the band.</p></div>
    <div class="mess"><div class="label">{UNDO}made a mess?</div><p>Everything here is reversible by turning it off: SRC to <span class="v">OFF</span> silences the bed entirely (and costs nothing while off), DUST back to 0 cleans the mix. Nothing in this lesson records into your loop.</p></div>
  </div>
  <div class="folio"><span class="n">18</span><span class="t">SLOOP, Gently</span></div>
</section>'''

# ============================================================== PAGE 23 · the pattern
p23 = f'''
<section class="page r2 trk4 odd" data-part="Part 2 · Rhythm and low end">
  <div class="runhead"><span>L6 · drums, gently</span><span class="trk">track 4</span></div>
  <div class="row" style="grid-template-columns:1.1fr 1fr;gap:9mm;align-items:end;"><h2 class="cont" style="font-size:27pt;letter-spacing:-.03em;margin:0;">A pattern to copy, and a take you can count</h2><p class="lead" style="margin:0;font-size:1.02em;">If a blank bar feels like a dare, borrow this one. Sixteen steps make one bar (at the default step size of 1/16), counted <b>1&nbsp;2&nbsp;3&nbsp;4</b> across it; the pattern below is the gentle backbone of half the lo-fi records ever made.</p></div>
  <figure style="margin:3mm auto 0;width:148mm;">{I.pattern_hero()}</figure>
  <p class="note" style="max-width:150mm;">Kick on the "1" and once more on the "and" after beat&nbsp;3, snare on beats 2 and 4, straight hats with every second one kept quiet. Play it slowly on the keys first; it needs only three fingers.</p>

  <h2 style="margin-top:4mm;">A counted four-bar take, start to finish</h2>
  <p style="max-width:150mm;">This is the count-in workflow from Lesson&nbsp;3, written out once in full on an empty loop, so there is no guessing:</p>
  <figure style="margin:0 0 1.5mm;width:150mm;">{I.four_bars()}</figure>
  <div class="row" style="grid-template-columns:1fr 1fr;gap:9mm;">
    <ol class="steps">
      <li><p>On TRACKS, check the tempo (a kindly 75–85 is lovely; keep whatever a free take already set if you have one). Make sure track <span class="tt t4">4</span> is selected.</p></li>
      <li><p>Press <kbd>REC</kbd> while stopped, then set the dials on the armed screen: <span class="v">LENGTH 4&nbsp;bars</span> · <span class="v">START count</span> · <span class="v">QUANT on</span> (on a completely empty loop a fourth dial, <span class="v">MODE</span>, appears first: set it to <i>tempo</i>; once any track holds notes that dial is gone and the set tempo is simply used).</p></li>
      <li><p>Press <kbd>PLAY</kbd>. One bar of clicks counts you in, <span class="scr">4-3-2-1</span> on the screen, then recording begins.</p></li>
    </ol>
    <div>
      <ol class="steps" start="4" style="counter-reset:st 3;">
        <li><p>Play the pattern above, round and round, counting <b>1&nbsp;2&nbsp;3&nbsp;4</b> with the click, for four bars (four counts of four). Perfection not required: quantise tidies the timing.</p></li>
        <li><p>Press <kbd>REC</kbd>. Recording stops and your four-bar beat plays on, looping. (Changed your mind during the count-in? <kbd>REC</kbd> cancels it.)</p></li>
      </ol>
      <div class="aside" style="margin-top:2mm;"><div class="label">{SPARK}Why four bars and not one</div><p>A longer loop leaves room for the pattern to vary: drop the kick syncopation in bars 1 and 2, let it in for bars 3 and 4, and the beat breathes without any extra machinery.</p></div>
    </div>
  </div>
  <div class="folio"><span class="n">23</span><span class="t">SLOOP, Gently</span></div>
</section>'''

# ============================================================== PAGE 35 · the web editor
p35 = f'''
<section class="page r2 trk1 odd" id="ch14" data-part="Part 3 · Performing and keeping it">
  <div class="runhead"><span>14 · the web editor</span><span>SLOOP 2.8.4</span></div>
  <div class="kicker"><span class="chno" style="color:var(--ink)">14</span><span>Chapter fourteen</span></div>
  <div class="row" style="grid-template-columns:1fr 1fr;gap:9mm;align-items:end;"><h1 style="font-size:28pt;margin:0;">The web editor<br>in ten minutes</h1><p class="lead" style="margin:0;font-size:1.02em;">Everything on the FM-1, mirrored live in a browser tab: bigger screen, mouse-draggable knobs, and the doors to backups, your own samples and much more. You met it in Chapter&nbsp;2; here is the guided lap.</p></div>
  <figure style="margin:2mm auto 0;width:118mm;">{I.signal_map()}</figure>

  <div class="row" style="grid-template-columns:1fr 1fr;gap:8mm;align-items:start;">
    <div>
      <ol class="steps" style="margin-top:0;">
        <li><p>Open <a href="https://isod89.github.io/sloop-fm1/webapp/editor/">isod89.github.io/sloop-fm1/webapp/editor</a> in Chrome or Edge, FM-1 on USB, press <b>Connect</b>. The editor follows the device live: turn a knob on the FM-1 and the screen value moves, and vice versa. Every value is a tile you drag up or down like a knob; double-click resets it.</p></li>
        <li><p>Walk the sidebar. <b>Sound</b>: every parameter of the selected track as cards, one per button. <b>Sequencer</b>: the pattern as a grid or piano roll, clickable. <b>Library</b>: a sound library kept in your browser, searchable and taggable, with drag and drop to the device's 32 user slots. <b>Song&nbsp;&amp;&nbsp;sections</b>: load and save A–D, export a song as a file, and the <b>Backup</b> button from Chapter&nbsp;2. <span class="v">LIVE</span>: the whole instrument laid out for performing from the computer, phone or tablet.</p></li>
        <li><p>Record your music into the Mac: on USB the FM-1 is also an <b>audio input</b> called <i>Felucca</i>: everything the headphones hear, dust, texture and punch-ins included, offered to any recording app. The box below walks it through for GarageBand.</p></li>
      </ol>
    </div>
    <div>
      <div class="gb"><div class="label">Recording into GarageBand, step by step</div>
      <p class="tight"><span class="v">1.</span> FM-1 on USB; on the device, hold <kbd>HOME</kbd> → AUDIO → set <b>USB&nbsp;AUDIO</b> to <span class="v">FULL</span>, so the Mac receives a fixed, healthy level whatever the MASTER knob does.</p>
      <p class="tight"><span class="v">2.</span> In GarageBand, open <b>Settings → Audio/MIDI</b> and choose <b>Felucca</b> as the <b>Input Device</b> (your speakers stay the output).</p>
      <p class="tight"><span class="v">3.</span> Create an <b>Audio track</b> (the microphone icon), input channels 1&nbsp;+&nbsp;2 (stereo), and leave software monitoring off so you listen on the FM-1's own output.</p>
      <p class="tight"><span class="v">4.</span> Arm the track, press GarageBand's record button, then press <kbd>PLAY</kbd> on the FM-1 (or play live). Stop both when done: your piece is now audio on the Mac, ready to trim, share, or build on.</p>
      <p class="tight" style="margin-top:1.5mm;">GarageBand's exact menu names shift between versions; the constant parts are the input device named <i>Felucca</i>, a stereo audio track, and USB&nbsp;AUDIO&nbsp;=&nbsp;FULL on the FM-1. One cable carries MIDI, the editor and this audio at once.</p></div>
      <div class="aside"><div class="label">{SPARK}Three small delights</div>
      <p>The editor installs as an offline app (the <i>Install the app</i> link under Connect) so it works without internet. It speaks to an audience too: the <span class="v">LIVE</span> page has a help "?" on every card. And you can try the whole editor with no FM-1 attached by adding <span style="font-family:'IBM Plex Mono'; font-size:.9em;">?mock=1</span> to its address, a pleasant way to explore from the couch.</p></div>
    </div>
  </div>
  <div class="mess" style="column-span:all;"><div class="label">{UNDO}made a mess?</div>
  <p>The editor cannot find the FM-1: Chrome or Edge only, a data cable, no hub, allow MIDI, and close any other app or tab using MIDI, then reload. The audio input does not appear on the Mac: replug the FM-1, and in your recording app rescan audio devices. Flash writes (presets, backups) politely wait until the song is stopped; the editor will ask.</p></div>
  <div class="folio"><span class="n">35</span><span class="t">SLOOP, Gently</span></div>
</section>'''

