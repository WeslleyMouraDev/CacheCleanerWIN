import os
from unittest.mock import MagicMock
from src.scanner import get_folder_size_mb, find_large_folders


def test_get_folder_size_mb(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_bytes(b"0" * 1024 * 1024)  # 1MB
    size = get_folder_size_mb(str(tmp_path))
    assert 0.9 < size < 1.1


def test_get_folder_size_mb_empty(tmp_path):
    size = get_folder_size_mb(str(tmp_path))
    assert size == 0.0


def test_find_large_folders(tmp_path):
    dir_large = tmp_path / "large_dir"
    dir_large.mkdir()
    (dir_large / "big.bin").write_bytes(b"0" * 2 * 1024 * 1024)  # 2MB

    dir_small = tmp_path / "small_dir"
    dir_small.mkdir()
    (dir_small / "small.bin").write_bytes(b"0" * 512 * 1024)  # 0.5MB

    results = find_large_folders([str(tmp_path)], min_mb=1.0)
    assert len(results) == 1
    assert results[0][0] == str(dir_large)
    assert 1.9 < results[0][1] < 2.1


def test_find_large_folders_with_console_and_sorting(tmp_path):
    dir1 = tmp_path / "dir1"
    dir1.mkdir()
    (dir1 / "file1.bin").write_bytes(b"0" * 1024 * 1024)  # 1MB

    dir2 = tmp_path / "dir2"
    dir2.mkdir()
    (dir2 / "file2.bin").write_bytes(b"0" * 3 * 1024 * 1024)  # 3MB

    mock_console = MagicMock()
    mock_status = MagicMock()
    mock_console.status.return_value = mock_status

    results = find_large_folders(
        [str(tmp_path), "Z:\\nonexistent_dir_xyz"], min_mb=0.5, console=mock_console
    )

    mock_console.status.assert_called_once()
    mock_status.start.assert_called_once()
    mock_status.stop.assert_called_once()

    assert len(results) == 2
    assert results[0][0] == str(dir2)
    assert results[1][0] == str(dir1)
    assert results[0][1] > results[1][1]
