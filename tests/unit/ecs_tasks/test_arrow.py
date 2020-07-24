from io import BytesIO, StringIO
from mock import patch

import pyarrow as pa
import pyarrow.json as pj
import pyarrow.parquet as pq
import pytest
import pandas as pd
from backend.ecs_tasks.delete_files.arrow import (
    delete_matches_from_file,
    delete_from_table,
    load_json,
    load_parquet,
    get_row_count,
)

pytestmark = [pytest.mark.unit, pytest.mark.ecs_tasks]


@patch("backend.ecs_tasks.delete_files.arrow.load_parquet")
@patch("backend.ecs_tasks.delete_files.arrow.delete_from_table")
def test_it_generates_new_parquet_file_without_matches(mock_delete, mock_load_parquet):
    # Arrange
    to_delete = [{"Column": "customer_id", "MatchIds": ["23456"]}]
    data = [{"customer_id": "12345"}, {"customer_id": "23456"}]
    df = pd.DataFrame(data)
    buf = BytesIO()
    df.to_parquet(buf)
    br = pa.BufferReader(buf.getvalue())
    f = pq.ParquetFile(br, memory_map=False)
    mock_df = pd.DataFrame([{"customer_id": "12345"}])
    mock_delete.return_value = [mock_df, 1]
    mock_load_parquet.return_value = f
    # Act
    out, stats = delete_matches_from_file("input_file.parquet", to_delete, "parquet")
    assert isinstance(out, pa.BufferOutputStream)
    assert {"ProcessedRows": 2, "DeletedRows": 1} == stats
    res = pa.BufferReader(out.getvalue())
    newf = pq.ParquetFile(res, memory_map=False)
    assert 1 == newf.read().num_rows


@patch("backend.ecs_tasks.delete_files.arrow.delete_from_table")
def test_it_generates_new_json_file_without_matches(mock_delete):
    # Arrange
    to_delete = [{"Column": "customer_id", "MatchIds": ["23456"]}]
    data = [{"customer_id": "12345"}, {"customer_id": "23456"}]
    out_stream = to_json_stream(data)
    mock_df = pd.DataFrame([{"customer_id": "12345"}])
    mock_delete.return_value = [mock_df, 1]
    # Act
    out, stats = delete_matches_from_file(out_stream.getvalue(), to_delete, "json")
    assert isinstance(out, pa.BufferOutputStream)
    assert {"ProcessedRows": 2, "DeletedRows": 1} == stats
    res = pa.BufferReader(out.getvalue())
    newf = load_json(res)
    assert 1 == newf.num_rows


def test_delete_correct_rows_from_table():
    data = [
        {"customer_id": "12345"},
        {"customer_id": "23456"},
        {"customer_id": "34567"},
    ]
    columns = [{"Column": "customer_id", "MatchIds": ["12345", "23456"]}]
    df = pd.DataFrame(data)
    table = pa.Table.from_pandas(df)
    res, deleted_rows = delete_from_table(table, columns)
    assert len(res) == 1
    assert deleted_rows == 2
    assert res["customer_id"].values[0] == "34567"


def test_delete_correct_rows_from_table_with_complex_types():
    data = {
        "customer_id": [12345, 23456, 34567],
        "user_info": [
            {"name": "matteo", "email": "12345@test.com"},
            {"name": "nick", "email": "23456@test.com"},
            {"name": "chris", "email": "34567@test.com"},
        ],
    }
    columns = [{"Column": "user_info.name", "MatchIds": ["matteo", "chris"]}]
    df = pd.DataFrame(data)
    table = pa.Table.from_pandas(df)
    res, deleted_rows = delete_from_table(table, columns)
    assert len(res) == 1
    assert deleted_rows == 2
    assert res["customer_id"].values[0] == 23456
    # user_info is saved unflattened preserving original schema:
    assert res["user_info"].values[0] == {"name": "nick", "email": "23456@test.com"}


def test_it_gets_row_count():
    data = [
        {"customer_id": "12345"},
        {"customer_id": "23456"},
        {"customer_id": "34567"},
    ]
    df = pd.DataFrame(data)
    assert 3 == get_row_count(df)


def test_it_loads_json_files():
    out_stream = to_json_stream([{"customer_id": "12345"}, {"customer_id": "23456"}])
    resp = load_json(out_stream.getvalue())
    assert 2 == resp.num_rows


def test_it_loads_parquet_files():
    data = [{"customer_id": "12345"}, {"customer_id": "23456"}]
    df = pd.DataFrame(data)
    buf = BytesIO()
    df.to_parquet(buf, compression="snappy")
    resp = load_parquet(buf)
    assert 2 == resp.read().num_rows


def to_json_stream(data):
    df = pd.DataFrame(data)
    buf = StringIO()
    out_stream = pa.BufferOutputStream()
    df.to_json(buf, orient="records", lines=True)
    out_stream.write(buf.getvalue().encode())
    return out_stream
