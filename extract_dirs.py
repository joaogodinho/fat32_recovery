'''

Takes FAT32 data and extracts all clusters
that look like a directory

'''
import argparse


def main():
    parser = argparse.ArgumentParser(description='Takes a FAT32 data and extracts all clusters that look like a directory')
    parser.add_argument('fat_data', help='The file representing the data')
    args = parser.parse_args()
    parse_file(args.fat_data)


def parse_file(fat_data):
    # Bytes to check if dir
    CHECK = b'\x2E\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20'
    # Size in bytes
    CLUSTER_SIZE = 0x1000

    data = ''

    with open(fat_data, 'rb') as file_data:
        # CAREFUL!!!!1111 Doing this because the data is smallish (~4GB)
        # This way I'm removing the disk bottleneck
        data = file_data.read()

    for i in range(0, len(data), CLUSTER_SIZE):
        if data[i:i+len(CHECK)] == CHECK:
            # Position is + 2 because cluster 0 is actually in number 2
            print('Found dir @ {0}'.format(i + 2))
            with open('cluster' + str(int(i/CLUSTER_SIZE) + 2), 'wb') as dirfile:
                # Assuming a directory is at most one cluster long, might not
                # be the case, but it's not important right now
                dirfile.write(data[i:i+CLUSTER_SIZE])
        else:
            continue


if __name__ == '__main__':
    main()
