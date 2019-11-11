import csv
import re

class Pyradigms:
    
    def __init__(self, output_file):
        self.output_file = output_file
    
    #This takes a list of keys (in this case, of parameter names) and a hash (in this case, of an entry), and returns a list of values from the hash. Used to combine different parameters
    def get_args(self, list, hash): 
        output = []
        for item in list:
            output.append(hash[item])
        return(output)

    #This uses the above function to create a string like 1PL:PST (from the parameter values 1, PL, and PST)
    def keyify(self, list, hash):
        return re.sub(r"(\d):", r"\1", ":".join(self.get_args(list, hash))).strip(":")
    
    #This reads entries from a file and creates a 3D hash with the specified parameters as dimensions
    def create_hash(self, input_file, x, y, z, filtered_parameters={}):
        
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
                my_y[x_key] = entry["Form"]
        self.tables = tables
        return(tables)
        
    def print_paradigms(self, tables="", filtered_parameters={}):
        if tables == "":
            tables = self.tables
        if filtered_parameters == {} and hasattr(self, "filtered_parameters"):
            filtered_parameters = self.filtered_parameters
        output = []
        table_count = 0
        for key, table in tables.items():
            x_values = []
            y_values = []
            output.append([])
            output[table_count].append([])
            row_count = 0
            for y_key, y in table.items():
                if y_key not in y_values:
                    y_values.append(y_key)
                for x_key, x in y.items():
                    if x_key not in x_values:
                        x_values.append(x_key)
            output[table_count][row_count].append(key)
            for x in x_values:
                output[table_count][row_count].append(x)
            for x_key in table.keys():
                output[table_count].append([])
                row_count += 1
                output[table_count][row_count].append(x_key)
                for i in x_values:
                    output[table_count][row_count].append("")
                for y_key, y in table[x_key].items():
                    col_count = 0
                    while col_count < len(x_values):
                        if output[table_count][0][col_count+1] == y_key:
                            output[table_count][row_count][col_count+1] = y
                        col_count += 1
            table_count += 1
            output.append([])
            
        with open(self.output_file, "w") as csvfile:
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