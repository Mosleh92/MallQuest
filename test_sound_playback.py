import sys
from types import SimpleNamespace
from unittest.mock import MagicMock
import importlib

# Create a stub pygame module for environments without the real package
pygame_stub = SimpleNamespace()
pygame_stub.mixer = SimpleNamespace(
    get_init=MagicMock(return_value=True),
    init=MagicMock(),
    Sound=MagicMock()
)
sys.modules['pygame'] = pygame_stub

# Stub database module to avoid side effects during import
database_stub = SimpleNamespace(db=MagicMock())
sys.modules['database'] = database_stub

graphics_module = importlib.import_module("3d_graphics_module")
play_sound = graphics_module.play_sound


def test_play_sound_uses_pygame():
    mock_sound = pygame_stub.mixer.Sound
    mock_instance = mock_sound.return_value

    play_sound("test.wav", volume=0.5, loop=True)

    mock_sound.assert_called_once_with("test.wav")
    mock_instance.set_volume.assert_called_once_with(0.5)
    mock_instance.play.assert_called_once_with(loops=-1)
