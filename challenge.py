import sys
import time

DICT_ACGT = {0:'A', 1:'C', 2:'G', 3:'T'}
FASTQ_FORMAT = '@READ_{index}\n{dna_sequence}\n+READ_{index}\n{quality_score}\n'

def file_reader(filename, sequence_size):
    """Python generator that yields chunks of bytes from the input file.

    Args:
        filename (str): name/path of the input file
        sequence_size (int): size of the byte chunks

    Yields:
        bytes: string of bytes
    """
    with open(filename, "rb") as input_file:
        while True:
            chunk_of_bytes = input_file.read(sequence_size)
            if chunk_of_bytes:
                yield chunk_of_bytes
            else:
                input_file.close()
                break

def process_piece(chunk_of_bytes):
    """Parse bytes into dna sequence and quality score strings.
    The first two (most significant) bits of each byte encode the DNA letter
    The last six (least significant) bits of each byte encode the quality score.

    Args:
        chunk_of_bytes (bytes): bytes to be decoded

    Returns:
        str: decoded DNA sequence
        str: quality score
    """
    sequence = ""
    quality = ""
    for _ in chunk_of_bytes:
        quality += chr((_ & 0b111111) + 33)
        sequence += str(DICT_ACGT[_ >> 6])
    return sequence, quality

def create_fastq_file(filename,sequence_size):
    """Read input file and decode it.
    Create new file and save the date ib new file in FASTQ format.

    Args:
        filename (str): _description_
        sequence_size (int): _description_
    """
    index = 0
    timestamo = time.time()
    for piece in file_reader(filename, sequence_size):
        index += 1
        dna_sequence, quality_score = process_piece(piece)
        with open(f'output_{timestamo}.txt', "a", encoding="utf-8") as output_file:
            output_file.write(FASTQ_FORMAT.format(index=index,
                                                  dna_sequence=dna_sequence,
                                                  quality_score=quality_score))
            output_file.close()

if __name__ == "__main__":
    filename = sys.argv[1]
    sequence_size  = int(sys.argv[2])
    create_fastq_file(filename, sequence_size)
