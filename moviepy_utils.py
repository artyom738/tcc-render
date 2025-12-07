"""
Утилиты для безопасной работы с MoviePy и предотвращения ошибок с дескрипторами FFmpeg
"""
import atexit
import weakref


# Глобальный реестр открытых клипов для автоматического закрытия при завершении программы
_open_clips = weakref.WeakSet()


def register_clip(clip):
    """
    Регистрирует клип для автоматического закрытия при завершении программы
    """
    _open_clips.add(clip)
    return clip


def close_all_clips():
    """
    Закрывает все зарегистрированные клипы
    """
    for clip in list(_open_clips):
        try:
            if hasattr(clip, 'close'):
                clip.close()
        except Exception as e:
            # Игнорируем ошибки при закрытии
            pass


# Регистрируем функцию закрытия при выходе из программы
atexit.register(close_all_clips)


def safe_close(clip):
    """
    Безопасно закрывает клип, игнорируя ошибки
    """
    if clip is None:
        return

    try:
        if hasattr(clip, 'close'):
            clip.close()
    except Exception:
        # Игнорируем ошибки при закрытии (например, если процесс уже завершен)
        pass

