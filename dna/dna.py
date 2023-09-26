import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        return
    database_filename = sys.argv[1]
    sequence_filename = sys.argv[2]

    # Read database file into a variable
    database = read_csv(database_filename)
    
    # Read DNA sequence file into a variable
    sequence = read_sequence(sequence_filename)

    # Find longest match of each STR in DNA sequence
    str_counts = {}
    for str_name in database[0][1:]:
        str_counts[str_name] = longest_match(sequence, str_name)

    # Check database for matching profiles
    match = find_match(database, str_counts)
    if match:
        print(match)
    else:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            
            # If there is no match in the substring
            else:
                break
        
        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run

def read_csv(filename):
    """Reads a CSV file and returns its contents as a list of lists."""
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        return [row for row in reader]

def read_sequence(filename):
    """Reads a text file and returns its contents as a string."""
    with open(filename, mode='r') as file:
        return file.read()

def find_match(database, str_counts):
    """Finds a matching individual in the database based on STR counts."""
    for row in database[1:]:
        name = row[0]
        counts = [int(cell) for cell in row[1:]]
        if counts == [str_counts[str_name] for str_name in database[0][1:]]:
            return name
    return None

main()
