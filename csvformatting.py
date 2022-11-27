import csv


with open('2022fixturesfixed.csv') as f_input:
    data = list(csv.reader(f_input))
with open('2022fixtures.csv', 'w', newline='') as f_output:
    csv_output = csv.writer(f_output) 
    for row in data:
        if row[3] == "@":
            csv_output.writerow([row[0], row[1], row[4], row[2], row[6], row[5]])
        else:
            csv_output.writerow([row[0], row[1], row[2], row[4], row[5], row[6]])
# csv rewriting program which can be used for updating 2022 fixtures csv