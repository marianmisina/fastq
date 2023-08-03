SEQUENCE_SIZE = 80
DICT_ACGT = {0:'A', 1:'C', 2:'G', 3:'T'}
FILENAME = "input"

def file_reader(filename, sequence_size):
    with open(filename, "rb") as input_file:
        while True:
            chunk_of_bytes = input_file.read(sequence_size)
            if chunk_of_bytes:
                yield chunk_of_bytes
            else:
                input_file.close()
                break

def process_piece(chunk_of_bytes):
    sequence = ""
    quality = ""
    for _ in chunk_of_bytes:
        quality += chr((_ & 0b111111) + 33)
        sequence += str(DICT_ACGT[_ >> 6])
    return sequence, quality

index = 0
for piece in file_reader(FILENAME, SEQUENCE_SIZE):
    index += 1
    dna_sequence, quality_score = process_piece(piece)
    with open("output.txt", "a", encoding="utf-8") as output_file:
        output_file.write(f'@READ_{index}\n{dna_sequence}\n+READ_{index}\n{quality_score}\n')
        output_file.close()
