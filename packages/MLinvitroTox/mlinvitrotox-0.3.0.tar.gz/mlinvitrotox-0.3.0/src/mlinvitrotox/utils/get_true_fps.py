# Data processing: 2) process molecules
import re

import warnings

import pandas as pd
import numpy as np
from tqdm import tqdm
import logging

from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize
from openbabel import pybel
from CDK_pywrapper import CDK, FPType


def remove_illegal_smiles(df, smiles_column, nonallowed):
    """Remove rows where SMILES string contains specific non-allowed strings or characters"""
    nonallowed_pattern = "|".join(map(re.escape, nonallowed))
    mask = df[smiles_column].str.contains(nonallowed_pattern, na=False)
    df_clean = df[~mask]
    return df_clean


def standardize_smiles(raw_smiles):
    if raw_smiles is None:
        return None
    try:
        # Standardize and desalt the molecule
        std1_smiles = rdMolStandardize.StandardizeSmiles(raw_smiles)
        desalter = rdMolStandardize.LargestFragmentChooser()
        desalt_mol = desalter.choose(Chem.MolFromSmiles(std1_smiles))
        std2_smiles = rdMolStandardize.StandardizeSmiles(Chem.MolToSmiles(desalt_mol))
        return std2_smiles
    except Exception as e:
        # Log the exception and return None
        #        smiles = Chem.MolToSmiles(mol) if mol else "Invalid mol"
        logging.warning(f"Error processing molecule: {raw_smiles}; Error: {e}")
        return None


def standardize_mol(mol):
    if mol is None:
        return None
    try:
        # Standardize and desalt the molecule
        std1_mol = rdMolStandardize.StandardizeSmiles().standardize(
            Chem.MolToSmiles(mol)
        )
        desalter = rdMolStandardize.LargestFragmentChooser()
        desalt_mol = desalter.choose(std1_mol)
        std2_mol = rdMolStandardize.StandardizeSmiles().standardize(
            Chem.MolToSmiles(desalt_mol)
        )
        return std2_mol
    except Exception as e:
        # Log the exception and return None
        smiles = Chem.MolToSmiles(mol) if mol else "Invalid mol"
        logging.warning(f"Error processing molecule: {smiles}; Error: {e}")
        return None


