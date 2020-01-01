from click.testing import CliRunner
from yabump.cli import main


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert len(result.output) > 0
