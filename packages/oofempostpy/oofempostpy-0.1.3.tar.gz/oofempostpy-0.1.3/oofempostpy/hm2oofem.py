# transform inp file to in file for OOFEM
def hm2oofem(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        # Write the headers for the OOFEM output file
        outfile.write("######################N O D E########################\n")
        
        nodes_section = False
        elements_section = False
        ignore_lines = False
        elements_started = False
        
        for line in infile:
            line = line.strip()
            
            # Ignore lines starting with "**HW_COMPONENT"
            if line.startswith("**HW_COMPONENT"):
                continue
            
            # Ignore lines starting with "**HW_SET" and everything after
            if line.startswith("**HW_SET"):
                ignore_lines = True
            
            if ignore_lines:
                continue
            
            # Detect the nodes section
            if line.startswith("*NODE"):
                nodes_section = True
                elements_section = False
                continue
            
            # Detect the elements section
            elif line.startswith("*ELEMENT"):
                if not elements_started:
                    # Write the element section header
                    outfile.write("######################ELEMENT########################\n")
                    elements_started = True
                elements_section = True
                nodes_section = False
                continue
            
            # Process nodes section
            if nodes_section and line:
                parts = line.split(',')
                node_id = parts[0].strip()
                x_coord = parts[1].strip()
                y_coord = parts[2].strip()
                outfile.write(f"node  {node_id}  coords  2   {x_coord}  {y_coord}\n")
            
            # Process elements section
            elif elements_section and line and not line.startswith("**"):
                parts = line.split(',')
                element_id = parts[0].strip()
                node_ids = '    '.join(part.strip() for part in parts[1:])
                outfile.write(f"Quad1PlaneStrain  {element_id}  nodes  4    {node_ids}  mat  1  crossSect  1\n")


# # Input and output file names
# input_filename = "test.inp"
# output_filename = "test.in"

# # Call the function to translate the file
# hm2oofem(input_filename, output_filename)
