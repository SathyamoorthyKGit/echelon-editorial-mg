import numpy as np, wave

SR = 48000
DUR = 86.5
N = int(SR * DUR)

def load(p, n=None):
    w = wave.open(p)
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    if n is not None:
        if len(x) < n:
            x = np.pad(x, ((0, n - len(x)), (0, 0)))
        else:
            x = x[:n]
    return x

def wr(p, x):
    o = wave.open(p, 'wb'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); o.close()

speech = load('audio/speech.wav', N)
bgm_raw = load('audio/bgm_src.wav')
# trim a clean 86.5s bed starting at 0:00 (track has no vocals, intro works as-is)
bgm = bgm_raw[:N] if len(bgm_raw) >= N else np.pad(bgm_raw, ((0, N - len(bgm_raw)), (0, 0)))
bgm = bgm / (np.abs(bgm).max() + 1e-9)

sfx_g = load('audio/sfx_graphics.wav', N)
sfx_f = load('audio/sfx_footage.wav', N)
sfx_all = sfx_g + sfx_f

# --- sidechain duck: envelope-follow the speech track, drop BGM under it ---
env = np.abs(speech).max(1)
hop = 240  # 5ms @ 48k
hop_env = np.array([env[i:i+hop].max() for i in range(0, len(env), hop)]) + 1e-9
db = 20 * np.log10(hop_env)
gate = (db > -38).astype(np.float32)  # speech present
# attack/release smoothing on the gate (fast duck-down, slower recover)
smoothed = np.zeros_like(gate)
atk, rel = 0.25, 0.08  # per-hop coefficients (hop=5ms)
cur = 0.0
for i, g in enumerate(gate):
    cur = cur + atk * (g - cur) if g > cur else cur + rel * (g - cur)
    smoothed[i] = cur
duck_db = -9.0  # how far music ducks under voice
gain_db = smoothed * duck_db
gain_lin = 10 ** (gain_db / 20)
gain_full = np.repeat(gain_lin, hop)[:N]
if len(gain_full) < N:
    gain_full = np.pad(gain_full, (0, N - len(gain_full)), mode='edge')
music_ducked = bgm * (0.5 * gain_full[:, None] + 0.5) * 10 ** (-16 / 20)  # base bed level -16dBFS peak-ish, ducked further under VO

wr('audio/WF_H02_Music_bed_ducked_BuildingTomorrow.wav', music_ducked)
wr('audio/WF_H02_SFX_all_stem.wav', sfx_all)
wr('audio/WF_H02_SFX_graphics_stem.wav', sfx_g)
wr('audio/WF_H02_SFX_footage_cuts_stem.wav', sfx_f)

music_sfx = music_ducked + sfx_all
wr('audio/WF_H02_Music+SFX_stem.wav', music_sfx / max(1.0, np.abs(music_sfx).max()))

voice_sfx = speech * 10 ** (-2/20) + sfx_all
wr('audio/WF_H02_Voice+SFX_mix.wav', voice_sfx / max(1.0, np.abs(voice_sfx).max()))

full = speech * 10 ** (-2/20) + sfx_all + music_ducked
pk = np.abs(full).max()
if pk > 0.98:
    full = full * (0.98 / pk)
wr('audio/WF_H02_Full_mix_prenorm.wav', full)
print('peak pre-norm', pk, 'duration', N/SR)
