from PIL import Image
import streamlit as st
import pandas as pd
import altair as alt

image = Image.open("dna-logo.jpg")

# Display the image and expand to column width
st.image(image, use_column_width=True)

st.write(
    """
    # DNA Nucleotide Count

    Counts the nucleotide composition of a query DNA

    ***
    """
)

st.header("DNA Sequence")

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area("Sequence input", sequence_input, height=130).splitlines()
sequence = sequence[1:]  # omit the sequence name
sequence = "".join(sequence)  # concaternate list to string

# Horizontal line break
st.write(
    """
    ***
    """
)

st.header("Input DNA Query")
sequence

st.header("Output DNA Nucleotide Count")


# 1. Print the dictionary
st.subheader("1. Print dictionary")


def DNA_nucleotide_count(seq):
    count = dict(
        [
            ("A", seq.count("A")),
            ("T", seq.count("T")),
            ("G", seq.count("G")),
            ("C", seq.count("C")),
        ]
    )
    return count


DNA_count = DNA_nucleotide_count(sequence)
DNA_count

# 2. Print the count
st.subheader("2. Print text")
st.write("There are " + str(DNA_count["A"]) + " adenine (A).")
st.write("There are " + str(DNA_count["T"]) + " thymine (T).")
st.write("There are " + str(DNA_count["G"]) + " guanine (G).")
st.write("There are " + str(DNA_count["C"]) + " cytosine (C).")

# 3. Display the data frame
st.subheader("3. Display data frame")
df = pd.DataFrame.from_dict(DNA_count, orient="index")
df = df.rename({0: "Count"}, axis="columns")  # rename 0 to count
df.reset_index(inplace=True)
df = df.rename(columns={"index": "Nucleotide"})
st.write(df)

# 4. Display the bar chart from the data frame
st.subheader("4. Display bar chart")
bar_chart = alt.Chart(df).mark_bar().encode(x="Nucleotide", y="Count")
bar_chart = bar_chart.properties(width=alt.Step(80))  # bar widths
st.write(bar_chart)
