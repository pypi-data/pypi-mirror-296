from __future__ import annotations

from pathlib import Path

import click
from Bio.PDB.mmcifio import MMCIFIO

from alphafold3_pytorch.models.components.alphafold3 import Alphafold3
from alphafold3_pytorch.models.components.inputs import Alphafold3Input

# simple cli using click


@click.command()
@click.option("-ckpt", "--checkpoint", type=str, help="Path to alphafold3 checkpoint")
@click.option("-prot", "--protein", type=str, multiple=True, help="Protein sequences")
@click.option("-rna", "--rna", type=str, multiple=True, help="Single-stranded RNA sequences")
@click.option("-dna", "--dna", type=str, multiple=True, help="Single-stranded DNA sequences")
@click.option("-o", "--output", type=str, help="output path", default="output.cif")
def cli(checkpoint: str, protein: list[str], rna: list[str], dna: list[str], output: str):
    checkpoint_path = Path(checkpoint)
    assert checkpoint_path.exists(), f"Alphafold3 checkpoint must exist at {str(checkpoint_path)}"

    alphafold3_input = Alphafold3Input(
        proteins=protein,
        ss_rna=rna,
        ss_dna=dna,
    )

    alphafold3 = Alphafold3.init_and_load(checkpoint_path)

    alphafold3.eval()
    (structure,) = alphafold3.forward_with_alphafold3_inputs(
        alphafold3_input, return_bio_pdb_structures=True
    )

    output_path = Path(output)
    output_path.parents[0].mkdir(exist_ok=True, parents=True)

    pdb_writer = MMCIFIO()
    pdb_writer.set_structure(structure)
    pdb_writer.save(str(output_path))

    print(f"mmCIF file saved to {str(output_path)}")
