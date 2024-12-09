#!/bin/bash

# Variables
RBP=${1}  # Pass the RBP name as the first argument
GENOME_FA="annot/Homo_sapiens.GRCh38.dna.primary_assembly.fa"
GENOME_FAI="${GENOME_FA}.fai"
#
# Directories
INPUT_DIR="input/skipper/${RBP}"
#
# Ensure input directory exists
if [ ! -d "${INPUT_DIR}" ]; then
    echo "Error: Directory ${INPUT_DIR} does not exist."
    exit 1
fi



# Step 2: Extend BED file
echo "Extending BED file by 202 bp on both sides..."
bedtools slop -i ${INPUT_DIR}/skipper_c.bed -g ${GENOME_FAI} -b 202 > ${INPUT_DIR}/ext.bed

# Step 3: Convert extended BED to FASTA
echo "Converting extended BED to FASTA..."
bedtools getfasta -s -fi ${GENOME_FA} -bed ${INPUT_DIR}/ext.bed -fo ${INPUT_DIR}/ext.fasta

# Step 4: Process positives.fasta
echo "Processing positives.fasta..."
python process_fasta.py -i ${INPUT_DIR}/ext.fasta -o ${INPUT_DIR}/positives.fasta

# Step 5: Create negatives.bed by shuffling peaks
echo "Creating negatives.bed..."
bedtools shuffle -i ${INPUT_DIR}/skipper_c.bed -g ${GENOME_FAI} -excl ${INPUT_DIR}/ext.bed > ${INPUT_DIR}/negatives.bed

# Step 6: Extend negatives.bed
echo "Extending negatives.bed by 202 bp on both sides..."
bedtools slop -i ${INPUT_DIR}/negatives.bed -g ${GENOME_FAI} -b 202 > ${INPUT_DIR}/negatives_ext.bed

# Step 7: Sanity check for overlap
echo "Performing sanity check for overlaps..."
bedtools intersect -a ${INPUT_DIR}/ext.bed -b ${INPUT_DIR}/negatives_ext.bed > ${INPUT_DIR}/overlaps.bed

# Step 8: Convert extended negatives BED to FASTA
echo "Converting extended negatives BED to FASTA..."
bedtools getfasta -s -fi ${GENOME_FA} -bed ${INPUT_DIR}/negatives_ext.bed -fo ${INPUT_DIR}/negatives_ext.fasta

# Step 9: Process negatives.fasta
echo "Processing negatives.fasta..."
python process_fasta.py -i ${INPUT_DIR}/negatives_ext.fasta -o ${INPUT_DIR}/negatives.fasta

# Step 10: Split positives.fasta into train/test
echo "Splitting positives.fasta into train/test..."
python split_fasta.py -i ${INPUT_DIR}/positives.fasta -train ${INPUT_DIR}/positives_train.fasta -test ${INPUT_DIR}/positives_test.fasta -r 0.7

# Step 11: Split negatives.fasta into train/test
echo "Splitting negatives.fasta into train/test..."
python split_fasta.py -i ${INPUT_DIR}/negatives.fasta -train ${INPUT_DIR}/negatives_train.fasta -test ${INPUT_DIR}/negatives_test.fasta -r 0.7

echo "Preprocessing complete for RBP: ${RBP} skippy"