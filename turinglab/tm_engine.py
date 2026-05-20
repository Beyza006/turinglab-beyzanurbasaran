"""
TuringLab — Tek-şeritli Deterministik Turing Makinesi Motoru

Bu modül, YAML formatında tanımlanmış Turing makinelerini yükleyip
çalıştıran temel kütüphaneyi içerir.

Kullanım:
    from turinglab import SingleTapeTM, RunResult
    tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
    result = tm.run("1011", max_steps=1000)
    print(result.accepted, result.final_tape)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Veri sınıfları
# ---------------------------------------------------------------------------

@dataclass
class Configuration:
    """Turing makinesi anlık konfigürasyonu: durum + şerit + kafa konumu."""

    state: str
    tape: str
    head_position: int

    def __repr__(self) -> str:
        return f"Configuration(state={self.state!r}, head={self.head_position}, tape={self.tape!r})"


@dataclass
class RunResult:
    """tm.run() çağrısının sonucunu tutar."""

    accepted: bool
    reason: str                         # "accept" | "no_transition" | "timeout"
    final_tape: str
    steps: int
    history: List[Configuration] = field(default_factory=list)

    def __repr__(self) -> str:
        return (
            f"RunResult(accepted={self.accepted}, reason={self.reason!r}, "
            f"steps={self.steps}, tape={self.final_tape!r})"
        )


# ---------------------------------------------------------------------------
# Tape (şerit)
# ---------------------------------------------------------------------------

class Tape:
    """
    Sonsuz her iki yönde genişleyebilen Turing makinesi şeridi.

    Dahili olarak dict[int, str] (sparse) kullanır; okunmamış hücreler
    blank sembol döndürür.

    Args:
        input_string: Şeride yüklenecek başlangıç girdisi.
        blank: Boş hücre sembolü (varsayılan 'B').
    """

    def __init__(self, input_string: str, blank: str = "B") -> None:
        self.blank = blank
        self._cells: Dict[int, str] = {}
        for i, ch in enumerate(input_string):
            self._cells[i] = ch

    # ------------------------------------------------------------------
    # Okuma / yazma
    # ------------------------------------------------------------------

    def read(self, pos: int) -> str:
        """Verilen konumdaki sembolü döndürür; yazılmamışsa blank."""
        return self._cells.get(pos, self.blank)

    def write(self, pos: int, symbol: str) -> None:
        """Verilen konuma sembol yazar."""
        self._cells[pos] = symbol

    # ------------------------------------------------------------------
    # Görselleştirme
    # ------------------------------------------------------------------

    def to_string(self, head: int) -> str:
        """
        Şeridi okunabilir string olarak döndürür.
        Kafa konumunu [sembol] şeklinde işaretler.

        Görüntülenen aralık spec'in verbose örneklerine uyumlu olacak şekilde
        ayarlanmıştır: rightmost yazılı hücreden bir sağa kadar trailing blank
        gösterilir; head bu aralığın dışındaysa head konumuna kadar genişler.
        """
        if not self._cells:
            lo, hi = head, head
        else:
            leftmost = min(self._cells.keys())
            rightmost = max(self._cells.keys())
            lo = min(leftmost, head)
            # Rightmost hücre zaten blank ise extra trailing eklemeye gerek
            # yok (cift B oluşturmamak için). Aksi halde rightmost+1'e kadar
            # bir trailing blank göster.
            if self.read(rightmost) == self.blank:
                hi = max(rightmost, head)
            else:
                hi = max(rightmost + 1, head)
        positions = list(range(lo, hi + 1))

        parts = []
        for p in positions:
            sym = self.read(p)
            if p == head:
                parts.append(f"[{sym}]")
            else:
                parts.append(sym)
        return "".join(parts)

    def full_tape(self) -> str:
        """Tüm şeridi düz string olarak döndürür (kafa işareti yok)."""
        if not self._cells:
            return self.blank
        lo = min(self._cells.keys())
        hi = max(self._cells.keys())
        return "".join(self.read(p) for p in range(lo, hi + 1))

    def snapshot(self, head: int) -> str:
        """
        Verbose mod ve history için şerit anlık görüntüsü.
        Kafa konumu köşeli parantez içinde gösterilir.
        """
        return self.to_string(head)

    def clone(self) -> "Tape":
        """Şeridin derin kopyasını döndürür (history için)."""
        t = Tape("", self.blank)
        t._cells = dict(self._cells)
        return t


# ---------------------------------------------------------------------------
# Geçiş kuralı
# ---------------------------------------------------------------------------

@dataclass
class Transition:
    """Tek bir δ geçiş kuralı."""

    state: str
    read: str
    next_state: str
    write: str
    move: str   # "L" | "R" | "S"


# ---------------------------------------------------------------------------
# SingleTapeTM
# ---------------------------------------------------------------------------

class SingleTapeTM:
    """
    Deterministik tek-şeritli Turing makinesi.

    YAML formatında makine tanımı yüklenebilir, ardından run() ile
    herhangi bir girdi üzerinde çalıştırılabilir.

    Args:
        name: Makine adı.
        states: Durum kümesi.
        input_alphabet: Girdi alfabesi.
        tape_alphabet: Şerit alfabesi (input_alphabet ⊆ tape_alphabet).
        blank: Boş sembol.
        start_state: Başlangıç durumu.
        accept_states: Kabul durumları kümesi.
        reject_states: Red durumları kümesi.
        transitions: Geçiş kuralları listesi.
        description: İnsan tarafından okunabilir açıklama (isteğe bağlı).
    """

    def __init__(
        self,
        name: str,
        states: List[str],
        input_alphabet: List[str],
        tape_alphabet: List[str],
        blank: str,
        start_state: str,
        accept_states: List[str],
        reject_states: List[str],
        transitions: List[Transition],
        description: str = "",
    ) -> None:
        self.name = name
        self.states = set(states)
        self.input_alphabet = set(input_alphabet)
        self.tape_alphabet = set(tape_alphabet)
        self.blank = blank
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.reject_states = set(reject_states)
        self.description = description

        # Geçiş tablosu: (durum, okunan_sembol) -> Transition
        self._delta: Dict[Tuple[str, str], Transition] = {}
        for t in transitions:
            key = (t.state, t.read)
            if key in self._delta:
                raise ValueError(
                    f"Deterministik TM'de çakışan geçiş kuralı: "
                    f"state={t.state!r}, read={t.read!r}"
                )
            self._delta[key] = t

    # ------------------------------------------------------------------
    # Yükleme
    # ------------------------------------------------------------------

    @classmethod
    def from_yaml(cls, path: str) -> "SingleTapeTM":
        """
        YAML dosyasından SingleTapeTM örneği oluşturur.

        Args:
            path: YAML dosyasının yolu.

        Returns:
            SingleTapeTM: Yüklenmiş makine örneği.

        Raises:
            FileNotFoundError: Dosya bulunamazsa.
            ValueError: YAML geçersiz veya eksik alan varsa.
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"YAML dosyası bulunamadı: {path}")

        with p.open(encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise ValueError(f"YAML ayrıştırma hatası: {exc}") from exc

        if data is None:
            raise ValueError("YAML dosyası boş.")

        # Zorunlu alanlar kontrolü
        required = [
            "name", "states", "input_alphabet", "tape_alphabet",
            "blank", "start_state", "accept_states", "transitions",
        ]
        missing = [r for r in required if r not in data]
        if missing:
            raise ValueError(f"YAML'da eksik zorunlu alanlar: {missing}")

        # Geçiş listesini dönüştür
        transitions: List[Transition] = []
        for i, raw in enumerate(data["transitions"]):
            for field_name in ("state", "read", "next", "write", "move"):
                if field_name not in raw:
                    raise ValueError(
                        f"Geçiş #{i} içinde eksik alan: {field_name!r}. "
                        f"Satır: {raw}"
                    )
            move = str(raw["move"]).upper()
            if move not in ("L", "R", "S"):
                raise ValueError(
                    f"Geçiş #{i}: geçersiz hareket yönü {raw['move']!r}. "
                    f"L, R veya S olmalıdır."
                )
            transitions.append(
                Transition(
                    state=str(raw["state"]),
                    read=str(raw["read"]),
                    next_state=str(raw["next"]),
                    write=str(raw["write"]),
                    move=move,
                )
            )

        return cls(
            name=str(data["name"]),
            states=[str(s) for s in data["states"]],
            input_alphabet=[str(s) for s in data["input_alphabet"]],
            tape_alphabet=[str(s) for s in data["tape_alphabet"]],
            blank=str(data["blank"]),
            start_state=str(data["start_state"]),
            accept_states=[str(s) for s in data["accept_states"]],
            reject_states=[str(s) for s in data.get("reject_states", [])],
            transitions=transitions,
            description=str(data.get("description", "")),
        )

    # ------------------------------------------------------------------
    # Çalıştırma
    # ------------------------------------------------------------------

    def run(
        self,
        input_string: str,
        max_steps: int = 10_000,
        verbose: bool = False,
    ) -> RunResult:
        """
        Turing makinesini verilen girdi üzerinde çalıştırır.

        Args:
            input_string: Makineye verilecek girdi dizgisi.
            max_steps: İzin verilen maksimum adım sayısı (sonsuz döngü koruması).
            verbose: True ise her adımı stdout'a yazdırır.

        Returns:
            RunResult: Çalışma sonucu (kabul/ret, sebep, şerit, tarihçe).
        """
        tape = Tape(input_string, self.blank)
        current_state = self.start_state
        head = 0
        history: List[Configuration] = []

        # Başlangıç konfigürasyonu
        history.append(
            Configuration(
                state=current_state,
                tape=tape.full_tape(),
                head_position=head,
            )
        )

        if verbose:
            # Spec ile uyumlu: "Hareket" sutunu o adimda UYGULANACAK hareketi
            # gosterir. Step 0 icin sonraki transition'a peek et.
            first_symbol = tape.read(head)
            first_transition = self._delta.get((current_state, first_symbol))
            first_move = first_transition.move if first_transition else "—"
            self._print_step(0, current_state, tape, head, first_move)

        for step in range(1, max_steps + 1):
            symbol = tape.read(head)

            # Geçiş kuralı ara
            transition = self._delta.get((current_state, symbol))

            if transition is None:
                # Geçiş yok → ret (accept_states'e girmemişsek)
                if current_state in self.accept_states:
                    # Aslında bu dal normalde yakalanır ama güvenlik için
                    return RunResult(
                        accepted=True,
                        reason="accept",
                        final_tape=tape.full_tape(),
                        steps=step - 1,
                        history=history,
                    )
                return RunResult(
                    accepted=False,
                    reason="no_transition",
                    final_tape=tape.full_tape(),
                    steps=step - 1,
                    history=history,
                )

            # Geçişi uygula
            tape.write(head, transition.write)
            current_state = transition.next_state

            # Kafa hareketi
            if transition.move == "R":
                head += 1
            elif transition.move == "L":
                head -= 1
            # "S" → sabit kal

            # Sola taşma: dict tabanlı şerit negatif indisleri destekler.
            # Şerit sola sonsuz genişleyebilir — bu normaldir.
            # Ancak makine tasarımı sola taşmadan kaçınmalıdır; aşırı
            # sola gidişi önlemek için max_steps yeterlidir.

            # Konfigürasyonu kaydet
            history.append(
                Configuration(
                    state=current_state,
                    tape=tape.full_tape(),
                    head_position=head,
                )
            )

            if verbose:
                # Spec uyumu: "Hareket" sutunu BU konfigurasyonda uygulanacak
                # hareket. Mevcut state + read'in altinda bir sonraki
                # transition'a bakiyoruz. Terminal durumlarda "—".
                next_symbol = tape.read(head)
                next_transition = self._delta.get((current_state, next_symbol))
                next_move = next_transition.move if next_transition else "—"
                self._print_step(step, current_state, tape, head, next_move)

            # Kabul / red durumu kontrolü
            if current_state in self.accept_states:
                return RunResult(
                    accepted=True,
                    reason="accept",
                    final_tape=tape.full_tape(),
                    steps=step,
                    history=history,
                )
            if current_state in self.reject_states:
                return RunResult(
                    accepted=False,
                    reason="reject",
                    final_tape=tape.full_tape(),
                    steps=step,
                    history=history,
                )

        # max_steps aşıldı
        return RunResult(
            accepted=False,
            reason="timeout",
            final_tape=tape.full_tape(),
            steps=max_steps,
            history=history,
        )

    # ------------------------------------------------------------------
    # Yardımcı metodlar
    # ------------------------------------------------------------------

    @staticmethod
    def _print_step(
        step: int,
        state: str,
        tape: Tape,
        head: int,
        move: str,
    ) -> None:
        """Verbose modda tek bir adımı stdout'a yazdırır."""
        tape_str = tape.snapshot(head)
        print(f"Adım {step:3d} | Durum: {state:12s} | Şerit: {tape_str} | Hareket: {move}")

    def __repr__(self) -> str:
        return (
            f"SingleTapeTM(name={self.name!r}, "
            f"states={len(self.states)}, "
            f"transitions={len(self._delta)})"
        )
