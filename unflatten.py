import json
from argparse import ArgumentParser


def unflatten(doc, separator='.'):
    """Unflattens a flattened dictionary."""
    result = {}
    for k, v in doc.items():
        parts = k.split(separator)
        current = result
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current[part] = v
            else:
                if part not in current:
                    # Check if the next part is an integer (for lists)
                    try:
                        int(parts[i+1])
                        current[part] = [] # Initialize as list
                    except ValueError:
                        current[part] = {} # Initialize as dictionary
                current = current[part]
    return result


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('file', help='ndjson file with data to unflatten')
    parser.add_argument('target', help='target file name for unflattened data')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # Example usage:
    args = parse_args()
    with open(args.file) as f:
        with open(args.target, 'w') as f2:
            for line in f:
                doc = json.loads(line)
                unflattened = unflatten(doc)
                f2.write(json.dumps(unflattened))
                f2.write('\n')