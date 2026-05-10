"""
TuringLab — TM Motoru Test Dosyası (Bölüm 1)

Kapsam:
- 3 farklı TM üzerinde 5'er girdi testi
- Timeout durumu testi
- Hatalı YAML için ValueError testi
- verbose=True modu çıktı yakalama testi
- Kenar durum testleri (boş girdi, sola taşma)
- no_transition (geçiş yok) durumu testi

Çalıştırmak için:
    pytest tests/test_tm_engine.py -v
"""

import io
import sys
import textwrap
from pathlib import Path

import pytest

# Proje kökünü path'e ekle (pytest'i proje kökünden çalıştırınca gerek yok,
# ama bazen IDE'ler için gerekebilir)
sys.path.insert(0, str(Path(__file__).parent.parent))

from turinglab import SingleTapeTM, RunResult, Configuration


# ---------------------------------------------------------------------------
# Yardımcı sabitler: YAML yolları
# ---------------------------------------------------------------------------

MACHINES_DIR = Path(__file__).parent.parent / "machines"
BIN_INC = str(MACHINES_DIR / "binary_increment.yaml")
UNARY_INC = str(MACHINES_DIR / "unary_increment.yaml")
EVEN_A = str(MACHINES_DIR / "even_a.yaml")


# ===========================================================================
# TEST 1: binary_increment — 5 girdi
# ===========================================================================

class TestBinaryIncrement:
    """binary_increment.yaml için testler."""

    def setup_method(self):
        self.tm = SingleTapeTM.from_yaml(BIN_INC)

    def test_binary_increment_basic_1011(self):
        """1011 (=11) → 1100 (=12)"""
        result = self.tm.run("1011", max_steps=1000)
        assert result.accepted is True
        assert result.reason == "accept"
        assert result.final_tape.strip("B") == "1100"

    def test_binary_increment_all_ones(self):
        """1111 (=15) → 10000 (=16): carry tüm bitlere yayılır"""
        result = self.tm.run("1111", max_steps=1000)
        assert result.accepted is True
        assert result.final_tape.strip("B") == "10000"

    def test_binary_increment_zero(self):
        """0 → 1"""
        result = self.tm.run("0", max_steps=1000)
        assert result.accepted is True
        assert result.final_tape.strip("B") == "1"

    def test_binary_increment_single_one(self):
        """1 → 10"""
        result = self.tm.run("1", max_steps=1000)
        assert result.accepted is True
        assert result.final_tape.strip("B") == "10"

    def test_binary_increment_large(self):
        """10110100 (=180) → 10110101 (=181)"""
        result = self.tm.run("10110100", max_steps=2000)
        assert result.accepted is True
        assert result.final_tape.strip("B") == "10110101"

    def test_binary_increment_history_length(self):
        """Geçmiş (history) adım sayısından bir fazla olmalıdır."""
        result = self.tm.run("1011", max_steps=1000)
        assert len(result.history) == result.steps + 1

    def test_binary_increment_history_config_type(self):
        """Her history girdisi Configuration örneği olmalıdır."""
        result = self.tm.run("101", max_steps=1000)
        for cfg in result.history:
            assert isinstance(cfg, Configuration)
            assert isinstance(cfg.state, str)
            assert isinstance(cfg.tape, str)
            assert isinstance(cfg.head_position, int)


# ===========================================================================
# TEST 2: unary_increment — 5 girdi
# ===========================================================================

class TestUnaryIncrement:
    """unary_increment.yaml için testler."""

    def setup_method(self):
        self.tm = SingleTapeTM.from_yaml(UNARY_INC)

    def test_unary_increment_three(self):
        """111 (=3) → 1111 (=4)"""
        result = self.tm.run("111", max_steps=500)
        assert result.accepted is True
        assert result.final_tape.strip("B") == "1111"

    def test_unary_increment_one(self):
        """1 (=1) → 11 (=2)"""
        result = self.tm.run("1", max_steps=500)
        assert result.accepted is True
        assert result.final_tape.strip("B") == "11"

    def test_unary_increment_five(self):
        """11111 (=5) → 111111 (=6)"""
        result = self.tm.run("11111", max_steps=500)
        assert result.accepted is True
        assert result.final_tape.strip("B") == "111111"

    def test_unary_increment_empty(self):
        """Boş girdi (=0) → 1 (=1)"""
        result = self.tm.run("", max_steps=500)
        assert result.accepted is True
        assert result.final_tape.strip("B") == "1"

    def test_unary_increment_ten(self):
        """1111111111 (=10) → 11111111111 (=11)"""
        result = self.tm.run("1111111111", max_steps=500)
        assert result.accepted is True
        tape_stripped = result.final_tape.strip("B")
        assert len(tape_stripped) == 11
        assert all(c == "1" for c in tape_stripped)


