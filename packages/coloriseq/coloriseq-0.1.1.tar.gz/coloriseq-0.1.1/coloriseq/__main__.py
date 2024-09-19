import argparse
import re
from tqdm import tqdm
from Bio import SeqIO
from Bio.Seq import Seq

ansi_colors = {
  'red': '\033[31m',
  'yellow': '\033[33m',
  'blue': '\033[34m',
  'magenta': '\033[35m',
  'cyan': '\033[36m',
  'reset': '\033[0m',
  'green': '\033[32m'
}

ansi_bg_colors = {
  'bg_red': '\033[41m',
  'bg_yellow': '\033[43m',
  'bg_blue': '\033[44m',
  'bg_magenta': '\033[45m',
  'bg_cyan': '\033[46m',
  'reset': '\033[0m',
  'bg_green': '\033[42m'
}

colorize_banner="""
 \033[31m██████╗  ██████╗  ██╗       ██████╗  ██████╗  ██╗ ███████╗ ███████╗\033[0m
\033[33m██╔════╝ ██╔═══██╗ ██║      ██╔═══██╗ ██╔══██╗ ██║ ╚══███╔╝ ██╔════╝\033[0m
\033[31m██║      ██║   ██║ ██║      ██║   ██║ ██████╔╝ ██║   ███╔╝  █████╗  \033[0m
\033[33m██║      ██║   ██║ ██║      ██║   ██║ ██╔══██╗ ██║  ███╔╝   ██╔══╝  \033[0m
\033[31m╚██████╗ ╚██████╔╝ ███████╗ ╚██████╔╝ ██║  ██║ ██║ ███████╗ ███████╗\033[0m
\033[33m ╚═════╝  ╚═════╝  ╚══════╝  ╚═════╝  ╚═╝  ╚═╝ ╚═╝ ╚══════╝ ╚══════╝\033[0m

\033[35m           ███████╗  █████╗  ███████╗ ████████╗  █████╗ \033[0m
\033[36m           ██╔════╝ ██╔══██╗ ██╔════╝ ╚══██╔══╝ ██╔══██╗\033[0m
\033[35m           █████╗   ███████║ ███████╗    ██║    ███████║\033[0m
\033[36m           ██╔══╝   ██╔══██║ ╚════██║    ██║    ██╔══██║\033[0m
\033[35m           ██║      ██║  ██║ ███████║    ██║    ██║  ██║\033[0m
\033[36m           ╚═╝      ╚═╝  ╚═╝ ╚══════╝    ╚═╝    ╚═╝  ╚═╝\033[0m
"""

print(colorize_banner)


def parse_arguments():
  parser = argparse.ArgumentParser()                                                                                              
  parser.add_argument('input_fasta', help='input.fasta file to color')
  parser.add_argument('-p', '--patterns-fasta', help='patterns.fasta file to color in the input.fasta (Maximum 5)')
  parser.add_argument('-o', '--output', help='output.colored.fasta\n ')
  parser.add_argument('-r', '--revcomp', action='store_true', help='annotate reverse complement of given patterns too')
  parser.add_argument('--map-patterns', action='store_true', help='color given patterns.fasta file too')
  parser.add_argument('--min-polya', type=int, default=10,
                    help=('Minimum number of bases to annotate polyA sequences (default: 10). '
                          'When used with --revcomp, polyT sequences will also be colored. '
                          'If set to 0, no polyA or polyT sequences will be annotated.'))
  parser.add_argument('--max-substitutions', type=int, default=1, help='Maximum number of substitutions allowed in fuzzy search (default: 1)')
  parser.add_argument('--max-deletions', type=int, default=0, help='Maximum number of deletions allowed in fuzzy search (default: 0)')
  parser.add_argument('--max-insertions', type=int, default=0, help='Maximum number of insertions allowed in fuzzy search (default: 0)')
  return parser.parse_args()

