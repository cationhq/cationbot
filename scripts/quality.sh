# The source path.
APP_PATH=cationbot

# The unit tests path.
UNIT_TEST_PATH=tests

## =================== JOBS =================== ##

# Remove unsed variables and imports.
poetry run autoflake \
    --remove-all-unused-imports \
    --recursive \
    --remove-unused-variables \
    --in-place $APP_PATH $UNIT_TEST_PATH

# Sort imports from app and unit tests.
# There's a configuration on 'pyproject.toml' to make isort compatible with black.
# See: https://black.readthedocs.io/en/stable/compatible_configs.html#isort
poetry run isort $APP_PATH $UNIT_TEST_PATH

# Audit python files on app.
poetry run pylama $APP_PATH
# Audit python files on unit tests (ignoring E501: line too long).
poetry run pylama $UNIT_TEST_PATH --ignore=E501

# Pydocstyle:
#   - D101: Missing docstring in public class.
#   - D102: Missing docstring in public method.
#   - D103: Missing docstring in public function.
poetry run pydocstyle \
    --select=D101,D102,D103 \
    $APP_PATH

poetry run black --check $APP_PATH $UNIT_TEST_PATH
