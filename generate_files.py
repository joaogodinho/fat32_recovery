'''

Takes the output CSV of get_files.py and the data and
generates the files

Created by João Godinho, Jan 2017
'''
import argparse
import struct
import csv


def main():
    parser = argparse.ArgumentParser('Takes the output CSV of get_fiels.py and the FAT data and generates the files')
    parser.add_argument('files_csv', help='CSV with the file name and corresponding clusters')
    parser.add_argument('fat_data', help='The FAT data, from which files are generated')
    args = parser.parse_args()
    generate_files(args.files_csv, args.fat_data)


def generate_files(files_csv, fat_data):
    fat_data = open(fat_data, 'rb')
    try:
        with open(files_csv, 'r') as csv_file:
            files = csv.DictReader(csv_file)
            for file in files:
                clusters = list(map(int, file['clusters'].split(';')))
                name = file['name']
                with open(name, 'wb') as out_file:
                    out_file.write(get_file(fat_data, clusters, int(file['size'])))
    finally:
        fat_data.close()


# Takes a FAT data pointer and a cluster list and returns
# the file
def get_file(fat, clusters, size):
    # Cluster start at minus 2, since first cluster is #2
    OFFSET = 0x2
    # Cluster size
    CLUSTER_SIZE = 0x1000
    result = b''
    for cluster in clusters:
        fat.seek((cluster - OFFSET) * CLUSTER_SIZE)
        result += fat.read(CLUSTER_SIZE)
    return result[:size]


if __name__ == '__main__':
    main()
