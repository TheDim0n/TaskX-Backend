import glob
import os


def test_delete_test_database():
    path_to_db = glob.glob("*/sql_app.db")[0]
    os.remove(path_to_db)
    assert not os.path.exists(path_to_db)
