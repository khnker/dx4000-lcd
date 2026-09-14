from types import SimpleNamespace

from dx4000_lcd.screens.network import NetworkScreen
from dx4000_lcd.screens.torrent import TorrentScreen
from dx4000_lcd.screens.disk import DiskScreen
from dx4000_lcd.screens.status import StatusScreen
from dx4000_lcd.screens.storage import StorageScreen
from dx4000_lcd.screens.system import SystemScreen
from dx4000_lcd.screens.alert import AlertScreen
from dx4000_lcd.icons import DOWNLOAD, UPLOAD


def _out(screen, state, **kwargs):
    return screen.render(state, **kwargs) if kwargs else screen.render(state)


def test_network_shows_traffic_not_ip():
    state = SimpleNamespace(network=SimpleNamespace(rx_bps=0, tx_bps=0, ip="10.0.0.1"))
    out = NetworkScreen().render(state)
    assert len(out.line1) == 16
    assert len(out.line2) == 16
    assert "10.0.0.1" not in out.line1
    assert "10.0.0.1" not in out.line2
    assert "IDLE" not in out.line1
    assert "IDLE" not in out.line2
    assert DOWNLOAD in out.line1
    assert UPLOAD in out.line2
    assert "0B/s" in out.line1
    assert "0B/s" in out.line2


def test_torrent_offline_idle_active():
    screen = TorrentScreen()

    off = screen.render(SimpleNamespace(torrent=None), name_index=3)
    assert len(off.line1) == 16
    assert "TOR OFFLINE" in off.line1
    assert off.line2.strip() == "QBIT ERROR"
    assert "■" in off.line1

    idle = screen.render(
        SimpleNamespace(torrent=SimpleNamespace(active_torrents=0, dl_speed=0, name="ubuntu.iso"))
    )
    assert "TOR IDLE" in idle.line1
    assert "NO DOWNLOAD" in idle.line2
    assert "ubuntu" not in idle.line1 + idle.line2
    assert "%" not in idle.line1 + idle.line2

    active = screen.render(
        SimpleNamespace(
            torrent=SimpleNamespace(active_torrents=3, dl_speed=12.4 * 1024 * 1024, name="film.mkv")
        )
    )
    assert "TOR" in active.line1
    assert "ACTIVE" in active.line1
    assert "▶" in active.line1
    assert DOWNLOAD in active.line2
    assert "film" not in active.line1 + active.line2
    assert len(active.line1) == 16
    assert len(active.line2) == 16


def test_disk_hottest_and_empty():
    screen = DiskScreen()
    empty = screen.render(SimpleNamespace(disks=[]))
    assert empty.line1.strip() == "DISK --"
    assert empty.line2.strip() == "NO DATA"

    cool = SimpleNamespace(name="sda", temp_c=30, health="ok")
    hot = SimpleNamespace(name="sdb", temp_c=48, health="ok")
    out = screen.render(SimpleNamespace(disks=[cool, hot]))
    assert "sdb" in out.line1
    assert "HOT" in out.line1
    assert "48C" in out.line2
    assert len(out.line1) == 16

    warm = SimpleNamespace(name="sdc", temp_c=40, health="ok")
    normal = screen.render(SimpleNamespace(disks=[cool, warm]))
    assert "sdc" in normal.line1
    assert "40C" in normal.line1
    assert "OK" in normal.line2


def test_status_labels_no_temp_glyph_no_bar():
    cpu = SimpleNamespace(temp_c=42, temp=42)
    fan = SimpleNamespace(rpm=2100)
    disks = [SimpleNamespace(name="sda", temp_c=38), SimpleNamespace(name="sdb", temp_c=41)]
    storage = SimpleNamespace(used_pct=73.2)
    out = StatusScreen().render(SimpleNamespace(cpu=cpu, fan=fan, disks=disks, storage=storage))
    assert len(out.line1) == 16
    assert len(out.line2) == 16
    assert out.line1.startswith("CPU ")
    assert "FAN" in out.line1
    assert "DSK" in out.line2
    assert "STO" in out.line2
    assert "73%" in out.line2
    from dx4000_lcd.icons import TEMP
    assert TEMP not in out.line1
    assert TEMP not in out.line2

    missing = StatusScreen().render(
        SimpleNamespace(cpu=None, fan=SimpleNamespace(rpm=None), disks=[], storage=None)
    )
    assert "--C" in missing.line1
    assert "FAN --" in missing.line1
    assert "--C" in missing.line2
    assert "--%" in missing.line2


def test_storage_bar_and_fit():
    out = StorageScreen().render(
        SimpleNamespace(storage=SimpleNamespace(used_pct=81.6, used_bytes=500 * 1024 ** 3))
    )
    assert len(out.line1) == 16
    assert len(out.line2) == 16
    assert out.line1.startswith("STO ")
    assert "82%" in out.line1 or "81%" in out.line1

    missing = StorageScreen().render(SimpleNamespace(storage=None))
    assert "--%" in missing.line1
    assert len(missing.line1) == 16
    assert len(missing.line2) == 16


def test_system_cpu_ram_load():
    cpu = SimpleNamespace(usage=37, usage_pct=37, temp_c=51, load=1.23, load1=1.23)
    memory = SimpleNamespace(used_pct=64.4)
    out = SystemScreen().render(SimpleNamespace(cpu=cpu, memory=memory))
    assert len(out.line1) == 16
    assert len(out.line2) == 16
    assert "CPU 37%" in out.line1
    assert "51C" in out.line1
    assert "RAM 64%" in out.line2
    assert "L1.23" in out.line2


def test_alert_single_bang_prefix():
    health = SimpleNamespace(value="hot")
    alert = SimpleNamespace(source="disk", health=health, message="sda 45C extra text")
    out = AlertScreen().render(alert)
    assert len(out.line1) == 16
    assert len(out.line2) == 16
    assert out.line1.strip().startswith("! DISK")
    assert "HOT" in out.line1
    assert out.line1.count("!") == 1
    assert "sda 45C" in out.line2
