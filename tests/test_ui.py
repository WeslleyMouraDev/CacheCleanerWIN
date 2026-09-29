from unittest.mock import patch
import pytest
from src.ui import (
    get_space_panel,
    show_header,
    ask_confirmation,
    ask_danger_confirmation,
    print_success,
    print_error,
)

def test_get_space_panel():
    panel = get_space_panel(1000, 1500)
    assert "Antes: 1000" in str(panel)
    assert "Liberado: 500" in str(panel)

def test_show_header():
    show_header()

def test_print_helpers():
    print_success("Tudo certo")
    print_error("Algo deu errado")

def test_ask_confirmation():
    with patch("rich.prompt.Confirm.ask", return_value=True):
        assert ask_confirmation("Continuar?") is True
    with patch("rich.prompt.Confirm.ask", return_value=False):
        assert ask_confirmation("Continuar?") is False

def test_ask_danger_confirmation():
    with patch("rich.prompt.Confirm.ask", return_value=True) as mock_ask:
        assert ask_danger_confirmation("Excluir tudo?") is True
        mock_ask.assert_called_once()
        assert "PERIGO:" in mock_ask.call_args[0][0]
