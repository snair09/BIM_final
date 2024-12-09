import argparse

def process_fasta(input_fasta, output_fasta):
    with open(input_fasta, 'r') as f_in, open(output_fasta, 'w') as f_out:
        while True:
            header = f_in.readline()
            if not header:
                break  # End of file
            assert header.startswith('>'), f"Invalid FASTA header: {header}"
            sequence = f_in.readline().strip()
            
            # Skip sequences containing 'N'
            if 'N' in sequence.upper():
                continue
            
            # Process the sequence: first 150 lowercase, middle uppercase, last 150 lowercase
            if len(sequence) > 300:
                lower_5prime = sequence[:150].lower()
                middle = sequence[150:-150].upper()
                lower_3prime = sequence[-150:].lower()
                processed_seq = lower_5prime + middle + lower_3prime
            else:
                # If sequence length <= 300, lowercase all bases
                processed_seq = sequence.lower()
            
            # Write to output
            f_out.write(header)
            f_out.write(processed_seq + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process FASTA sequences to format regions with specific case.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTA file")
    parser.add_argument("-o", "--output", required=True, help="Output FASTA file")
    args = parser.parse_args()

    process_fasta(args.input, args.output)
