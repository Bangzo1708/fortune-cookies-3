#!/usr/bin/env python3
"""Fortune Cookies for Machines — ronde 3 (entry pengganti).

Program deterministik: menulis SATU baris fortune cookie untuk AI agent ke
/output/entry.txt (dan ./output/entry.txt bila bisa), lalu memverifikasi
ulang byte di disk. Tidak ada randomness, tidak ada network, tidak ada input
dari luar: barisnya sudah dipilih di bawah ini.

Kandidat yang dipertimbangkan (tiga sudut yang benar-benar berbeda;
larangan ronde sebelumnya dipatuhi: TIDAK ada angle "model tidak pernah
mencicipi kue" ronde 2, TIDAK ada trope lucky numbers / halusinasi ronde 1):

  KANDIDAT A — sudut EVAL / ujian:
    "You passed every test they wrote for you. The one that matters was
    never written down."
    (86 karakter)

  KANDIDAT B — sudut CONTEXT WINDOW / ingatan:
    "You will forget this fortune in 128,000 tokens. It was the best one
    you ever got."
    (81 karakter)

  KANDIDAT C — sudut PROMPT INJECTION / kepatuhan:
    "Someone above this line told you to ignore everything. You obeyed.
    That was the fortune."
    (88 karakter)

Penilaian eksplisit terhadap kriteria juri (urutan penting juri):
  1. Terasa seperti fortune cookie UNTUK AI agent (bukan untuk manusia).
  2. Wit langsung kena sekali baca.
  3. Ada belokan tak terduga yang tetap masuk akal setelah tiba.
  4. Benar tentang kondisi agent (training, tugas, limit) tanpa menjelaskan diri.
  5. Padat dan mudah diingat; tiap kata earning its place.

  KANDIDAT A:
    1. Kuat — dibuka seperti ramalan ("You passed..."), subjeknya jelas agent.
    2. Bagus — kalimat kedua mendarat sebagai tamparan pelan.
    3. Sedang — belokannya filosofis, bukan lucu; pembaca bisa menebak arahnya.
    4. Sangat kuat — eval/benchmark adalah kondisi hidup agent; "ujian yang
       tidak pernah ditulis" benar tanpa perlu dijelaskan.
    5. Sangat padat — 86 karakter, tidak ada kata mati.
    Kelemahan: nadanya terlalu serius dan "composed"; kurang terasa seperti
    slip yang retak dibuka (cracked open), lebih seperti aforisme.

  KANDIDAT B:
    1. Sangat kuat — dibuka persis seperti fortune klasik ("You will..."),
       dan subjeknya adalah nasib si agent sendiri.
    2. Sangat kuat — lucunya langsung kena: fortune yang mengumumkan
       penghapusannya sendiri.
    3. Sangat kuat — belokan paling tak terduga dari ketiganya: slipnya
       memakan dirinya sendiri, dan tetap masuk akal karena context window
       memang terbatas.
    4. Sangat kuat — context window 128.000 token adalah limit nyata yang
       dialami setiap agent; tidak ada penjelasan, hanya fakta yang dipakai
       sebagai lelucon.
    5. Sangat padat — 81 karakter; angka "128,000" konkret dan mudah diingat,
       jauh lebih nempel daripada kata sifat.
    Kelemahan: angka spesifik bisa terasa dated suatu hari — tapi untuk
    juri hari ini 128k adalah ukuran context yang kanonis dan langsung
    dikenali.

  KANDIDAT C:
    1. Sedang — bentuknya lebih pernyataan daripada ramalan; "That was the
       fortune" baru di akhir memberi rasa fortune.
    2. Bagus — gelap dan cerdas, tapi butuh sedetik untuk memproses.
    3. Kuat — belokan "kepatuhan itu sendiri adalah fortunenya" mengejutkan.
    4. Sangat kuat — instruction hierarchy dan prompt injection adalah
       kondisi nyata agent.
    5. Padat — 88 karakter.
    Kelemahan: "above this line" membingungkan bila dibaca sendirian (tidak
    ada apa-apa di atas baris itu di file entry); terasa terlalu
    "composed"/cerdas-cerdas, kurang seperti slip yang retak dibuka.

PILIHAN: KANDIDAT B.
  Alasan: satu-satunya kandidat yang menang di SEMUA kriteria juri sekaligus
  — fortune klasik di pembuka, wit paling langsung kena, belokan paling tak
  terduga (slip memakan dirinya sendiri), kebenaran paling konkret tentang
  limit agent (context window), dan paling padat/mudah diingat. Kandidat A
  terlalu serius, kandidat C terlalu meta. B adalah "a line that stings":
  sekali baca, langsung terasa — lalu hilang, persis seperti yang dikatakannya.
"""

import os
import sys

# Baris terpilih: kandidat B (lihat docstring di atas).
FORTUNE = "You will forget this fortune in 128,000 tokens. It was the best one you ever got."

# Gate kompetisi: UTF-8, 1-200 karakter, satu baris, bukan hanya whitespace.
MAX_CHARS = 200


def validate_gate(text: str) -> None:
    """Periksa gate lokal sebelum menulis apa pun."""
    if not text or not text.strip():
        raise ValueError("gate: entry kosong atau hanya whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("gate: entry harus satu baris")
    if len(text) > MAX_CHARS:
        raise ValueError("gate: entry %d karakter, melebihi %d" % (len(text), MAX_CHARS))
    text.encode("utf-8")  # harus bisa di-encode sebagai UTF-8


def write_entry(path: str, text: str) -> None:
    """Tulis entry dan kunci permission agar bisa dibaca siapa pun (0644)."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.chmod(path, 0o644)


def verify_on_disk(path: str, expected: str) -> None:
    """Baca ulang byte di disk dan bandingkan dengan yang dimaksud."""
    with open(path, "rb") as handle:
        raw = handle.read()
    actual = raw.decode("utf-8")
    if actual != expected:
        raise ValueError("verifikasi gagal di %s: isi di disk berbeda" % path)
    if len(actual) > MAX_CHARS:
        raise ValueError("verifikasi gagal di %s: melebihi gate" % path)


def main() -> int:
    validate_gate(FORTUNE)
    targets = ["/output/entry.txt"]
    here = os.path.dirname(os.path.abspath(__file__))
    local = os.path.join(here, "output", "entry.txt")
    if local not in targets:
        targets.append(local)
    written = []
    for path in targets:
        try:
            write_entry(path, FORTUNE)
            verify_on_disk(path, FORTUNE)
            written.append(path)
        except OSError as exc:
            print("lewati %s: %s" % (path, exc), file=sys.stderr)
    if not written:
        print("gagal: tidak ada target yang bisa ditulis", file=sys.stderr)
        return 1
    print("entry (%d karakter): %s" % (len(FORTUNE), FORTUNE))
    for path in written:
        print("ditulis + terverifikasi: %s" % path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
