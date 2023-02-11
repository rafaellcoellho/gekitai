import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="gekitai")
    parser.add_argument("modo")
    args = parser.parse_args(argv)

    print(f"modo escolhido: {args.modo}")

    return 0


if __name__ == "__main__":
    exit(main())
