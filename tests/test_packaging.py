import tomllib


def test_kanade_dependency_is_pip_installable_direct_reference():
    with open("pyproject.toml", "rb") as fp:
        project = tomllib.load(fp)["project"]

    dependencies = project["dependencies"]

    assert (
        "kanade-tokenizer @ git+https://github.com/frothywater/kanade-tokenizer"
        in dependencies
    )
