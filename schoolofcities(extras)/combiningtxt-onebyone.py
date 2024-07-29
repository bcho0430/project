import os

# List of input text files
input_files = ['part_1.txt', 'part_2.txt', 'part_3.txt', 'part_4.txt',
               'part_5.txt', 'part_6.txt', 'part_7.txt', 'part_8.txt',
               'part_9.txt', 'part_10.txt', 'part_11.txt', 'part_12.txt']  # Add your file names here

# Accessible_parking_bylaw.txt', 'Application_for_Zoning_By-law_Amendment.txt', 'CRoZBy_Signed_By-law.txt', 
#                'DSD_BUILD_DC_Bylaw.txt', 'DSD_PLAN_NPR_ZBL_section_4.txt', 'DSD_PLAN_NPR_Zoning_Typologies_Sec_Plans.txt',
#                'DSD_PLAN_Park_Dedication_By-Law_2022-101.txt', 'Park_Dedication_By-Law_2008-93.txt', 
#                'Site_Alteration_bylaw.txt', 'Termite_Prevention_And_Control.txt', 'TRANSPORT_Traffic_And_Parking_Bylaw.txt',
#                'TRANSPORT_Traffic_And_Parking_Bylaw.txt

# Name of the output file
output_file = 'combined.txt'

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    for fname in input_files:
        # Open each input file in read mode
        with open(fname, 'r') as infile:
            # Read the contents of the input file and write them to the output file
            contents = infile.read()
            outfile.write(contents)
            outfile.write("\n")  # Optional: Add a newline between files
print(f"All files have been combined into {output_file}")
