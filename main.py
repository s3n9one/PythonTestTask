import argparse
import csv
from tabulate import tabulate
import pytest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Путь к CSV-файлу")
    parser.add_argument("--where", help="Условие фильтрации")
    parser.add_argument("--aggregate", help="Аггрегация")
    args = parser.parse_args()

    with open(args.file, mode="r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if args.where:
        if ">=" in args.where:
            col, val = args.where.split(">=")
            filtered_rows = [row for row in rows if row[col] >= val]
        elif "<=" in args.where:
            col, val = args.where.split("<=")
            filtered_rows = [row for row in rows if row[col] <= val]
        elif "!=" in args.where:
            col, val = args.where.split("!=")
            filtered_rows = [row for row in rows if row[col] != val]
        elif ">" in args.where:
            col, val = args.where.split(">")
            filtered_rows = [row for row in rows if row[col] > val]
        elif "<" in args.where:
            col, val = args.where.split("<")
            filtered_rows = [row for row in rows if row[col] < val]
        elif "=" in args.where:
            col, val = args.where.split("=")
            filtered_rows = [row for row in rows if row[col] == val]
        print(tabulate(filtered_rows, headers="keys", tablefmt="grid"))                   
    else:
        print(tabulate(rows, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()