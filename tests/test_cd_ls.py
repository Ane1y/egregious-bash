import io
import pathlib
import tempfile

import pytest

from src.Environment import Environment
from src.builtin import Cd, Ls


@pytest.fixture(autouse=True)
def env():
    Environment({})


def test_cd(tmp_path):
    cwd = Environment.get_cwd()
    assert Cd().impl([tmp_path.as_posix()], None, None) == 0
    n_cwd = Environment.get_cwd()
    assert cwd != n_cwd
    assert pathlib.Path(n_cwd) == tmp_path


def test_cd_user():
    assert Cd().impl([], None, None) == 0
    cwd = Environment.get_cwd()
    assert pathlib.Path('~').expanduser() == pathlib.Path(cwd)


def test_cd_user_tilda():
    assert Cd().impl(['~'], None, None) == 0
    cwd = Environment.get_cwd()
    assert pathlib.Path('~').expanduser() == pathlib.Path(cwd)


def test_ls_without_files(tmp_path):
    result = io.StringIO()
    assert Ls().impl([tmp_path.as_posix()], None, result) == 0
    assert result.getvalue() == ''


def test_ls_with_files(tmp_path):
    result = io.StringIO()
    files = []
    with tempfile.TemporaryFile(dir=tmp_path) as f1, tempfile.TemporaryFile(dir=tmp_path) as f2:
        files.append(f1.name.rsplit('\\', 1)[1])
        files.append(f2.name.rsplit('\\', 1)[1])
        assert Ls().impl([tmp_path.as_posix()], None, result) == 0

    assert set(result.getvalue().splitlines()) == set(files)
