import csv
import re
from prettytable import PrettyTable

class Pyradigms:
    
    def __init__(self, separator=":"):
        self.separator = separator
    
    #This takes a list of keys (in this case, of parameter names) and a hash (in this case, of an entry), and returns a list of values from the hash. Used to combine different parameters
    def get_args(self, list, hash): 
        output = []
        for item in list:
            output.append(hash[item])
        return(output)

    #This uses the above function to create a string like 1PL:PST (from the parameter values 1, PL, and PST)
    def keyify(self, list, hash):
        return re.sub(r"(\d)%s" % self.separator, r"\1", self.separator.join(self.get_args(list, hash))).strip(self.separator)
    
    #This reads entries from a file and creates a 3D hash with the specified parameters as dimensions
    def read_file(self, input_file, x, y, z, filtered_parameters={}, target_string="Form"):
        
        self.target_string = target_string
        
        #Read file of entries
        reader = csv.DictReader(open(input_file))
        
        #Assign axis parameters
        x_dim = x
        y_dim = y
        z_dim = z

        #Convert the CSV file to a list of entries
        entries = []
        for entry in reader:
            entries.append(dict(entry))
        
        if filtered_parameters != {}:
            self.filtered_parameters = filtered_parameters
        #The tables hash will hold all of the tables
        tables = {}
        #Iterate through all entries and create the necessary tables
        for entry in entries:
            z_key = self.keyify(z_dim, entry)
            if z_key not in tables.keys():
                tables[z_key] = {}
    
        #Iterate through all entries and generate the necessary rows in the appropriate tables
        for entry in entries:
            z_key = self.keyify(z_dim, entry)
            my_table = tables[z_key]
            y_key = self.keyify(y_dim, entry)
            if y_key not in my_table.keys():
                my_table[y_key] = {}
    
        #Iterate through all entries and put the form in the appropriate columns
        for entry in entries:
            z_key = self.keyify(z_dim, entry)
            my_table = tables[z_key]
            y_key = self.keyify(y_dim, entry)
            my_y = my_table[y_key]
            good = True
            for col, val in filtered_parameters.items():
                if entry[col] != val:
                    good = False
            if good:
                #Find the appropriate column
                x_key = self.keyify(x_dim, entry)
                if x_key in my_y:
                    my_y[x_key] += "; " + entry[self.target_string]
                else:
                    my_y[x_key] = entry[self.target_string]
        self.tables = tables
        return(tables)
        
    def print_paradigms(self, tables="", name="output", single_file=True, filtered_parameters={}, x_sort_order=[], y_sort_order=[], display=False, fill_empty=False):
        if tables == "":
            tables = self.tables
        if filtered_parameters == {} and hasattr(self, "filtered_parameters"):
            filtered_parameters = self.filtered_parameters
        if fill_empty:
            empty_string = " "
        else:
            empty_string = ""
        output = []
        table_count = 0
        for key, table in tables.items():
            x_values = []
            output.append([])
            output[table_count].append([])
            row_count = 0
            
            for y in table.values():
                for x_key, x in y.items():
                    if x_key not in x_values:
                        x_values.append(x_key)
                        
            if x_sort_order:
                x_sort = {}
                for i, v in enumerate(x_sort_order):
                    x_sort[v] = i
                x_values = sorted(x_values, key=lambda val: str(x_sort[val]) if val in x_sort.keys() else str(val))
                
            output[table_count][row_count].append(key)
            for x in x_values:
                output[table_count][row_count].append(x)
            
            y_values = table.keys()  
            if y_sort_order:
                y_sort = {}
                for i, v in enumerate(y_sort_order):
                    y_sort[v] = i
                y_values = sorted(y_values, key=lambda val: str(y_sort[val]) if val in y_sort.keys() else str(val))

            for x_key in y_values:
                output[table_count].append([])
                row_count += 1
                output[table_count][row_count].append(x_key)
                for i in x_values:
                    output[table_count][row_count].append(empty_string)
                for y_key, y in table[x_key].items():
                    col_count = 0
                    while col_count < len(x_values):
                        if output[table_count][0][col_count+1] == y_key:
                            output[table_count][row_count][col_count+1] = y
                        col_count += 1
            table_count += 1
            output.append([])
        
        if display:
            for output_table in output:
                if output_table == []: continue
                x = PrettyTable()
                x.field_names = output_table[0]
                for output_row in output_table[1:]:
                    x.add_row(output_row)
                print(x)
        
        if name != None:    
            if single_file:    
                with open(name + ".csv", "w") as csvfile:
                    writer = csv.writer(csvfile, delimiter=",")
                    params = []
                    if len(filtered_parameters.keys()) > 0:
                        for col, val in self.filtered_parameters.items():
                            params.append("%s: %s" % (col, val))
                        writer.writerow([";".join(params)])
                        writer.writerow([])
                    for table in output:
                        for row in table:
                            writer.writerow(row)
                        writer.writerow([])
            else:
                for table in output:
                    if table == []: continue
                    with open("%s_" % table[0][0] + name + ".csv", "w") as csvfile:
                        writer = csv.writer(csvfile, delimiter=",")
                        params = []
                        if len(filtered_parameters.keys()) > 0:
                            for col, val in self.filtered_parameters.items():
                                params.append("%s: %s" % (col, val))
                            writer.writerow([";".join(params)])
                            writer.writerow([])
                        for row in table:
                            if row == []: continue
                            writer.writerow(row)