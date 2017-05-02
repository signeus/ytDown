import sys
from ytDown import YtDown

if __name__ == '__main__':
    searchText = ""
    if(len(sys.argv) > 1):
        searchText = str(sys.argv[1])
    else:
        searchText = input("What's your search? ")
    YtDown().getMeThat(searchText)