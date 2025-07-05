import pytest
import csv
from main import parse_condition, apply_condition, aggregate_data, main
from tabulate import tabulate

# Фикстуры для тестовых данных
@pytest.fixture
def sample_rows():
    return [
        {"brand": "xiaomi", "rating": "4.5", "price": "15000"},
        {"brand": "samsung", "rating": "4.7", "price": "20000"},
        {"brand": "apple", "rating": "4.9", "price": "50000"},
    ]

@pytest.fixture
def empty_rows():
    return []

# Тесты для parse_condition
def test_parse_condition_equal():
    assert parse_condition("rating=4.5") == ("rating", "=", "4.5")

def test_parse_condition_greater():
    assert parse_condition("price>20000") == ("price", ">", "20000")

def test_parse_condition_invalid():
    with pytest.raises(ValueError):
        parse_condition("invalid_condition")

# Тесты для apply_condition
def test_apply_condition_equal(sample_rows):
    filtered = apply_condition(sample_rows, "brand=xiaomi")
    assert len(filtered) == 1
    assert filtered[0]["brand"] == "xiaomi"

def test_apply_condition_greater(sample_rows):
    filtered = apply_condition(sample_rows, "rating>4.6")
    assert len(filtered) == 2
    assert all(float(row["rating"]) > 4.6 for row in filtered)

def test_apply_condition_empty(empty_rows):
    assert apply_condition(empty_rows, "brand=xiaomi") == []

# Тесты для aggregate_data
def test_aggregate_min(sample_rows):
    result = aggregate_data(sample_rows, "price", "min")
    assert result[0]["Результат"] == 15000

def test_aggregate_mean(sample_rows):
    result = aggregate_data(sample_rows, "price", "mean")
    assert result[0]["Результат"] == (15000 + 20000 + 50000) / 3

def test_aggregate_empty(empty_rows):
    assert aggregate_data(empty_rows, "price", "sum") is None

def test_main_with_aggregate(tmp_path, capsys):
    csv_data = "brand,rating,price\nxiaomi,4.5,15000\nsamsung,4.7,20000"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_data)

    main(["--file", str(csv_file), "--aggregate", "price=sum"])
    captured = capsys.readouterr()
    
    assert "Агрегация" in captured.out
    assert "Столбец" in captured.out
    assert "Результат" in captured.out
    assert "sum" in captured.out
    assert "price" in captured.out
    assert "35000" in captured.out

def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main([])