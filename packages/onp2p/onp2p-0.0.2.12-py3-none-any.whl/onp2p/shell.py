# my_shell/shell.py

def shell():
    print("Benvenuto nella shell interattiva. Scrivi 'exit' per uscire.")

    while True:
        command = input(">>> ")

        if command.lower() == "exit":
            print("Uscita dalla shell.")
            break

        try:
            result = eval(command)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Errore: {e}")
