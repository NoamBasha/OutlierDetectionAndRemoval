import csv
import time
import datetime
import pandas as pd


def read_csv_to_df(path, id_col_name, columns):
    if id_col_name is None:
        dtf = pd.read_csv(path)
    else:
        dtf = pd.read_csv(path, index_col=id_col_name)
    dtf = dtf[columns]
    return dtf

def copy_without_header(from_path, to_path):
    dtf = pd.read_csv(from_path, low_memory=False)
    dtf.to_csv(to_path, index=False, header=False)
    
    
def write_dataset_to_csv(path, dataset):
    try:
        with open(path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(dataset)
    except:
        print("Could not write a new file. There might not be permission. You can use the CSVs attached.")


def brazilian_houses_to_data_set(old_path, new_path):
    brazilian_houses_dataset = list()
    with open(old_path, encoding='utf-8', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i == 0:
                del row[0]
                """`
                for j in range(data_binary.shape[1], 0, -1):
                    row = ["city-{}".format(j)] + row
                row = ["Id"] + row
                """
            else:
                if row[5] == '-':
                    row[5] = 0
                row[6] = (1 if row[6] == 'acept' else 0)
                row[7] = (1 if row[7] == 'furnished' else 0)
                # city_ind = brazilian_houses_cities_list.index(row[0])
                del row[0]
                # row = data_binary.values[city_ind].tolist() + row
                # row = [i] + row
            brazilian_houses_dataset.append(row)
    write_dataset_to_csv(new_path, brazilian_houses_dataset)


def COVID_symptoms_to_data_set(old_path, new_path):
    covid_symptoms_dataset = list()
    with open(old_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(reader):
            del row[-1]
            del row[19:22]
            covid_symptoms_dataset.append(row)
    write_dataset_to_csv(new_path, covid_symptoms_dataset)


def goodreads_books_to_data_set(old_path, new_path):
    goodreads_books_dataset = list()
    with open(old_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(reader):
            if i == 0:
                author_row = []
                lancode_row = []
                publisher_row = []
                del row[0:3]
                del row[1:4]
                del row[-1]
            else:
                del row[0:2]
                del row[0]
                try:
                    float(row[0])
                except:
                    del row[0]
                del row[1:4]
                del row[-1]
                try:
                    t = datetime.datetime.strptime(row[-1], "%m/%d/%Y")
                    if t == datetime.datetime(1970, 1, 1):
                        row[-1] = 0.0
                    elif t.year < 1970:
                        epoch = datetime.datetime(1970, 1, 1)
                        t = datetime.datetime.strptime(row[-1], "%m/%d/%Y")
                        diff = t - epoch
                        row[-1] = diff.total_seconds()
                    else:
                        row[-1] = time.mktime(datetime.datetime.strptime(row[-1],
                                                                         "%m/%d/%Y").timetuple())
                except Exception as e:
                    row[-1] = 0.0
            if i != 0:
                for r in row:
                    if r is str:
                        r = r.replace("\"", "")
                        r = float(r)
            goodreads_books_dataset.append(row)
    write_dataset_to_csv(new_path, goodreads_books_dataset)


def Jan_flight_delay_to_data_set(old_path, new_path):
    jan_flights_dataset = list()
    with open(old_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(reader):
            flag = True
            del row[2:7]
            del row[3:5]
            del row[4:6]
            del row[6]
            if i != 0:
                for i in range(len(row)):
                    if '\"' in row[i]:
                        row[i] = row[i].replace("\"", "")
                    if row[i] == '':
                        flag = False
            if flag:
                jan_flights_dataset.append(row)
    write_dataset_to_csv(new_path, jan_flights_dataset)
