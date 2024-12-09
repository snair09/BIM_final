import argparse

def tsv_to_bed(tsv_file, output_bed, max_lines=5000):
    with open(tsv_file, 'r') as infile, open(output_bed, 'w') as outfile:
        line_count = 0
        for line in infile:
            # Stop if we have written max_lines
            if line_count >= max_lines:
                break

            # Skip header lines if present
            if line.startswith("chr") and "start" in line and "end" in line:
                continue
            
            # Parse TSV line
            cols = line.strip().split('\t')
            chrom, start, end, name, score, strand = cols[0], cols[1], cols[2], cols[3], cols[4], cols[5]
            
            # Modify chromosome names
            if chrom.startswith("chr"):
                chrom = chrom[3:]  # Remove 'chr'
            if chrom == "M":
                chrom = "MT"       # Change 'M' to 'MT'

            # Calculate the center position
            start, end = int(start), int(end)
            center = int((start + end) / 2)
            
            # Write in BED6 format
            bed_line = f"{chrom}\t{center}\t{center + 1}\t{name}\t{score}\t{strand}\n"
            outfile.write(bed_line)
            line_count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Skipper TSV to BED with center positions, remove 'chr', convert 'M' to 'MT', and limit output to 4,000 lines.")
    parser.add_argument("-i", "--input", required=True, help="Input Skipper TSV file")
    parser.add_argument("-o", "--output", required=True, help="Output BED file")
    parser.add_argument("--max_lines", type=int, default=4000, help="Maximum number of lines to output (default: 4000)")
    args = parser.parse_args()
    
    tsv_to_bed(args.input, args.output, args.max_lines)
