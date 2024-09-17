from pytest import fixture


@fixture
def tecton_unit_test():
    from ..utils.tecton_utils import set_conf

    with set_conf(
        {
            "TECTON_DEBUG": "true",
            "TECTON_FORCE_FUNCTION_SERIALIZATION": "false",
            "DUCKDB_EXTENSION_REPO": "",
        }
    ):
        yield


@fixture
def tecton_vector_db_test_config(tmp_path):
    from .utils import make_local_vector_db_config

    path = str(tmp_path / "test.db")
    return make_local_vector_db_config(path, remove_if_exists=True)
