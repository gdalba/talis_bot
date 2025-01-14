import ctypes
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, LPWSTR

# Constantes das mensagens
WM_SETCURSOR = 0x0020
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205

HTCLIENT = 1  # Hit-test no cliente da janela
MK_LBUTTON = 0x0001  # Botão esquerdo pressionado
MK_RBUTTON = 0x0002  # Botão direito pressionado

# Carregando a biblioteca user32.dll
user32 = ctypes.windll.user32


# Função para criar o LPARAM com as coordenadas
def make_lparam(x: int, y: int) -> LPARAM:
    return LPARAM(y << 16 | x & 0xFFFF)


# Funções para cliques de mouse
def left(hwnd: int, x: int, y: int):
    """Simula um clique com o botão esquerdo do mouse."""
    user32.SendMessageW(HWND(hwnd), WM_SETCURSOR, WPARAM(hwnd), LPARAM(HTCLIENT | (WM_MOUSEMOVE << 16)))
    user32.SendMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_LBUTTONDOWN, WPARAM(MK_LBUTTON), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_LBUTTONUP, WPARAM(0), make_lparam(x, y))


def right(hwnd: int, x: int, y: int):
    """Simula um clique com o botão direito do mouse."""
    user32.SendMessageW(HWND(hwnd), WM_SETCURSOR, WPARAM(hwnd), LPARAM(HTCLIENT | (WM_MOUSEMOVE << 16)))
    user32.SendMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_RBUTTONDOWN, WPARAM(MK_RBUTTON), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_RBUTTONUP, WPARAM(0), make_lparam(x, y))


# Função para mover o mouse com PostMessage
def move(hwnd: int, x: int, y: int):
    """
    Move fisicamente o cursor do mouse para uma posição específica dentro da janela alvo.

    Args:
        hwnd (int): Handle da janela onde o movimento será calculado.
        x (int): Coordenada X relativa à janela.
        y (int): Coordenada Y relativa à janela.
    """
    # Obter a posição absoluta da janela na tela
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(HWND(hwnd), ctypes.byref(rect))
    window_x, window_y = rect.left, rect.top

    # Converter coordenadas relativas à janela em coordenadas absolutas
    absolute_x = window_x + x
    absolute_y = window_y + y

    # Mover o cursor fisicamente para as coordenadas absolutas
    user32.SetCursorPos(absolute_x, absolute_y)

def get_window_title(self, pid):
    def enum_windows_callback(hwnd, param):
        try:
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == param['pid']:
                window_text = win32gui.GetWindowText(hwnd)
                if window_text:  # Ignore windows without titles
                    param['title'] = window_text
                    return False  # Stop enumeration
        except Exception as e:
            print(f"Error accessing hwnd: {hwnd}, error: {e}")
        return True

    param = {'pid': pid, 'title': "N/A"}
    try:
        win32gui.EnumWindows(enum_windows_callback, param)
    except Exception as e:
        print(f"Error enumerating windows: {e}")
    return param['title']

def get_game_hwnd(pid=None, title="monkito - Bot Master"):
    """
    Get game window handle by PID or title.
    Args:
        pid: Process ID (optional)
        title: Window title to search for (default: Wizard101)
    Returns:
        HWND of the game window or None if not found
    """
    def callback(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            if pid:
                try:
                    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                    if process_id == pid:
                        ctx.append(hwnd)
                except:
                    pass
            else:
                if title.lower() in win32gui.GetWindowText(hwnd).lower():
                    ctx.append(hwnd)
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    return windows[0] if windows else None

"""
import mouse

hwnd = 0x000E0398
xPos, yPos = 75, 75

mouse.left(hwnd, xPos, yPos)
"""
import win32gui
import win32process
import win32api

import mouse

def main():
    hwnd = get_game_hwnd()
    print(f"Game window handle: {hwnd}")
    if not hwnd:
        print("Not found.")
        return  
    xPos, yPos = 750, 150    
    

    cursor_pos = win32gui.GetCursorPos()
    print(f"Cursor position: {cursor_pos}")

    mouse.left(hwnd, xPos, yPos)

if __name__ == "__main__":
    main()