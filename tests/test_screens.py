from types import SimpleNamespace

from dx4000_lcd.screens.network import NetworkScreen
from dx4000_lcd.screens.torrent import TorrentScreen
from dx4000_lcd.screens.disk import DiskScreen
from dx4000_lcd.screens.status import StatusScreen
from dx4000_lcd.screens.storage import StorageScreen
from dx4000_lcd.screens.system import SystemScreen
from dx4000_lcd.screens.alert import AlertScreen
from dx4000_lcd.icons import BAR_20, BAR_40, BAR_60, BAR_80, TEMP, FAN, DOWNLOAD, UPLOAD
from dx4000_lcd.bar import render_bar
from dx4000_lcd.cgram import CGRAM_GLYPHS, load_cgram
from dx4000_lcd.tokens import (
    TemperatureToken, PercentToken, SpeedToken, BytesToken, DiskToken,
    StateToken, CountToken, LabelToken, LoadToken, FanToken,
    ValueToken, DirectionToken, CapacityToken,
)
from dx4000_lcd.layouts import (
    layout_standard_2x2, layout_status, layout_disk, layout_system,
    layout_network, layout_torrent, layout_storage, layout_storage_mergerfs,
    layout_alert,
)


# ── icons ──────────────────────────────────────────────────────────

def test_icons_are_exact_chr07():
    assert BAR_20 == chr(0)
    assert BAR_40 == chr(1)
    assert BAR_60 == chr(2)
    assert BAR_80 == chr(3)
    assert TEMP == chr(4)
    assert FAN == chr(5)
    assert DOWNLOAD == chr(6)
    assert UPLOAD == chr(7)


def test_icons_no_legacy_aliases():
    import dx4000_lcd.icons as icons_module
    exports = [n for n in dir(icons_module) if not n.startswith('_')]
    assert set(exports) == {"BAR_20", "BAR_40", "BAR_60", "BAR_80", "TEMP", "FAN", "DOWNLOAD", "UPLOAD"}


# ── cgram ──────────────────────────────────────────────────────────

def test_cgram_slots_0_to_7():
    assert set(CGRAM_GLYPHS.keys()) == {0, 1, 2, 3, 4, 5, 6, 7}


def test_cgram_slot_mapping():
    assert CGRAM_GLYPHS[0] is not None  # BAR_20
    assert CGRAM_GLYPHS[1] is not None  # BAR_40
    assert CGRAM_GLYPHS[2] is not None  # BAR_60
    assert CGRAM_GLYPHS[3] is not None  # BAR_80
    assert CGRAM_GLYPHS[4] is not None  # TEMP
    assert CGRAM_GLYPHS[5] is not None  # FAN
    assert CGRAM_GLYPHS[6] is not None  # DOWNLOAD
    assert CGRAM_GLYPHS[7] is not None  # UPLOAD


def test_cgram_bars_are_slots_0_3():
    assert CGRAM_GLYPHS[0] is not None
    assert CGRAM_GLYPHS[1] is not None
    assert CGRAM_GLYPHS[2] is not None
    assert CGRAM_GLYPHS[3] is not None


def test_load_cgram_calls_set_char():
    from unittest.mock import MagicMock
    mock_lcd = MagicMock()
    load_cgram(mock_lcd)
    assert mock_lcd.set_char.call_count == 8
    for slot in range(8):
        mock_lcd.set_char.assert_any_call(slot, CGRAM_GLYPHS[slot])


# ── bar ──────────────────────────────────────────────────────────────

def test_bar_never_chr4():
    for pct in [0, 5, 12.5, 25, 33.3, 50, 62.7, 75, 88, 99, 100]:
        for w in [1, 5, 9, 10, 16]:
            result = render_bar(pct, w)
            assert chr(4) not in result, f"chr(4) found at pct={pct}, width={w}: {result!r}"


def test_bar_uses_bar_slots():
    result = render_bar(100, 9)
    assert all(c in [BAR_20, BAR_40, BAR_60, BAR_80, " "] for c in result), \
        f"Unexpected chars in bar: {result!r}"


def test_bar_full_width_no_chr4():
    result = render_bar(100, 16)
    assert chr(4) not in result


def test_bar_zero_percent():
    result = render_bar(0, 9)
    assert chr(4) not in result
    assert len(result) == 9


def test_bar_clamps_percent():
    r1 = render_bar(-10, 9)
    r2 = render_bar(150, 9)
    assert chr(4) not in r1
    assert chr(4) not in r2


def test_bar_render_bar_is_sole_generator():
    assert hasattr(render_bar, '__call__')


# ── tokens ─────────────────────────────────────────────────────────

def test_temperature_token():
    assert TemperatureToken.render(31) == " 31C"
    assert TemperatureToken.render(None) == "  --"
    assert TemperatureToken.render(0) == "  0C"


