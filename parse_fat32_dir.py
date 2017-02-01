'''

Takes a FAT32 directory cluster
and outputs the directory contents to
a csv file with the same name as input

Created by João Godinho, Jan 2017
'''
import argparse
import struct
import csv


def main():
    parser = argparse.ArgumentParser(description='Takes a directory cluster and outputs the directory listing to csv file with same name.')
    parser.add_argument('cluster_file', help='The file representing the directory cluster')
    args = parser.parse_args()
    entries = parse_file(args.cluster_file)

    with open(args.cluster_file + '.csv', 'w') as csvfile:
        fieldnames = sorted(entries[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)


def parse_file(cluster_file):
    RECORD_SIZE = 0x20
    # Take the file content as binary
    with open(cluster_file, 'rb') as cluster:
        content = cluster.read()


    entries = []
    lfn = ''
    for i in range(0, len(content), RECORD_SIZE):
        raw_entry = content[i:i+RECORD_SIZE]

        # Stop when found multiple nulls, quick hack
        if raw_entry[:0x5] == b'\x00\x00\x00\x00\x00':
            break

        # Prepend the name
        if raw_entry[0x0B] == 0x0F:
            lfn = parse_lfn(raw_entry) + lfn
            continue

        entry = {}
        entry['type'] = 'Dir' if raw_entry[0x0B] & 0x10 else 'File'
        entry['deleted'] = 'Yes' if raw_entry[0x00] == 0xE5 else 'No'
        if lfn == '':
            entry['name'] = raw_entry[:0x0B].decode('utf8', errors='ignore')
        else:
            entry['name'] = lfn
        entry['cluster'] = struct.unpack('<H', raw_entry[0x14:0x16])[0] << 0x10 | struct.unpack('<H', raw_entry[0x1A:0x1C])[0]
        entry['size'] = struct.unpack('<L', raw_entry[0x1C:])[0]
        entries.append(entry)
        lfn = ''

    return entries


# Long File Names are 0x20 bytes entries with at most 13 chars per entry
# at specific offsets
def parse_lfn(entry):
    OFFSETS = [0x01, 0x0E, 0x1C]
    SIZES = [10, 12, 4]
    name = ''

    for idx, offset in enumerate(OFFSETS):
        for c in range(0, SIZES[idx], 2):
            if entry[offset + c] == 0x00:
                return name
            name += chr(entry[offset + c])
    return name


if __name__ == '__main__':
    main()
