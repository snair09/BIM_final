import argparse

### Makes it the same format as genome annotation file and limits to the first 8000 lines

def parse_bed(bed_file, output_bed):
    with open(bed_file, 'r') as infile, open(output_bed, 'w') as outfile:
        line_count = 0
        for line in infile:
            if line_count >= 5000:
                break  # Stop processing after 8000 lines
            
            cols = line.strip().split('\t')
            chrom, start, end, name, score, strand = cols[:6]
            
            # Modify chromosome names
            if chrom.startswith("chr"):
                chrom = chrom[3:]  # Remove 'chr'
            if chrom == "M":
                chrom = "MT"       # Change 'M' to 'MT'
            
            # Adjust based on strand
            if strand == '+':
                end = str(int(start) + 1)  # 5' end for '+' strand
            elif strand == '-':
                start = str(int(end) - 1)  # 5' end for '-' strand
            else:
                raise ValueError(f"Unexpected strand '{strand}' in line: {line.strip()}")
            
            # Write updated BED6 format
            bed_line = f"{chrom}\t{start}\t{end}\t{name}\t{score}\t{strand}\n"
            outfile.write(bed_line)

            line_count += 1  # Increment the line counter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Clipper BED to 5' cross-link sites, remove 'chr', convert 'M' to 'MT', and limit to the first 8000 lines.")
    parser.add_argument("-i", "--input", required=True, help="Input BED file")
    parser.add_argument("-o", "--output", required=True, help="Output BED file")
    args = parser.parse_args()
    
    parse_bed(args.input, args.output)
