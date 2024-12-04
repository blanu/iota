import keyboard

class REPL:
    def __init__(self):
        keyboard.add_hotkey('space', self.space)

        keyboard.wait()

    def space(self):
        print('space was pressed!')

def main():
    REPL()

if __name__ == '__main__':
    main()