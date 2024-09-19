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

        parser = argparse.ArgumentParser(prog='onp2p-shell', description="ONP2P interctive shell")

        # Aggiungiamo i sottocomandi per le diverse operazioniss
        subparsers = parser.add_subparsers(dest='command')

        # Definizione del sottocomando 'somma'
        parser_sum = subparsers.add_parser('sum', help='Add two interger numbers')
        parser_sum.add_argument('a', type=int, help='First number')
        parser_sum.add_argument('b', type=int, help='Second numer')

        # Definizione del sottocomando 'somma'
        parser_create_channel = subparsers.add_parser('create_channel', help='create a tor channels')
        parser_create_channel.add_argument('port', type=int, help='port')
     

        try:

            # Parsing dell'input dell'utente
            args = parser.parse_args(command)

            # Esegui l'operazione corrispondente
            if args.command == 'sum':
                print(wrapper.add(args.a, args.b))
            
            elif args.command == 'create_channel':
                wrapper.create_channel(args.port)
                print(f'channel created at port {args.port}')
            
            else:
                print("Command not recognized.")

        except SystemExit:
            # Gestione per evitare che argparse chiuda la shell su errore
            pass
        except Exception as e:
            print(f"Error: {e}")
