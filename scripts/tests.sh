set -e
set -x

poetry run pytest --cov --cov-report=xml -v