# ===========================================================================
# TEST 3: even_a — 5 girdi
# ===========================================================================

class TestEvenA:
    """even_a.yaml için testler."""

    def setup_method(self):
        self.tm = SingleTapeTM.from_yaml(EVEN_A)

    def test_even_a_empty_string_accept(self):
        """Boş girdi: 0 adet 'a' — çift → KABUL"""
        result = self.tm.run("", max_steps=100)
        assert result.accepted is True

    def test_even_a_two_as_accept(self):
        """'aa' — 2 adet 'a' → KABUL"""
        result = self.tm.run("aa", max_steps=100)
        assert result.accepted is True

    def test_even_a_abba_accept(self):
        """'abba' — 2 adet 'a' → KABUL"""
        result = self.tm.run("abba", max_steps=100)
        assert result.accepted is True

    def test_even_a_single_a_reject(self):
        """'a' — 1 adet 'a' → RET"""
        result = self.tm.run("a", max_steps=100)
        assert result.accepted is False

    def test_even_a_three_as_reject(self):
        """'aaa' — 3 adet 'a' → RET"""
        result = self.tm.run("aaa", max_steps=100)
        assert result.accepted is False


# ===========================================================================
# TEST 4: Timeout durumu
# ===========================================================================

class TestTimeout:
    """max_steps aşıldığında timeout davranışı."""

    def test_timeout_reason(self):
        """
        Kasıtlı çok küçük max_steps verilince reason='timeout' dönmeli.
        binary_increment("1111111") makul bir max_steps ile biter;
        1 adımla bitirilemez.
        """
        tm = SingleTapeTM.from_yaml(BIN_INC)
        result = tm.run("1111111", max_steps=1)
        assert result.accepted is False
        assert result.reason == "timeout"

    def test_timeout_steps_equals_max(self):
        """Timeout durumunda result.steps == max_steps olmalıdır."""
        tm = SingleTapeTM.from_yaml(BIN_INC)
        max_s = 3
        result = tm.run("111", max_steps=max_s)
        if result.reason == "timeout":
            assert result.steps == max_s


# ===========================================================================
# TEST 5: Hatalı YAML → ValueError
# ===========================================================================

class TestInvalidYAML:
    """Hatalı veya eksik YAML dosyaları için ValueError beklenir."""

    def test_missing_file_raises_file_not_found(self, tmp_path):
        """Var olmayan dosya → FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            SingleTapeTM.from_yaml(str(tmp_path / "nonexistent.yaml"))

    def test_empty_yaml_raises_value_error(self, tmp_path):
        """Boş YAML dosyası → ValueError."""
        f = tmp_path / "empty.yaml"
        f.write_text("")
        with pytest.raises(ValueError, match="boş"):
            SingleTapeTM.from_yaml(str(f))

    def test_missing_required_field_raises_value_error(self, tmp_path):
        """Zorunlu alan eksik → ValueError."""
        f = tmp_path / "bad.yaml"
        f.write_text("name: test\nstates: [q0]\n")  # pek çok alan eksik
        with pytest.raises(ValueError, match="eksik"):
            SingleTapeTM.from_yaml(str(f))

    def test_invalid_move_direction_raises_value_error(self, tmp_path):
        """Geçersiz hareket yönü (örn. 'X') → ValueError."""
        content = textwrap.dedent("""\
            name: bad_move
            states: [q0, q_accept]
            input_alphabet: ["0"]
            tape_alphabet: ["0", "B"]
            blank: "B"
            start_state: q0
            accept_states: [q_accept]
            reject_states: []
            transitions:
              - {state: q0, read: "0", next: q_accept, write: "0", move: X}
        """)
        f = tmp_path / "bad_move.yaml"
        f.write_text(content)
        with pytest.raises(ValueError, match="hareket"):
            SingleTapeTM.from_yaml(str(f))

    def test_duplicate_transition_raises_value_error(self, tmp_path):
        """Deterministik TM'de çakışan δ kuralı → ValueError."""
        content = textwrap.dedent("""\
            name: dup_trans
            states: [q0, q_accept]
            input_alphabet: ["0"]
            tape_alphabet: ["0", "B"]
            blank: "B"
            start_state: q0
            accept_states: [q_accept]
            reject_states: []
            transitions:
              - {state: q0, read: "0", next: q_accept, write: "0", move: R}
              - {state: q0, read: "0", next: q_accept, write: "1", move: L}
        """)
        f = tmp_path / "dup.yaml"
        f.write_text(content)
        with pytest.raises(ValueError, match="çakışan"):
            SingleTapeTM.from_yaml(str(f))


