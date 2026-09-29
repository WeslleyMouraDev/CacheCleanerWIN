import os
from unittest.mock import MagicMock, patch
from src.cleaner import get_free_space_mb, safe_delete_folder_contents, clean_system_caches


def test_get_free_space_mb():
    space = get_free_space_mb("C:\\")
    assert space > 0


def test_safe_delete_folder_contents(tmp_path):
    sub_dir = tmp_path / "subdir"
    sub_dir.mkdir()
    file1 = tmp_path / "file1.txt"
    file1.write_text("hello")
    file2 = sub_dir / "file2.txt"
    file2.write_text("world")

    safe_delete_folder_contents(str(tmp_path))

    assert tmp_path.exists()
    assert list(tmp_path.iterdir()) == []


def test_safe_delete_folder_contents_nonexistent():
    safe_delete_folder_contents("Z:\\path_that_does_not_exist_12345")


def test_safe_delete_folder_contents_handles_exceptions(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("hello")

    with patch("os.unlink", side_effect=PermissionError("Permission denied")):
        safe_delete_folder_contents(str(tmp_path))
    assert file1.exists()


def test_clean_system_caches():
    mock_console = MagicMock()
    status_mock = MagicMock()
    mock_console.status.return_value.__enter__.return_value = status_mock

    with patch("src.cleaner.safe_delete_folder_contents") as mock_delete:
        with patch("os.path.exists", return_value=True):
            clean_system_caches(mock_console)

    mock_console.status.assert_called_once()
    assert mock_delete.call_count == 7
