"""Ultra-lightweight synthesizer for Ben 10 / Omnitrix audio sound effects.

Generates pure math WAV audio files without external dependencies (pure Python standard library).
Total package size is < 50 KB.
"""

from __future__ import annotations

import io
import math
from pathlib import Path
import struct
import wave

SAMPLE_RATE = 22050


def synthesize_wav(
    sample_rate: int,
    duration_s: float,
    freq_func,
    amp_func,
) -> bytes:
    """Synthesize mono 16-bit PCM WAV bytes from frequency and amplitude envelope functions."""
    num_samples = int(sample_rate * duration_s)
    phase = 0.0
    buf = io.BytesIO()

    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        for i in range(num_samples):
            t = i / sample_rate
            progress = i / max(1, num_samples - 1)

            # Instantaneous frequency and amplitude
            freq = freq_func(t, progress)
            amp = amp_func(t, progress)

            phase += 2.0 * math.pi * freq / sample_rate
            val = math.sin(phase) * amp
            # Soft clamp
            val = max(-1.0, min(1.0, val))
            sample = int(val * 32767 * 0.75)
            wf.writeframes(struct.pack("<h", sample))

    return buf.getvalue()


def make_dial_turn() -> bytes:
    """Futuristic high-tech bezel mechanical click / blip (45ms)."""
    duration = 0.045

    def freq_func(t: float, p: float) -> float:
        # Rapid pitch rise: 1200 Hz to 2400 Hz
        return 1200.0 + (1200.0 * p)

    def amp_func(t: float, p: float) -> float:
        # Sharp transient attack with exponential decay
        return math.exp(-6.0 * p)

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_alien_select() -> bytes:
    """Iconic Omnitrix alien selection & lock-in power surge (220ms)."""
    duration = 0.22

    def freq_func(t: float, p: float) -> float:
        # Three-tier galvanic crescendo: 400 -> 800 -> 1600 Hz
        return 400.0 + 1200.0 * (p ** 1.5)

    def amp_func(t: float, p: float) -> float:
        # Pulsing modulation with resonant swell
        pulse = 0.8 + 0.2 * math.sin(2.0 * math.pi * 30.0 * t)
        envelope = math.sin(math.pi * p) ** 0.8
        return pulse * envelope

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_shockwave() -> bytes:
    """Sub-bass alien energy pulse / shockwave boom (240ms)."""
    duration = 0.24

    def freq_func(t: float, p: float) -> float:
        # Deep downward sub-frequency sweep: 220 Hz down to 55 Hz
        return 220.0 - 165.0 * (p ** 0.5)

    def amp_func(t: float, p: float) -> float:
        # High impact transient with resonant tail
        return math.exp(-4.5 * p)

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_radar_ping() -> bytes:
    """Clear acoustic sonar/radar ping for BLE detection (120ms)."""
    duration = 0.12

    def freq_func(t: float, p: float) -> float:
        return 1760.0  # High A note (pure sine wave)

    def amp_func(t: float, p: float) -> float:
        return math.exp(-7.0 * p)

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_beep() -> bytes:
    """Futuristic UI interaction feedback blip (65ms)."""
    duration = 0.065

    def freq_func(t: float, p: float) -> float:
        return 1100.0 if p < 0.5 else 1450.0

    def amp_func(t: float, p: float) -> float:
        return math.exp(-4.0 * p)

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_error() -> bytes:
    """Omnitrix low-charge / timeout / fault warning buzz (180ms)."""
    duration = 0.18

    def freq_func(t: float, p: float) -> float:
        # Low frequency flutter
        flutter = 15.0 * math.sin(2.0 * math.pi * 45.0 * t)
        return 160.0 + flutter

    def amp_func(t: float, p: float) -> float:
        return math.exp(-3.0 * p)

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_popup() -> bytes:
    """Omnitrix mechanical core spring pop-up & pneumatic latch (160ms)."""
    duration = 0.16

    def freq_func(t: float, p: float) -> float:
        # Quick pneumatic swoosh then sharp mechanical latch click
        if p < 0.4:
            return 250.0 + 600.0 * (p / 0.4)
        else:
            return 1800.0 + 1200.0 * math.sin(2.0 * math.pi * 50.0 * (t - 0.064))

    def amp_func(t: float, p: float) -> float:
        if p < 0.4:
            return 0.7 * (p / 0.4)
        return 0.9 * math.exp(-12.0 * (p - 0.4))

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_transform() -> bytes:
    """Iconic heroic transformation slam & alien energy shockwave (450ms)."""
    duration = 0.45

    def freq_func(t: float, p: float) -> float:
        # Heavy sub-bass slam dropping to 45Hz + rising plasma harmonic surge
        sub = 180.0 * math.exp(-6.0 * p) + 45.0
        surge = 400.0 + 1400.0 * (p ** 2.0)
        return (sub * 0.4) + (surge * 0.6)

    def amp_func(t: float, p: float) -> float:
        # Huge initial impact shockwave with sustained glowing resonance
        impact = math.exp(-3.5 * p)
        res = 0.3 * math.sin(math.pi * p)
        return min(1.0, impact + res)

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_recharge() -> bytes:
    """Galvanic Omnitrix recharge chime (350ms, 4 ascending crystal notes)."""
    duration = 0.35
    notes = [587.33, 739.99, 880.0, 1174.66]  # D5, F#5, A5, D6

    def freq_func(t: float, p: float) -> float:
        idx = min(3, int(p * 4))
        return notes[idx]

    def amp_func(t: float, p: float) -> float:
        note_p = (p * 4) % 1.0
        return math.exp(-3.5 * note_p) * 0.85

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_timeout() -> bytes:
    """Omnitrix energy timeout / revert warning alarm pulses (320ms)."""
    duration = 0.32

    def freq_func(t: float, p: float) -> float:
        # 4 urgent pulsing alarm beeps
        pulse_idx = int(p * 4)
        return 1760.0 if pulse_idx % 2 == 0 else 2093.0

    def amp_func(t: float, p: float) -> float:
        sub_p = (p * 4) % 1.0
        return 0.8 * math.exp(-5.0 * sub_p)

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_self_destruct() -> bytes:
    """Omnitrix S.D.M. Emergency Self-Destruct Klaxon Siren (480ms)."""
    duration = 0.48

    def freq_func(t: float, p: float) -> float:
        # Oscillating emergency alarm siren
        return 650.0 + 350.0 * math.sin(2.0 * math.pi * 5.0 * t)

    def amp_func(t: float, p: float) -> float:
        return 0.85 * (0.8 + 0.2 * math.sin(2.0 * math.pi * 10.0 * t))

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_dna_scan() -> bytes:
    """Extraterrestrial DNA scanner radar frequency sweep (300ms)."""
    duration = 0.30

    def freq_func(t: float, p: float) -> float:
        # Sci-fi warble beam
        base = 800.0 + 600.0 * math.sin(2.0 * math.pi * 8.0 * t)
        return base + 100.0 * math.sin(2.0 * math.pi * 32.0 * t)

    def amp_func(t: float, p: float) -> float:
        return 0.75 * math.sin(math.pi * p)

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def make_master_control() -> bytes:
    """Omnitrix Master Control unlocked heroic fanfare (420ms)."""
    duration = 0.42
    fanfare = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6

    def freq_func(t: float, p: float) -> float:
        idx = min(3, int(p * 4))
        return fanfare[idx]

    def amp_func(t: float, p: float) -> float:
        sub_p = (p * 4) % 1.0
        return 0.9 * math.exp(-2.5 * sub_p)

    return synthesize_wav(SAMPLE_RATE, duration, freq_func, amp_func)