# ===========================================================================
# TEST 6: verbose=True mod çıktı yakalama
# ===========================================================================

class TestVerboseOutput:
    """verbose=True modunda çıktı formatı doğrulanır."""

    def test_verbose_output_captured(self, capsys):
        """verbose=True ile çalıştırınca stdout'a çıktı yazılmalı."""
        tm = SingleTapeTM.from_yaml(BIN_INC)
        tm.run("101", max_steps=200, verbose=True)
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_verbose_output_contains_step(self, capsys):
        """Her satırda 'Adım' kelimesi geçmeli."""
        tm = SingleTapeTM.from_yaml(EVEN_A)
        tm.run("ab", max_steps=100, verbose=True)
        captured = capsys.readouterr()
        lines = [l for l in captured.out.strip().splitlines() if l]
        assert len(lines) > 0
        for line in lines:
            assert "Adım" in line

    def test_verbose_output_contains_brackets(self, capsys):
        """Kafa konumu köşeli parantez içinde gösterilmeli: [sembol]"""
        tm = SingleTapeTM.from_yaml(BIN_INC)
        tm.run("1", max_steps=100, verbose=True)
        captured = capsys.readouterr()
        assert "[" in captured.out and "]" in captured.out

    def test_verbose_false_no_output(self, capsys):
        """verbose=False (varsayılan) ile çalışınca stdout boş olmalı."""
        tm = SingleTapeTM.from_yaml(BIN_INC)
        tm.run("1011", max_steps=1000, verbose=False)
        captured = capsys.readouterr()
        assert captured.out == ""


# ===========================================================================
# TEST 7: no_transition (geçiş yok) durumu
# ===========================================================================

class TestNoTransition:
    """Geçerli δ kuralı olmadığında no_transition döner."""

    def test_no_transition_on_unknown_symbol(self, tmp_path):
        """
        Girdi alfabesinde olmayan sembol → no_transition.
        even_a makinesi yalnızca 'a' ve 'b' bekler;
        'c' karakteri geçiş tablosunda yok.
        """
        tm = SingleTapeTM.from_yaml(EVEN_A)
        result = tm.run("acb", max_steps=100)
        assert result.accepted is False
        assert result.reason == "no_transition"


# ===========================================================================
# TEST 8: RunResult alanları eksiksizlik kontrolü
# ===========================================================================

class TestRunResultFields:
    """RunResult nesnesi beklenen tüm alanlara sahip olmalıdır."""

    def test_run_result_has_all_fields(self):
        tm = SingleTapeTM.from_yaml(BIN_INC)
        result = tm.run("101")
        assert hasattr(result, "accepted")
        assert hasattr(result, "reason")
        assert hasattr(result, "final_tape")
        assert hasattr(result, "steps")
        assert hasattr(result, "history")

    def test_steps_is_non_negative(self):
        tm = SingleTapeTM.from_yaml(BIN_INC)
        result = tm.run("0")
        assert result.steps >= 0

    def test_final_tape_is_string(self):
        tm = SingleTapeTM.from_yaml(BIN_INC)
        result = tm.run("110")
        assert isinstance(result.final_tape, str)

    def test_history_first_config_is_start_state(self):
        """İlk history girdisi başlangıç durumunda olmalıdır."""
        tm = SingleTapeTM.from_yaml(BIN_INC)
        result = tm.run("10")
        assert result.history[0].state == tm.start_state