def read_patterns(patterns_fasta, revcomp):
  patterns = {}
  with open(patterns_fasta, 'r') as pattern_file:
    for i, record in enumerate(SeqIO.parse(pattern_file, 'fasta')):
      if i >= 5:
        raise ValueError("Patterns FASTA file must contain no more than 5 records!")
      pattern_seq = str(record.seq)
      patterns[record.id] = {
        'seq': pattern_seq,
        'revcomp': str(Seq(pattern_seq).reverse_complement()) if revcomp else None,
        'color': list(ansi_colors.values())[i]
      }
  return patterns

def find_poly(sequence, poly_base, min_length):
  regions = []
  start = float('inf')
  for i in range(len(sequence)):
    if sequence[i] == poly_base:
      if i < start:
        start = i
      elif i == len(sequence) - 1 and i-1 - start >= min_length:
        regions.append((start, i))
    else:
      if i > start and i-1 - start >= min_length:
        regions.append((start, i-1))
      start = float('inf')
  return regions

def fuzzy_search(sequence, pattern, fuzzy_params):
  fuzzy_pattern = f"({pattern}){{s<={fuzzy_params['max_substitutions']},d<={fuzzy_params['max_deletions']},i<={fuzzy_params['max_insertions']}}}"
  matches = re.finditer(fuzzy_pattern, sequence, re.IGNORECASE)
  regions = []
  for match in matches:
    start = match.start()
    end = match.end() - 1
    regions.append((start, end))
  return regions
    
def color_sequence(sequence, min_polya, polyt, patterns, fuzzy_params):
    colored_sequence = list(sequence)
    if min_polya:
      for start, end in find_poly(sequence, 'A', min_polya): 
        colored_sequence[start] = ansi_colors['green'] + colored_sequence[start]
        colored_sequence[end] += ansi_colors['reset']
      if polyt:
        for start, end in find_poly(sequence, 'T', min_polya):
          colored_sequence[start] = ansi_colors['green'] + colored_sequence[start]
          colored_sequence[end] += ansi_colors['reset']
    if patterns:
      for _, vals in patterns.items():
        color = vals['color']
        for start, end in fuzzy_search(sequence, vals['seq'], fuzzy_params):
          for i in range(start, end):
            colored_sequence[i] = color + colored_sequence[i]
          colored_sequence[end - 1] += ansi_colors['reset']
        if vals['revcomp']:
          for start, end in fuzzy_search(sequence, vals['revcomp'], fuzzy_params):
            for i in range(start, end):
              colored_sequence[i] = color + colored_sequence[i]
            colored_sequence[end - 1] += ansi_colors['reset']
    return "".join(colored_sequence) + ansi_colors['reset']

def main():
  args = parse_arguments()
  patterns = read_patterns(args.patterns_fasta, args.revcomp) if args.patterns_fasta else None
  if args.min_polya < 0:
    raise ValueError(f"Parameter {args.min_polya} must be >= 0") 
  polyt = bool(args.min_polya) and args.revcomp
  fuzzy_params = {
    'max_substitutions': args.max_substitutions,
    'max_deletions': args.max_deletions,
    'max_insertions': args.max_insertions
  }
  for k,v in fuzzy_params.items():
    if v < 0:
      raise ValueError(f"Parameter {k} must be >= 0") 
    
  fasta = SeqIO.parse(args.input_fasta, "fasta")
  if args.output: 
    with open(args.input_fasta, 'r') as file:
      line_cnt = sum(1 for line in file) / 2
    with tqdm(total=line_cnt, bar_format="Coloring reads: {percentage:3.0f}%|{bar}| remaining: {remaining}]") as pbar:
      with open(args.output, "w") as out:
        for record in fasta:
          pbar.update(1)
          print(f">{record.id}\n{color_sequence(str(record.seq), args.min_polya, polyt, patterns, fuzzy_params)}", file=out)
  else:
    for record in fasta:
      print(f">{record.id}\n{color_sequence(str(record.seq), args.min_polya, polyt, patterns, fuzzy_params)}")

if __name__ == '__main__':
  main()
