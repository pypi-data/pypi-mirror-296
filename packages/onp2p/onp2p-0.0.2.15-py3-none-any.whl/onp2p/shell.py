import pyfiglet

def shell():
    # Creare un titolo in ASCII art con il font "slant"
    ascii_title = pyfiglet.figlet_format("ONP2P", font="slant")
    print(ascii_title)

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
