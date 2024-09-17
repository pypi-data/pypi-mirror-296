from typing import TextIO

from deeprank2.domain.aminoacidlist import amino_acids, amino_acids_by_letter
from deeprank2.molstruct.residue import Residue
from deeprank2.molstruct.structure import Chain
from deeprank2.utils.pssmdata import PssmRow, PssmTable


def parse_pssm(file_: TextIO, chain: Chain) -> PssmTable:
    """Read the PSSM data.

    Args:
        file_: The pssm file.
        chain: The chain that the pssm file represents, residues from this chain must match the pssm file.

    Returns:
        The position-specific scoring table, parsed from the pssm file.
    """
    conservation_rows = {}

    # Read the pssm header.
    header = next(file_).split()
    column_indices = {column_name.strip(): index for index, column_name in enumerate(header)}

    for line in file_:
        row = line.split()

        # Read what amino acid the chain is supposed to have at this position.
        amino_acid = amino_acids_by_letter[row[column_indices["pdbresn"]]]

        # Some PDB files have insertion codes, find these to prevent
        # exceptions.
        pdb_residue_number_string = row[column_indices["pdbresi"]]
        if pdb_residue_number_string[-1].isalpha():
            pdb_residue_number = int(pdb_residue_number_string[:-1])
            pdb_insertion_code = pdb_residue_number_string[-1]
        else:
            pdb_residue_number = int(pdb_residue_number_string)
            pdb_insertion_code = None

        # Build the residue, to match with the pssm row
        residue = Residue(chain, pdb_residue_number, amino_acid, pdb_insertion_code)

        # Build the pssm row
        information_content = float(row[column_indices["IC"]])
        conservations = {amino_acid: float(row[column_indices[amino_acid.one_letter_code]]) for amino_acid in amino_acids}

        conservation_rows[residue] = PssmRow(conservations, information_content)

    return PssmTable(conservation_rows)
