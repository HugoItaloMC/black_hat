# behaviours argparser (flags to script commands)
import argparse



class Parser:
    def arg_parser(self):
        parser = argparse.ArgumentParser(prog='Replacing NetCat with Python', description='%(prog)s')
        parser.add_argument('-l', '--listen', action='store_true', help='TODO: ')
        parser.add_argument('-e', '--execute', metavar='FILE', help='TODO: ')
        parser.add_argument('-c', '--command', action='store_true', help='TODO: ')
        parser.add_argument('-u', '--upload', metavar='DESTINATION', help='TODO: ')
        parser.add_argument('-t', '--targer', metavar='HOST', help="TODO: ")
        parser.add_argument('-p', '--port', metavar='PORT', help='TODO: ')
        args = parser.parse_args()
        if not any(vars(args).values()):
            print(parser.print_usage())
        else:
            return args



if __name__ == '__main__':
    args = Parser().arg_parser()
    #  {'listen': False, 'execute': None, 'command': False, 'upload': None, 'targer': None, 'port': None}