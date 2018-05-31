# read student list ripped from Submitty. See example file
# returns dictionary: keys => section ID  values => student IDs in a list, alphabetical order
def read_student_sections(filename):
    file = open(filename)
    
    sections = dict()
    
    # parse out data
    for line in file:
        parsed_data = line.strip().split(" ")
        section_id = parsed_data[1]
		
        # skip the header lines
        if section_id == "Enrolled":
            continue
			
        student_id = parsed_data[2]
        if section_id not in sections:
            sections[section_id] = list()
			
        sections[section_id].append(student_id)
        
    # sort names alphabetically
    for key in sections:
        sections[key].sort()
        
    file.close()
    return sections
    
        
# Read in the rainbowgrades HTML file and return the header block, closing block, and student records
def read_rainbowgrades(filename):
    file = open(filename)
    
    data = file.read()
    
    parsed_data = data.split("<tr>")
    
    header = parsed_data.pop(0) + '<tr>' # HTML Header
    header += parsed_data.pop(0) + '<tr>' # first row is the column names
    header += parsed_data.pop(0) + '<tr>' # blank row, but I'll add it in, why not
    header += parsed_data.pop(0) + '<tr>' # AVERAGE Row
    header += parsed_data.pop(0) + '<tr>' # STDDEV Row
    header += parsed_data.pop(0) + '<tr>' # PERFECT Row
    
    closing = '''</table>
<p>* = 1 late day used</p>
<p>&nbsp;<p>
'''
    
    parsed_data[-1] = parsed_data[-1].replace(closing, "") # remove closing HTML from last students code block
    rainbow_grades = dict()
  
    # each entry is a code block for each student
    for entry in parsed_data:
        # extract student ID from code block
        student_id = entry.split("</font></td>")[3].split("<font size=-1>")[1]
        rainbow_grades[student_id] = entry

    file.close()
    return (header, closing, rainbow_grades)
    

# Reconstruct a rainbowgrades report to be grouped by lab number and sorted by name
def reconstruct_rainbowgrades(students_filename, rainbow_grades_filename):
	sections = read_student_sections(students_filename)
	
	# Get sorted list of sections
	section_list = list(sections.keys())
	for i in range(len(section_list)):
		section_list[i] = int(section_list[i])
	section_list.sort()

	(header, closing, rainbow_grades) = read_rainbowgrades(rainbow_grades_filename)

	### Construct Output File ###
	file = open("parsed_" + rainbow_grades_filename, 'w')

	# Write Header Block
	file.write(header)

	# Write Student Records
	for key in section_list:
		for student in sections[str(key)]:
			file.write("<tr>\n" + rainbow_grades[student] + '\n</tr>')

	# Write Closing Block
	file.write(closing)
	
	# Close the output file
	file.close()
	
      
if __name__ == "__main__":
	reconstruct_rainbowgrades("students.txt", "output.html")
