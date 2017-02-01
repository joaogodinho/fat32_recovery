'''

Takes a list of files as input, checks the header
and changes the extension accordingly

Created by João Godinho, Jan 2017
'''
import argparse

EXTENSIONS = dict()
EXTENSIONS['jpg'] = b'\xFF\xD8\xFF\xE0'
EXTENSIONS['doc'] = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'
EXTENSIONS['bmp'] = b'\x42\x4D'
EXTENSIONS['docx'] = b'\x50\x4b\x03\x04\x14\x00\x06\x00'
EXTENSIONS['pdf'] = b'\x25\x50\x44\x46'

FOLDERS = dict()
FOLDERS['imgs'] = ['jpg', 'bmp']
FOLDERS['docs'] = ['doc', 'docx', 'pdf']

NULL_CLUSTER = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
DIR = b'\x2E\x20\x20\x20\x20'


def main():
    parser = argparse.ArgumentParser('Takes a list of files and changes the extension according to the header')
    parser.add_argument('files', help='Files to check', nargs='+')
    args = parser.parse_args()
    fix_extension(args.files)


def fix_extension(files):
    dir_counter = 0
    file_counter = 0
    for f in files:
        with open(f, 'rb') as unknown_file:
            header_bytes = unknown_file.read(0x10)
            ext_found = False
            if header_bytes.startswith(NULL_CLUSTER):
                continue
            for ext, header in EXTENSIONS.items():
                if header_bytes.startswith(header):
                    # print('{0} has {1} extension'.format(f, ext))
                    unknown_file.seek(0)
                    create_file(str(file_counter), ext, unknown_file.read())
                    ext_found = True
                    file_counter += 1
                    break
            if header_bytes.startswith(DIR):
                # print('{0} is a directory'.format(f))
                # unknown_file.seek(0)
                # with open('dir' + str(dir_counter), 'wb') as new_dir:
                #     new_dir.write(unknown_file.read())
                # dir_counter += 1
                continue
            if not ext_found:
                print('No extension found for {0} with bytes: 0x{1}'.format(f, header_bytes.hex().upper()))


def create_file(filename, ext, content):
    for f, exts in FOLDERS.items():
        if ext in exts:
            with open(f + '/FILE' + filename + '.' + ext, 'wb') as file:
                file.write(content)
            return


if __name__ == '__main__':
    main()
