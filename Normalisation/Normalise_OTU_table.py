def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        help='filepath of OTU table')
    parser.add_argument('-r', '--rel',
                        help='output relative abundance')
    return parser.parse_args()

def normalise(data, r):
    if not r:
        sum_row = data
        min_sum = min(data.sum())
        normalised = data / sum_row * min_sum
        return normalised
    elif r:
        sum_row = otu.sum()
        min_sum = min(otu.sum())
        rel_abund = otu * 100 / sum_row
        return rel_abund

           
def main():
    args=parse_arguments(sys.argv)
    if args.input:
        data = pd.read_table(args.input, sep="\t", header=0, index_col=0)
    else: 
        print("Error input file not found")
    if args.rel:
        normalised_otu = normalise(data, "r")
        return normalised_otu.to_csv("otu_normalised.tab", sep="\t", encoding="utf-8")
    elif not args.rel:
        normalised_otu = normalise(data)
        return normalised_otu.to_csv("otu_normalised.tab", sep="\t", encoding="utf-8")

if __name__ == '__main__':
    main()