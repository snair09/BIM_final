#!/bin/bash

PROTEIN=$1

# Define methods
METHODS=("clipper" "skipper")

# Loop through methods and process each one
for METHOD in "${METHODS[@]}"; do
    echo "Processing ${METHOD} for ${PROTEIN}..."

    # Input and output paths
    INPUT_DIR="input/${METHOD}/${PROTEIN}"
    OUTPUT_BED="${INPUT_DIR}/${METHOD}_5p.bed"
    OUTPUT_SKIP="${INPUT_DIR}/${METHOD}_c.bed"
    TRAIN_FASTA_POS="${INPUT_DIR}/positives_train.fasta"
    TRAIN_FASTA_NEG="${INPUT_DIR}/negatives_train.fasta"
    TEST_FASTA_POS="${INPUT_DIR}/positives_test.fasta"
    TEST_FASTA_NEG="${INPUT_DIR}/negatives_test.fasta"
    MODEL_PREFIX="${PROTEIN}.${METHOD}"

    # Step 1: Convert data to BED format
    if [[ "${METHOD}" == "clipper" ]]; then
        python clipper_to_bed.py -i "${INPUT_DIR}/${METHOD}.bed" -o "${OUTPUT_BED}"
    elif [[ "${METHOD}" == "skipper" ]]; then
        python skipper_to_bed.py -i "${INPUT_DIR}/${METHOD}.tsv" -o "${OUTPUT_SKIP}"
    fi

    # Step 2: Preprocessing
    bash pre.sh "${PROTEIN}"
    bash pre_skip.sh "${PROTEIN}"

    # Log lengths of positive training sequences
    #grep ">" "${TRAIN_FASTA_POS}" | wc -l > "${INPUT_DIR}/positives_train_lengths.log"

    # Step 3: GraphProt training
    echo "Starting training for ${METHOD}..."
    GraphProt.pl -mode classification -action train \
        -fasta "${TRAIN_FASTA_POS}" \
        -negfasta "${TRAIN_FASTA_NEG}" \
        -prefix "${MODEL_PREFIX}"

    # Step 4: GraphProt prediction
    echo "Starting prediction for ${METHOD}..."
    GraphProt.pl -mode classification -action predict \
        -fasta "${TEST_FASTA_POS}" \
        -negfasta "${TEST_FASTA_NEG}" \
        -model "${MODEL_PREFIX}.model" \
        -prefix "${MODEL_PREFIX}"

    echo "#############################Completed ${METHOD} for ${PROTEIN}.##############################"
done

echo "Pipeline completed for ${PROTEIN}."
