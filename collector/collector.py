import time
import os
from analysis.analysis import Analysis

analysis = Analysis()

def tail(filepath):
    print("DEBUG: Opening:", filepath)

    # Spara filens position
    try:
        last_size = os.path.getsize(filepath)
    except FileNotFoundError:
        print("ERROR: File not found:", filepath)
        return

    print("DEBUG: Initial file size:", last_size)

    while True:
        try:
            current_size = os.path.getsize(filepath)
        except FileNotFoundError:
            print("ERROR: File vanished:", filepath)
            return

        # Om filen har vuxit har nya bytes skrivits
        if current_size > last_size:
            with open(filepath, "r", encoding="utf-8") as f:
                f.seek(last_size)  # hoppa till det som låg sist i listan senast
                new_data = f.read()
                lines = new_data.splitlines()

                for line in lines:
                    print("NEW:", line)
                    analysis.handle_log_line(line)

            last_size = current_size

        time.sleep(0.2)


def start_collector(filepath="test.log"):
    print(f"Collector started. Watching: {filepath}")
    print("CWD:", os.getcwd())
    tail(filepath)


if __name__ == "__main__":
    start_collector()