def process_molecules(
    id,
    smiles,
    fps_input_path,
    df_csi,
    fps_output_path,
    csv_output_path,
    sdf_output_path,
    store_as_csv=False,
):
    ## Set ID for SMILES
    #smiles = SMILES_ID

    # Read the CSV data
    data = pd.read_csv(fps_input_path)
    print("The shape of the input data frame with structures:")
    print(data.shape)

    # Check for duplicates
    if data[id].duplicated().any():
        warnings.warn(
            f"There are duplicates in the file {fps_input_path} based on '{id}'"
        )

    # Only keep SMILES and chemical ID
    keep_columns = [id, smiles]
    df = data[keep_columns].copy()
    print("The shape of the modified data frame:")
    print(df.shape)
    print(df.head())

    # pre-cleanup
    df.loc[:, id] = df[id].str.replace(
        "https://comptox.epa.gov/dashboard/chemical/details/", ""
    )
    df = remove_illegal_smiles(df, smiles, ["Zn", "Pt", "<", ">", "R"])
    df = df[df[smiles].str.count("[Cc]") >= 2]
    df.loc[:, "sdf"] = df[smiles].apply(lambda x: Chem.MolFromSmiles(x) if x else None)
    df.dropna(subset=["sdf"], inplace=True)

    # standardize according to chemdbl procedure
    df["standardized_smiles"] = df[smiles].apply(standardize_smiles)
    df["standardized_mol"] = df["standardized_smiles"].apply(
        lambda x: Chem.MolFromSmiles(x) if x else None
    )

    # Store sdf file
    writer = Chem.SDWriter(sdf_output_path)
    for index, row in df.sort_values(id).iterrows():
        mol = row["standardized_mol"]
        chem_id = row[id]
        if mol is not None:
            mol.SetProp(id, chem_id)
            writer.write(mol)
    writer.close()

    # Store csv file
    columns_to_save = [id, smiles, "standardized_smiles"]
    df[columns_to_save].sort_values(id).to_csv(csv_output_path, index=False)
    print("The shape of the cleaned-up data frame with smiles and mols:")
    print(df.shape)

    # generate FP3 and FP4 OB fingerprints via pybel
    allmols_with_dtxsid = []
    for mol in pybel.readfile("sdf", str(sdf_output_path)):
        if mol is not None:
            # Try to retrieve the molecule_id, default to "Unknown" if not found
            try:
                dtxsid = (
                    mol.OBMol.GetData(id).GetValue()
                    if mol.OBMol.HasData(id)
                    else "Unknown"
                )
            except Exception:
                dtxsid = "Unknown"
            allmols_with_dtxsid.append((dtxsid, mol))

    # FP3
    fps_FP3 = []
    fp3_bits = []
    for item in tqdm(allmols_with_dtxsid, desc="Calculating FP3", unit="mol"):
        dtxsid, mol = item  # Correctly unpack the tuple
        fp = mol.calcfp(fptype="FP3")
        fps_FP3.append({id: dtxsid, "fp": fp})
        fp3_bits.append({id: dtxsid, "bits": fp.bits})

    binary_vectors_fp3 = []
    n_bits = 55

    for item in tqdm(fps_FP3, desc="Processing FP3", unit="mol"):
        fp_bits = item["fp"].bits
        dtxsid = item[id]
        bv = np.zeros(n_bits, dtype=int)
        if fp_bits:
            fp_indexes = [i - 1 for i in fp_bits]
            bv[fp_indexes] = 1
        # Append the bits directly rather than as a 'vector' key
        binary_vectors_fp3.append(
            {**{f"fp3_bit_{i+1}": bv[i] for i in range(n_bits)}, id: dtxsid}
        )

    df_binary_vectors_fp3 = pd.DataFrame(binary_vectors_fp3)
    df_binary_vectors_fp3 = df_binary_vectors_fp3.set_index(id)
    print(f"columns of fp3 df: {df_binary_vectors_fp3.columns}")
    print(f"index of fp3 df: {df_binary_vectors_fp3.index}")

    # FP4
    fps_FP4 = []
    fp4_bits = []
    for item in tqdm(allmols_with_dtxsid, desc="Calculating FP4", unit="mol"):
        dtxsid, mol = item  # Correctly unpack the tuple
        fp = mol.calcfp(fptype="FP4")
        fps_FP4.append({id: dtxsid, "fp": fp})
        fp4_bits.append({id: dtxsid, "bits": fp.bits})

    binary_vectors_fp4 = []
    n_bits = 307  # Adjust the number of bits for FP4

    for item in tqdm(fps_FP4, desc="Processing FP4", unit="mol"):
        fp_bits = item["fp"].bits
        dtxsid = item[id]
        bv = np.zeros(n_bits, dtype=int)
        if fp_bits:
            fp_indexes = [i - 1 for i in fp_bits]
            bv[fp_indexes] = 1
        # Append the bits directly rather than as a 'vector' key
        binary_vectors_fp4.append(
            {**{f"fp4_bit_{i+1}": bv[i] for i in range(n_bits)}, id: dtxsid}
        )

    df_binary_vectors_fp4 = pd.DataFrame(binary_vectors_fp4)
    df_binary_vectors_fp4 = df_binary_vectors_fp4.set_index(id)
    print(f"columns of fp4 df: {df_binary_vectors_fp4.columns}")
    print(f"index of fp4 df: {df_binary_vectors_fp4.index}")

    # concatenate FP3 and FP4
    df_obabel = pd.concat([df_binary_vectors_fp3, df_binary_vectors_fp4], axis=1)
    print("The shape of the obabel data frame:")
    print(df_obabel.shape)
    print("The index of the obabel data frame:")
    print(df_obabel.index)

    # create MACCS, PubChem and Klekota Roth fingerprints with CKW_pywrapper
    mols_list = []
    chem_ids_list = []
    sdf_supplier = Chem.SDMolSupplier(sdf_output_path)

    for mol in tqdm(sdf_supplier, desc="Processing Molecules", unit="mol"):
        if mol is not None:
            mols_list.append(Chem.AddHs(mol))
            chem_ids_list.append(mol.GetProp(id))

    # calculate fingerprints
    cdk = CDK(fingerprint=FPType.MACCSFP)
    df_maccs = cdk.calculate(mols_list, show_banner=False)
    cdk = CDK(fingerprint=FPType.PubchemFP)
    df_pubchem = cdk.calculate(mols_list, show_banner=False)
    cdk = CDK(fingerprint=FPType.KRFP)
    df_klekotaroth = cdk.calculate(mols_list, show_banner=False)

    # concatenate CDK fingerprints
    df_cdk = pd.concat((df_maccs, df_pubchem, df_klekotaroth), axis=1)
    df_cdk.index = chem_ids_list
    print("The shape of the CDK data frame:")
    print(df_cdk.shape)

    # concatenate CKD and pybel fingerprints
    df_fps = pd.concat((df_obabel, df_cdk), axis=1)
    df_fps.dropna(inplace=True)
    print("The shape of the initial combined obabel and pyfps data frame:")
    print(df_fps.shape)
    df_fps.columns = range(len(df_fps.columns))

    # CSI FingerID definitions
    df_csi["absoluteIndex"] = df_csi["absoluteIndex"].astype(int)
    valid_indices = set(df_csi["absoluteIndex"]).intersection(set(df_fps.columns))
    filtered_df_fps = df_fps[list(valid_indices)]
    filtered_df_fps.columns = [str(col).zfill(4) for col in filtered_df_fps.columns]

    # Define the ranges of each fingerprint type
    # This ranges are only informative and not used later on.
    openbabel_fp3_range = range(0, 55)
    openbabel_fp4_range = range(55, 362)
    MACCS_range = range(369, 525)
    PubChem_range = range(659, 1395)
    klekota_range = range(1409, 6267)
    print_info = (
        "The absoluteIndex from csi_fingerid.tsv file "
        "are used as column names. Following fingerprints are generated:\n"
        f"openbabel_fp3 fingerprints (absoluteIndex range {openbabel_fp3_range.start} - {openbabel_fp3_range.stop - 1}),\n"
        f"openbabel_fp4 (CDK Substructure in SIRIUS, absoluteIndex range {openbabel_fp4_range.start} - {openbabel_fp4_range.stop - 1}),\n"
        f"MACCS (absoluteIndex range {MACCS_range.start} - {MACCS_range.stop - 1}),\n"
        f"PubChem (absoluteIndex range {PubChem_range.start} - {PubChem_range.stop - 1}),\n"
        f"Klekota-Roth (absoluteIndex range {klekota_range.start} - {klekota_range.stop - 1})."
    )
    print(print_info)

    filtered_df_fps = filtered_df_fps.reset_index().rename(columns={"index": id})
    filtered_df_fps = filtered_df_fps.sort_values(id)
    if store_as_csv:
        filtered_df_fps.to_csv(fps_output_path, index=False)
    else:
        filtered_df_fps.to_parquet(fps_output_path, index=False)

    print("The shape of the final data frame with fingerprints:")
    print(filtered_df_fps.shape)
