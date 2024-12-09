import argparse
from itertools import islice

def split_fasta(input_fasta, train_fasta, test_fasta, split_ratio=0.7):
    with open(input_fasta, 'r') as infile:
        entries = []
        while True:
            header = infile.readline()
            if not header:
                break
            sequence = infile.readline()
            entries.append((header, sequence))
    
    train_size = int(len(entries) * split_ratio)
    train_entries = entries[:train_size]
    test_entries = entries[train_size:]
    
    with open(train_fasta, 'w') as train_out, open(test_fasta, 'w') as test_out:
        for entry in train_entries:
            train_out.writelines(entry)
        for entry in test_entries:
            test_out.writelines(entry)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a FASTA file into training and testing sets.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTA file")
    parser.add_argument("-train", "--train_output", required=True, help="Output training FASTA file")
    parser.add_argument("-test", "--test_output", required=True, help="Output testing FASTA file")
    parser.add_argument("-r", "--ratio", type=float, default=0.7, help="Split ratio for training data (default: 0.7)")
    args = parser.parse_args()

    split_fasta(args.input, args.train_output, args.test_output, args.ratio)
