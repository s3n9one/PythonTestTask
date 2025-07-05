import argparse
import csv
from tabulate import tabulate

def parse_condition(condition):
    operators = ['>=', '<=', '!=', '=', '>', '<']
    for op in operators:
        if op in condition:
            column, value = condition.split(op, 1)
            return column.strip(), op, value.strip()
    raise ValueError(f"Неизвестный оператор в условии: {condition}")

def apply_condition(rows, condition):
    column, operator, value = parse_condition(condition)
    filtered_rows = []
    
    for row in rows:
        cell_value = row.get(column, '')
        try:
            cell_num = float(cell_value)
            value_num = float(value)
            match operator:
                case '=' if cell_num == value_num:
                    filtered_rows.append(row)
                case '>' if cell_num > value_num:
                    filtered_rows.append(row)
                case '<' if cell_num < value_num:
                    filtered_rows.append(row)
                case '>=' if cell_num >= value_num:
                    filtered_rows.append(row)
                case '<=' if cell_num <= value_num:
                    filtered_rows.append(row)
                case '!=' if cell_num != value_num:
                    filtered_rows.append(row)
        except ValueError:
            match operator:
                case '=' if cell_value == value:
                    filtered_rows.append(row)
                case '!=' if cell_value != value:
                    filtered_rows.append(row)
                case _:
                    continue
    return filtered_rows

def aggregate_data(rows, column, func):
    values = []
    for row in rows:
        try:
            values.append(float(row.get(column, 0)))
        except ValueError:
            continue
    
    if not values:
        return None

    match func:
        case 'min':
            result = min(values)
        case 'max':
            result = max(values)
        case 'mean':
            result = sum(values) / len(values)
        case 'sum':
            result = sum(values)
        case _:
            raise ValueError(f"Неизвестная функция агрегации: {func}")
    
    return [{"Агрегация": func, "Столбец": column, "Результат": result}]

def main(args=None):
    parser = argparse.ArgumentParser(description="Анализ CSV-файлов")
    parser.add_argument("--file", required=True, help="Путь к CSV-файлу")
    parser.add_argument("--where", help="Условие фильтрации (например, 'rating>4.5')")
    parser.add_argument("--aggregate", help="Агрегация (например, 'price=sum')")
    
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    with open(args.file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if args.where:
        rows = apply_condition(rows, args.where)

    if args.aggregate:
        column, func = args.aggregate.split('=')
        agg_result = aggregate_data(rows, column, func)
        if agg_result:
            print(tabulate(agg_result, headers="keys", tablefmt="grid"))
        else:
            print("Нет данных для агрегации.")
    else:
        print(tabulate(rows, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()