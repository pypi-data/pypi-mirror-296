# click cli app that takes a fasta file and writes a new fasta file with the sequences reversed and complemented
import click

import guigaga


class Sequence:
    def __init__(self, header, sequence):
        self.header = header
        self.sequence = sequence

    def reverse_complement(self):
        complement = {"A": "T", "C": "G", "G": "C", "T": "A", "U": "A", "N": "N"}
        return Sequence(self.header, "".join([complement[base] for base in self.sequence[::-1]]))

    def __str__(self):
        return f">{self.header}\n{self.sequence}"

def read_fasta(fasta_file):
    with open(fasta_file) as f:
        for line in f:
            if line.startswith(">"):
                header = line.strip()[1:]
                sequence = ""
            else:
                sequence += line.strip()
                yield Sequence(header, sequence)

def write_fasta(sequences, output_file):
    with open(output_file, "w") as f:
        for sequence in sequences:
            f.write(f">{sequence.header}\n{sequence.sequence}\n")

@guigaga.gui()
@click.command(help="Reverse complement a fasta file")
@click.argument("fasta_file", required=True, type=click.File())
def reverse_complement(
        fasta_file,
    ):
    sequences = [sequence.reverse_complement() for sequence in read_fasta(fasta_file)]
    for sequence in sequences:
        click.echo(sequence)

if __name__ == "__main__":
    reverse_complement()
