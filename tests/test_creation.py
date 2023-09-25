import os
import shlex
import subprocess
from contextlib import contextmanager

import pytest

default_context = {
    "project_name": "zztop",
    "repo_name": "zztop",
    "homepage": "https://kureta.xyz",
    "author_name": "kureta",
    "author_email": "skureta@gmail.com",
    "description": "A test project",
    "registry_name": "docker.kureta.xyz",
    "dvc_bucket": "s3://zztop",
    "dvc_endpoint": "https://cloud.kureta.xyz",
}


@pytest.fixture(scope="module")
def bakery(cookies_session):
    """create a session-wide cookiecutter instance"""
    result = cookies_session.bake(extra_context=default_context)
    yield result


@contextmanager
def run_within_dir(path: str):
    old_working_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_working_dir)


def base_assertions(bakery):
    assert bakery.exit_code == 0
    assert bakery.exception is None
    assert bakery.project_path.is_dir()


def test_bake_project(bakery):
    base_assertions(bakery)

    assert bakery.project_path.name == "zztop"


def test_make_build_base(bakery):
    base_assertions(bakery)

    with run_within_dir(str(bakery.project_path)):
        assert subprocess.check_call(shlex.split("make build_base")) == 0


def test_make_build(bakery):
    base_assertions(bakery)

    with run_within_dir(str(bakery.project_path)):
        assert subprocess.check_call(shlex.split("make build")) == 0


def test_make_build_test(bakery):
    base_assertions(bakery)

    with run_within_dir(str(bakery.project_path)):
        assert subprocess.check_call(shlex.split("make build_test")) == 0


def test_make_init(bakery):
    base_assertions(bakery)

    with run_within_dir(str(bakery.project_path)):
        assert subprocess.check_call(shlex.split("make init")) == 0


def test_make_git_status(bakery):
    base_assertions(bakery)

    with run_within_dir(str(bakery.project_path)):
        assert subprocess.check_call(shlex.split("git status")) == 0


def test_make_dvc_status(bakery):
    base_assertions(bakery)

    with run_within_dir(str(bakery.project_path)):
        assert subprocess.check_call(shlex.split(".venv/bin/python -m dvc status")) == 0


def test_make_test(bakery):
    base_assertions(bakery)

    with run_within_dir(str(bakery.project_path)):
        assert subprocess.check_call(shlex.split("make test")) == 0
