from gepwc.core import pywc
from click.testing import CliRunner


def test_gepcat():
    runner = CliRunner()
    result = runner.invoke(pywc, ['assets/simple'])
    assert result.exit_code == 0
    assert result.output == ('file size in byte: 61\n'
 'number of lines: 1\n'
 'number of words: 1\n'
 'number of characters: 12\n')

def test_byte_calculation():
    runner = CliRunner()
    result = runner.invoke(pywc, ['assets/simple', '-c'])
    assert result.exit_code == 0
    assert result.output == 'file size in byte: 61\n'


def test_lines_calculation():
    runner = CliRunner()
    result = runner.invoke(pywc, ['assets/simple', '-l'])
    assert result.exit_code == 0
    assert result.output == "number of lines: 1\n"


def test_word_count():
    runner = CliRunner()
    result = runner.invoke(pywc, ['assets/simple', '-w'])
    assert result.exit_code == 0
    assert result.output == "number of words: 1\n"


def test_characters_count():
    runner = CliRunner()
    result = runner.invoke(pywc, ['assets/simple', '-m'])
    assert result.exit_code == 0
    assert result.output == "number of characters: 12\n"

def test_version():
    runner = CliRunner()
    result = runner.invoke(pywc, ['-V'])
    assert result.exit_code == 0
    assert result.output == "0.0.dev0\n"