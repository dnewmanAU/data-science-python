import numpy as np
import pandas as pd
import streamlit as st
import pickle
from PIL import Image
from rdkit import Chem
from rdkit.Chem import Descriptors

# Calculate molecular descriptors
def AromaticProportion(m):
    aromatic_atoms = list()
    for i in range(m.GetNumAtoms()):
        aromatic_atoms.append(m.GetAtomWithIdx(i).GetIsAromatic())

    aa_count = []
    for i in aromatic_atoms:
        if i == True:
            aa_count.append(1)

    AromaticAtom = sum(aa_count)
    HeavyAtom = Descriptors.HeavyAtomCount(m)
    AR = AromaticAtom / HeavyAtom

    return AR


def generate(smiles):
    mol_data = []
    for elem in smiles:
        mol = Chem.MolFromSmiles(elem)
        mol_data.append(mol)

    base_data = np.arange(1, 1)
    i = 0
    for mol in mol_data:
        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
        desc_AromaticProportion = AromaticProportion(mol)
        row = np.array(
            [desc_MolLogP, desc_MolWt, desc_NumRotatableBonds, desc_AromaticProportion]
        )

        if i == 0:
            base_data = row
        else:
            base_data = np.vstack([base_data, row])

        i += 1

    col_names = ["MolLogP", "MolWt", "NumRotatableBonds", "AromaticProportion"]
    descriptors = pd.DataFrame(data=base_data, columns=col_names)

    return descriptors


# Title
image = Image.open("solubility-logo.jpg")
st.image(image, use_column_width=True)
st.write(
    """
# Molecular Solubility Prediction

Predict the **Solubility (LogS)** values of molecules.

Data obtained from the John S. Delaney. [ESOL: Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x). ***J. Chem. Inf. Comput. Sci.*** 2004, 44, 3, 1000-1005.
"""
)

# Input molecules (sidebar)
st.sidebar.header("User Input Molecules")
smiles_input = "NCCCC\nCCC\nCN"
smiles = st.sidebar.text_area("SMILES Input", smiles_input)
smiles = "C\n" + smiles  # adds C as a dummy first item
smiles = smiles.split("\n")

st.header("Input SMILES")
smiles[1:]  # skip the dummy first item

# Calculate molecular descriptors
st.header("Computed molecular descriptors")
x = generate(smiles)
x[1:]  # skip the dummy first item

# Load pre-built model
load_model = pickle.load(open("solubility_model.pkl", "rb"))

# Apply model to make predictions
predictions = load_model.predict(x)
st.header("Predicted LogS values")
predictions[1:]