def generate_all_sounds(output_dir: Path) -> dict[str, Path]:
    """Generate and write all sound effect files to destination directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    sound_generators = {
        "dial_turn.wav": make_dial_turn,
        "alien_select.wav": make_alien_select,
        "shockwave.wav": make_shockwave,
        "radar_ping.wav": make_radar_ping,
        "beep.wav": make_beep,
        "error.wav": make_error,
        "popup.wav": make_popup,
        "transform.wav": make_transform,
        "recharge.wav": make_recharge,
        "timeout.wav": make_timeout,
        "self_destruct.wav": make_self_destruct,
        "dna_scan.wav": make_dna_scan,
        "master_control.wav": make_master_control,
    }

    generated_paths = {}
    total_bytes = 0

    print("Generating ultra-lightweight Omnitrix sound assets...")
    for filename, gen_fn in sound_generators.items():
        data = gen_fn()
        out_file = output_dir / filename
        out_file.write_bytes(data)
        file_size = len(data)
        total_bytes += file_size
        generated_paths[out_file.stem] = out_file
        print(f"  [+] {filename:<18} ({file_size / 1024:.1f} KB)")

    print(f"Total Sound Package Size: {total_bytes / 1024:.1f} KB (Zero external dependencies!)\n")
    return generated_paths


if __name__ == "__main__":
    assets_sounds = Path(__file__).resolve().parent.parent / "assets" / "sounds"
    generate_all_sounds(assets_sounds)
