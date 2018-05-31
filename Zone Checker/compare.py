# Valid Sections
LOOKUP_TABLE = ["USERNAME", "A", "B", "C", "D", "E", "F", "G"]

# Read Gradescope file and return dataset as dictionary
# Key -> Username | Value -> Zone
def read_gradescope_file(filename):
    file = open(filename)
	
    # Store records in the dictionary
    records = dict()
    for line in file:
        parsed_data = line.strip().split(",")
        for i in range(0, len(parsed_data)):
            if parsed_data[i] == "TRUE":
                records[parsed_data[0]] = LOOKUP_TABLE[i]
    file.close()
	
    return records

	
# Read Submitty file and return dataset as dictionary
# Key -> Username | Value -> Zone
def read_submitty_file(filename):
    file = open(filename)
	
    # Store records in the dictionary
    records = dict()    
    for line in file:
        # Formatting
        line = ' '.join(line.split())
		
		# Extracting Data
        parsed_data = line.strip().split(" ")
		
        # Verify if there was a seating arrangement made for this student
        if len(parsed_data) >= 6:
            zone = parsed_data[5]
			
            # Sanity Check [Errors Currently Suppressed]
            if zone not in LOOKUP_TABLE:
                continue
				
            records[parsed_data[2]] = zone
            
    file.close()     
    return records  


# Compare Datasets and Report Mismatches
def compare(gradescope_seating, submitty_seating):
	# for each entry in Gradescope seating
	for key in gradescope_seating:
		# does there exist a configuration in the rainbow grades configuration?
		if key in submitty_seating:
			#compare the two entries
			if gradescope_seating[key] != submitty_seating[key]:
				print("MISMATCH:", key)
				print("Rainbow Grade Configuration:", submitty_seating[key])
				print("Gradescope Seating:", gradescope_seating[key])
				print("==================")


if __name__ == "__main__":

	# Read Gradescope and Submitty seating input files
	gradescope_seating = read_gradescope_file("gradescope.csv")
	submitty_seating = read_submitty_file("exam_seating")

	# Compare Datasets and Report Mismatches
	compare(gradescope_seating, submitty_seating)