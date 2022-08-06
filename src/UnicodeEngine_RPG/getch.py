# If Windows getch() available, use that.  If not, use a
# Unix version.
try:
    import msvcrt
    _getch = msvcrt.getch
except:
    import sys, tty, termios
    def _unix_getch():
        """Get a single character from stdin, Unix version"""

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())          # Raw read
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    _getch = _unix_getch

def getch():
    result = _getch()
    try:
        return result.decode() if isinstance(result, bytes) else result
    except Exception:
        return ""

if __name__ == "__main__":
    answer = getch().decode()
    print(answer)