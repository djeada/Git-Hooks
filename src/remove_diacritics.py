
# get file name from command line
import sys
import pathlib

def remove_diacritics(file_name: str) -> None:
    
    # read file contents
    with open(file_name, 'r', encoding='utf-8') as file:
        contents = file.read()

    # replace each character from ąāáǎàćēéěèęīíǐìłńōóǒòóśūúǔùǖǘǚǜżźĄĀÁǍÀĆĒĘÉĚÈĪÍǏÌŁŃŌÓǑÒÓŚŪÚǓÙǕǗǙǛŻŹ
    # with a respective character from aaaaaceeeeeiiiilnooooosuuuuüüüüzzAAAAACEEEEEIIIILNOOOOOSUUUUÜÜÜÜZZ
    contents = contents.replace('ą', 'a')
    contents = contents.replace('ā', 'a')
    contents = contents.replace('á', 'a')
    contents = contents.replace('ǎ', 'a')
    contents = contents.replace('à', 'aa')
    contents = contents.replace('ć', 'c')
    contents = contents.replace('č', 'c')
    contents = contents.replace('ĉ', 'c')
    contents = contents.replace('ċ', 'c')
    contents = contents.replace('ę', 'e')
    contents = contents.replace('ē', 'e')
    contents = contents.replace('ė', 'e')
    contents = contents.replace('ě', 'e')
    contents = contents.replace('ī', 'i')
    contents = contents.replace('į', 'i')
    contents = contents.replace('ĩ', 'i')
    contents = contents.replace('ĭ', 'i')
    contents = contents.replace('ł', 'l')
    contents = contents.replace('ń', 'n')
    contents = contents.replace('ň', 'n')
    contents = contents.replace('ņ', 'n')
    contents = contents.replace('ō', 'o')
    contents = contents.replace('ŏ', 'o')
    contents = contents.replace('ó', 'o')
    contents = contents.replace('ő', 'o')
    contents = contents.replace('ś', 's')
    contents = contents.replace('ŝ', 's')
    contents = contents.replace('š', 's')
    contents = contents.replace('ŭ', 'u')
    contents = contents.replace('ų', 'u')
    contents = contents.replace('ű', 'u')
    contents = contents.replace('ũ', 'u')
    contents = contents.replace('ů', 'u')
    contents = contents.replace('ź', 'z')
    contents = contents.replace('ż', 'z')
    contents = contents.replace('Ą', 'A')
    contents = contents.replace('Ā', 'A')
    contents = contents.replace('Á', 'A')
    contents = contents.replace('Ǎ', 'A')
    contents = contents.replace('À', 'A')
    contents = contents.replace('Ć', 'C')
    contents = contents.replace('Č', 'C')
    contents = contents.replace('Ĉ', 'C')
    contents = contents.replace('Ċ', 'C')
    contents = contents.replace('Ę', 'E')
    contents = contents.replace('Ē', 'E')
    contents = contents.replace('Ė', 'E')
    contents = contents.replace('Ě', 'E')
    contents = contents.replace('Ī', 'I')
    contents = contents.replace('Į', 'I')
    contents = contents.replace('Ĩ', 'I')
    contents = contents.replace('Ĭ', 'I')
    contents = contents.replace('Ł', 'L')
    contents = contents.replace('Ń', 'N')
    contents = contents.replace('Ň', 'N')
    contents = contents.replace('Ņ', 'N')
    contents = contents.replace('Ō', 'O')
    contents = contents.replace('Ŏ', 'O')
    contents = contents.replace('Ó', 'O')
    contents = contents.replace('Ő', 'O')
    contents = contents.replace('Ś', 'S')
    contents = contents.replace('Ŝ', 'S')   
    contents = contents.replace('Š', 'S')
    contents = contents.replace('Ŭ', 'U')
    contents = contents.replace('Ų', 'U')
    contents = contents.replace('Ű', 'U')
    contents = contents.replace('Ũ', 'U')
    contents = contents.replace('Ů', 'U')
    contents = contents.replace('Ź', 'Z')
    contents = contents.replace('Ż', 'Z')

    # write file contents
    with open(file_name, 'wb') as file:
        file.write(bytes(contents, "UTF-8"))

if __name__ == '__main__':

    # check if user provided file name
    if len(sys.argv) != 2:
        print('Usage: python remove_carriage_return.py <dir_name>')
        exit()
    
    # check if file exists
    file_name = sys.argv[1]

    if not pathlib.Path(file_name).is_dir():
        print('Dir does not exist')
        exit()
    
    # find all files in directory and remove carriage return
    for file in pathlib.Path(file_name).glob('**/*'):
        if file.is_file():
            remove_diacritics(file)