def test_percent_token():
    assert PercentToken.render(13) == " 13%"
    assert PercentToken.render(None) == "  --"
    assert PercentToken.render(100) == "100%"


def test_speed_token():
    assert "0B/s" in SpeedToken.render(0)
    assert "M/s" in SpeedToken.render(12_400_000)
    assert SpeedToken.render(None) == "    0B/s"


def test_bytes_token():
    assert "B" in BytesToken.render(500)
    assert "M" in BytesToken.render(500 * 1024 ** 2)
    assert BytesToken.render(None) == "    --"


def test_disk_token():
    assert DiskToken.render("sda") == " sda"
    assert DiskToken.render("/dev/sda") == " sda"
    assert DiskToken.render(None) == "  --"


def test_state_token():
    assert StateToken.render("ok") == "OK"
    assert StateToken.render("warn") == "WARN"
    assert StateToken.render("error") == "FAIL"
    assert StateToken.render(None) == "    --"


def test_count_token():
    assert CountToken.render(3) == "  3"
    assert CountToken.render(None) == " --"


def test_label_token():
    assert LabelToken.render("CPU") == "CPU "
    assert LabelToken.render("CPU_TEMP") == "CPU_"


def test_load_token():
    assert "L1.23" in LoadToken.render(1.23)
    assert LoadToken.render(None) == "   --"


def test_fan_token():
    assert FanToken.render(1200) == "1K"
    assert FanToken.render(0) == "   --"
    assert FanToken.render(None) == "   --"


def test_value_token():
    assert ValueToken.render(42.5) is not None
    assert ValueToken.render(None) == "    --"


def test_direction_token():
    assert DirectionToken.render("down") == "DOWN"
    assert DirectionToken.render("up") == "UP  "
    assert DirectionToken.render(None) == "  --"


def test_capacity_token():
    assert CapacityToken.render(None) == "    --"
    assert CapacityToken.render(0) is not None


def test_all_tokens_have_render():
    tokens = [
        TemperatureToken, PercentToken, SpeedToken, BytesToken, DiskToken,
        StateToken, CountToken, LabelToken, LoadToken, FanToken,
        ValueToken, DirectionToken, CapacityToken,
    ]
    for t in tokens:
        assert hasattr(t, "render") and callable(t.render)


# ── layouts ────────────────────────────────────────────────────────

def test_layouts_line_length():
    families = [
        layout_standard_2x2("CPU", "31C", "FAN", "1K"),
        layout_status("31C", "1K", "44C", "13%"),
        layout_disk("sda", "44C", "OK"),
        layout_system("32%", "31C", "42%", "L1.23"),
        layout_network("12.4M/s", "1.2M/s"),
        layout_torrent("TOR IDLE", "DOWN 0B/s"),
        layout_storage("13%", "3.5T"),
        layout_storage_mergerfs("13%", "3.5T", "10T"),
        layout_alert("DISK", "WARN"),
    ]
    for pair in families:
        for line in pair:
            assert len(line) <= 16, f"Line too long: {line!r} ({len(line)})"


# ── screens ────────────────────────────────────────────────────────

def test_status_screen():
    cpu = SimpleNamespace(temp_c=31)
    fan = SimpleNamespace(rpm=1200)
    disks = [SimpleNamespace(name="sda", temp_c=44)]
    storage = SimpleNamespace(used_pct=13)
    out = StatusScreen().render(SimpleNamespace(cpu=cpu, fan=fan, disks=disks, storage=storage))
    assert len(out.line1) == 16, f"line1 len {len(out.line1)}"
    assert len(out.line2) == 16, f"line2 len {len(out.line2)}"
    assert "31C" in out.line1
    assert "FAN" in out.line1
    assert "44C" in out.line2
    assert "STO" in out.line2
    assert "13" in out.line2


def test_status_missing():
    out = StatusScreen().render(SimpleNamespace(cpu=None, fan=SimpleNamespace(rpm=None), disks=[], storage=None))
    assert "FAN" in out.line1
    assert "--" in out.line1
    assert "--" in out.line2


def test_disk_screen_hottest():
    cool = SimpleNamespace(name="sda", temp_c=30, health="ok")
    hot = SimpleNamespace(name="sdb", temp_c=48, health="ok")
    out = DiskScreen().render(SimpleNamespace(disks=[cool, hot]))
    assert "sdb" in out.line1
    assert "48C" in out.line1
    assert "OK" in out.line2


def test_disk_screen_no_data():
    out = DiskScreen().render(SimpleNamespace(disks=[]))
    assert "NO DATA" in out.line2


def test_system_screen():
    cpu = SimpleNamespace(usage_pct=32, temp_c=31, load_1m=1.23)
    memory = SimpleNamespace(used_pct=42)
    out = SystemScreen().render(SimpleNamespace(cpu=cpu, memory=memory))
    assert "CPU" in out.line1
    assert "32%" in out.line1
    assert "31C" in out.line1
    assert "RAM" in out.line2
    assert "42%" in out.line2
    assert "L1.23" in out.line2 or "L1.2" in out.line2


