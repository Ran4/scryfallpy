import argparse



def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--print-url",
        dest="print_url",
        action="store_true",
        default=False,
        help="Prints scryfall url")
    
    parser.add_argument(
        "-n", "--no-color",
        dest="no_color",
        action="store_true",
        default=False,
        help="Disable color output")
    
    return parser


def get_args():
    parser = get_parser()
    return parser.parse_args()
