import sys
import click
from .__version import __version__
def byte_calculation(file_txt):
    size = 0
    for line in file_txt:
        size += sys.getsizeof(line)
    click.echo("file size in byte: ", nl=False)
    click.echo(size)


def lines_calculation(file_txt):
    counter = 0
    for line in file_txt:
        counter += 1
    click.echo("number of lines: ", nl=False)
    click.echo(counter)


def characters_calculation(file_txt):
    res = 0
    for line in file_txt:
        words = line.split()
        for word in words:
            res += len(word)
    click.echo("number of characters: ", nl=False)
    click.echo(res)


def words_calculation(file_txt):
    word_counter = 0
    for line in file_txt:
        words = line.split()
        word_counter += len(words)
    click.echo("number of words: ", nl=False)
    click.echo(word_counter)



@click.group()
def cli():
    pass

@click.command()
@click.argument('file_txt', type=str, nargs=-1)
@click.option('--byte_calculate', '-c', is_flag=True, default=False,help="calculate the number of bytes in a file")
@click.option('--lines_calculate', '-l', is_flag=True, default=False,help="calculate the number of lines in a file")
@click.option('--words_calculate', '-w', is_flag=True, default=False,help="calculate the number of words in a file")
@click.option('--characters_calculate', '-m', is_flag=True, default=False, help="calculate the number of characters in a file")
@click.option('--version', '-V', is_flag=True, default=False, help="output the version of gepwc")

def pywc(file_txt, byte_calculate, lines_calculate, words_calculate, characters_calculate, version):
    if version:
        click.echo(__version__)

    for file in file_txt:
        with open(file, 'r') as f:
            if byte_calculate:
                byte_calculation(f)

            elif lines_calculate:
                lines_calculation(f)

            elif words_calculate:
                words_calculation(f)

            elif characters_calculate:
                characters_calculation(f)

            else:
                byte_calculation(f)
                with open(file, 'r') as f:
                    lines_calculation(f)
                with open(file, 'r') as f:
                    words_calculation(f)
                with open(file, 'r') as f:
                    characters_calculation(f)


if __name__ == "__main__":
    pywc()