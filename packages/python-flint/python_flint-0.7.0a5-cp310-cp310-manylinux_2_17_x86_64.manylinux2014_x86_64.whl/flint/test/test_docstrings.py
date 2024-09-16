import doctest
import importlib
import pkgutil
import re

import flint

dunder_test_regex = re.compile(r'^(.*?)__test__\..*?\.(.*) \(line (\d+)\)$')


def find_doctests(module):
    finder = doctest.DocTestFinder()
    tests = []
    for module_info in pkgutil.walk_packages(module.__path__, flint.__name__ + "."):
        try:
            module = importlib.import_module(module_info.name)

            res = []
            for test in filter(lambda x: bool(x.examples), finder.find(module)):
                m = dunder_test_regex.match(test.name)
                if m is not None:
                    groups = m.groups()
                    test.name = groups[0] + groups[1]
                    test.lineno = int(groups[2])
                    res.append(test)

            tests.append((module_info.name, res))

        except Exception as e:
            print(f"Error importing {module_info.name}: {e}")
    return tests


# The below definitions are only useful when pytest is a) installed, and b) being currently run.
# We don't want to impose pytest on those that just want to use `python -m flint.test`
try:
    import pytest

    class PyTestDocTestRunner(doctest.DocTestRunner):
        def report_failure(self, out, test, example, got):
            pytest.fail(
                "\n".join([
                    f"{test.name}, line: {test.lineno}",
                    "Failed example:",
                    f"\t{example.source.strip()}",
                    "Expected:",
                    f"\t{example.want.strip()}",
                    "Got:",
                    f"\t{got.strip()}"
                ]),
                pytrace=False,
            )

        def report_unexpected_exception(self, out, test, example, exc_info):
            pytest.fail(
                "\n".join([
                    f"{test.name}, line: {test.lineno}",
                    "Failed example:",
                    f"\t{example.source.strip()}",
                    "Exception raised:",
                    doctest._indent(doctest._exception_traceback(exc_info))
                ]),
                pytrace=False,
            )

    runner = PyTestDocTestRunner()

    @pytest.mark.parametrize(
        "test",
        [
            test for _, test_set in find_doctests(flint)
            for test in test_set
        ],
        ids=lambda test: test.name,
    )
    def test_docstrings(test):
        runner.run(test)

except ImportError:
    class PyTestDocTestRunner(doctest.DocTestRunner):
        pass

    runner = None

    def test_docstrings(test):
        pass
