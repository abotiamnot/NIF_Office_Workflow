import csv
import pandas as pd

def leave(id, start, end, type, length, reason):
    data = [id, start, end, type, length, reason]
    with open('record.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows([data])

def generate(id):
    load_data = pd.read_csv('record.csv', names=['id', 'start', 'end', 'type', 'length', 'reason'])
    load_data = load_data.applymap(str)
    length_ = len(load_data['id'])
    column_names=['Duration', 'Leave Type', 'Reason']
    list_ = [column_names]
    for x in range(0, length_):
        if(load_data['id'][x] == id):
            duration = "{} to {}".format(load_data['start'][x], load_data['end'][x])
            list_.append([duration, load_data['type'][x], load_data['reason'][x]])
    saved_records = pd.DataFrame(list_[1:], columns=list_[0])
    fname = "{} Employee Record.csv".format(id)
    saved_records.to_csv(fname, index=False)