def test_network_screen():
    state = SimpleNamespace(network=SimpleNamespace(rx_bps=0, tx_bps=0))
    out = NetworkScreen().render(state)
    assert len(out.line1) == 16
    assert len(out.line2) == 16
    assert DOWNLOAD in out.line1
    assert UPLOAD in out.line2


def test_torrent_offline():
    out = TorrentScreen().render(SimpleNamespace(torrent=None))
    assert "TOR OFFLINE" in out.line1
    assert len(out.line1) == 16


def test_torrent_idle():
    t = SimpleNamespace(active_torrents=0, dl_speed=0)
    out = TorrentScreen().render(SimpleNamespace(torrent=t))
    assert "TOR IDLE" in out.line1
    assert "0B/s" in out.line2


def test_torrent_active():
    t = SimpleNamespace(active_torrents=3, dl_speed=12_400_000)
    out = TorrentScreen().render(SimpleNamespace(torrent=t))
    assert "ACTIVE" in out.line1
    assert "12" in out.line2
    assert "ubuntu" not in out.line1 + out.line2
    assert "eta" not in (out.line1 + out.line2).lower()


def test_storage_standard():
    out = StorageScreen().render(SimpleNamespace(
        storage=SimpleNamespace(used_pct=13, used_bytes=1_000_000_000_000,
                                free_bytes=8_000_000_000_000, total_bytes=9_000_000_000_000)
    ))
    assert "POOL" in out.line1
    assert "USED" in out.line1
    assert "FREE" in out.line2
    assert len(out.line1) <= 16
    assert len(out.line2) <= 16


def test_storage_mergerfs():
    out = StorageScreen().render(SimpleNamespace(
        storage=SimpleNamespace(used_pct=13, used_bytes=1_000_000_000_000,
                                free_bytes=8_000_000_000_000, total_bytes=9_000_000_000_000, mergerfs=True)
    ))
    assert "POOL" in out.line1
    assert "USED" in out.line1
    assert "FREE" in out.line2


def test_storage_missing():
    out = StorageScreen().render(SimpleNamespace(storage=None))
    assert len(out.line1) == 16
    assert len(out.line2) == 16


def test_alert_disk_warn():
    health = SimpleNamespace(value="warn")
    alert = SimpleNamespace(source="disk", health=health, temp_c=None, message="")
    out = AlertScreen().render(alert)
    assert "! DISK" in out.line1
    assert "WARN" in out.line1
    assert len(out.line1) <= 16


def test_alert_with_temp():
    health = SimpleNamespace(value="warn")
    alert = SimpleNamespace(source="disk", health=health, temp_c=48, message="")
    out = AlertScreen().render(alert)
    assert "C" in out.line2


def test_all_screen_lines_leq16():
    screens_and_states = [
        (StatusScreen(), SimpleNamespace(cpu=SimpleNamespace(temp_c=31), fan=SimpleNamespace(rpm=1200),
                        disks=[SimpleNamespace(name="sda", temp_c=44)], storage=SimpleNamespace(used_pct=13))),
        (DiskScreen(), SimpleNamespace(disks=[SimpleNamespace(name="sda", temp_c=44, health="ok")])),
        (SystemScreen(), SimpleNamespace(cpu=SimpleNamespace(usage_pct=32, temp_c=31), memory=SimpleNamespace(used_pct=42))),
        (NetworkScreen(), SimpleNamespace(network=SimpleNamespace(rx_bps=0, tx_bps=0))),
        (TorrentScreen(), SimpleNamespace(torrent=None)),
        (StorageScreen(), SimpleNamespace(storage=SimpleNamespace(used_pct=13, used_bytes=0, free_bytes=0, total_bytes=0))),
        (AlertScreen(), SimpleNamespace(source="disk", health=SimpleNamespace(value="warn"), temp_c=48, message="test")),
    ]
    for screen, state in screens_and_states:
        out = screen.render(state)
        assert len(out.line1) <= 16, f"{screen.__class__.__name__} line1 len {len(out.line1)}: {out.line1!r}"
        assert len(out.line2) <= 16, f"{screen.__class__.__name__} line2 len {len(out.line2)}: {out.line2!r}"


def test_torrent_no_names_eta_progress_consumed():
    t = SimpleNamespace(active_torrents=3, dl_speed=12_400_000,
                       torrent_name="ubuntu.iso", eta=3600, progress=50.0)
    out = TorrentScreen().render(SimpleNamespace(torrent=t))
    assert "ubuntu" not in (out.line1 + out.line2)
    assert "eta" not in (out.line1 + out.line2).lower()
    assert "50" not in out.line1
