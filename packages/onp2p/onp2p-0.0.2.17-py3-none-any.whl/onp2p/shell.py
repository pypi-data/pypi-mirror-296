import argparse
import pyfiglet

# local imports
import onp2p.wrapper as wrapper


def shell():
    # Creare un titolo in ASCII art con il font "slant"
    ascii_title = pyfiglet.figlet_format("ONP2P", font="slant")
    print(ascii_title)

    print("Welcome to the ONP2P interctive shell. Type 'exit' to close.")

    while True:
        command = input(">>> ").strip().split()


        if command[0].lower() == 'exit':
            print("Bye")
            break


        parser = argparse.ArgumentParser(prog='shell', description="Shell interattiva per eseguire operazioni matematiche.")

        # Aggiungiamo i sottocomandi per le diverse operazioni
        subparsers = parser.add_subparsers(dest='command')

        # Definizione del sottocomando 'somma'
        parser_sum = subparsers.add_parser('sum', help='Add two numbers')
        parser_sum.add_argument('a', type=float, help='First number')
        parser_sum.add_argument('b', type=float, help='Second numer')

        try:

            # Parsing dell'input dell'utente
            args = parser.parse_args(command)

            # Esegui l'operazione corrispondente
            if args.comando == 'sum':
                print(wrapper.add(args.a, args.b))
            
            else:
                print("Command not recognized.")

        except SystemExit:
            # Gestione per evitare che argparse chiuda la shell su errore
            pass
        except Exception as e:
            print(f"Error: {e}")
