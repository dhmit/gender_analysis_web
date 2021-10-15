import csv
import os

current_path = os.path.dirname(os.path.abspath(__file__)) # returns path of test.py
test_csv = os.path.join(current_path, 'small_talks.csv') # appends test.csv to the above

def parse_csv(path_to_files):
    # create directory name and loop each csv creating txt file from  'transcript' column
    path_to_folder = os.path.splitext(path_to_files)[0]
    print(f"Path: {path_to_folder}")
    if not os.path.exists(path_to_folder):
        os.mkdir(path_to_folder)
    print(f"Path to files: {path_to_files}")
    with open(path_to_files, encoding='utf-8') as test_data_csv:
        csv_reader = csv.DictReader(test_data_csv)
        for data in csv_reader:
            # filename = ''.join(filter(str.isalnum, data['title'])) + '.txt'
            print(data)
            print("bup")
            filename = f"{data['title']}.txt"
            #filename = filename.replace(...)
            text = data['transcript']
            if not os.path.isfile(os.path.join(path_to_folder, filename)):  # "If the file title.txt' doesn't exist in the designated folder...

                with open(os.path.join(path_to_folder, filename), "w", encoding='utf8') as f:
                    f.write(text)
    return path_to_folder

def test_function():
    print(test_csv)
    with open(test_csv, encoding='utf-8') as test_data:
        test_csv_reader = csv.DictReader(test_data)
        for row in test_csv_reader:
            print(row)

#def convert_ted_talks_csv(csv_path):
#    with open(csv_path, encoding='utf-8') as csv_file:
#        reader = csv.reader(csv_file)
#        for line in reader:
#            print(line)


if __name__ == '__main__':
    parse_csv(test_csv)