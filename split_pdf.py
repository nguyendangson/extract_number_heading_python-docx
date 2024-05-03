#from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import os
import tqdm
from tqdm import tqdm

import re
import tiktoken
import pandas as pd
# os.getcwd()

#Check tokens
def number_tokens(input_folder_path):
    '''
    input_pdf_path is a folder path
    Check number of tokens of all files in the folder
    '''
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    table ={}
    for name_pdf in os.listdir(input_folder_path):
        
        input_path_path = input_folder_path + '\\' + name_pdf
        pdf_reader = PdfReader(input_path_path)
        text = ''
        number_of_pages = len(pdf_reader.pages)
        for i in tqdm(range(number_of_pages)):
            text+= pdf_reader.pages[i].extract_text()
        
        table[name_pdf] = len(encoding.encode(text))
        df = pd.DataFrame(data=table, index= [0])
    return df.to_csv(input_folder_path + '\\' +'TokenCounts.csv')

# Split pdfs
def split_pdf_by_bookmarks(input_pdf_path, page_ranges):

    pdf_reader = PdfReader(input_pdf_path)
    input_path = input_pdf_path.split('\\')
    name_pdf = input_path[-1].split('.')[-0]
    output_folder = '\\'.join(input_path[:-1]) + '\\' + name_pdf
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for index, (start, end, name) in enumerate(page_ranges, start=1):
        writer = PdfWriter()
        for page_num in range(start-1, end):
            writer.add_page(pdf_reader.pages[page_num])

        output_filename = f"{output_folder}\[{name_pdf}]{name}.pdf"

        with open(output_filename, 'wb') as output_file:
            writer.write(output_file)
            output_file.close()

    pdf_reader.stream.close()
    number_tokens(output_folder)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_975_4 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-975-4_btms.pdf'  # Path to your input PDF
page_ranges_CBR_975_4 = [[1,7, 'Volvo, Nova Bus, and Mack Battery Thermal Management System (BTMS) User Manual'],[8,15, 'Chapter 1 Unit Installation'], [16,17 , 'Chapter 2 Applying and Removing Power'], 
                         [18,25 , 'Chapter 3 Inspection and Maintenance part 1'], [26,33 , 'Chapter 3 Inspection and Maintenance part 2'], [34,41 , 'Chapter 3 Inspection and Maintenance part 3'],
                         [42, 43, 'Appendix A Product Specifications'], [44, 45, 'Appendix B Product Specifications Reference and Support'], [46, 49, 'EVantage Battery Thermal Management System (BTMS) Troubleshooting Manual'], 
                         [50, 57, 'Chapter 1 BTMS Fault List'], [58, 74, 'Chapter 2 Flow Charts']]
split_pdf_by_bookmarks(input_pdf_path_CBR_975_4, page_ranges_CBR_975_4)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_2273_6_Tp_250d_1 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-2273-6_Tp_250d 1.pdf'
page_ranges_CBR_2273_6_Tp_250d_1 = [[1, 4, 'Section 1 Introduction, Section 2 Product Description'], 
                                    [5, 9, 'Section 3 Important Safety Notice'], 
                                    [10, 11, 'Section 4 Parts Lists part 1'], [12, 16, 'Section 4 Parts Lists part 2'],
                                    [17,17, 'Section 5 Special Tools'], [18,21, 'Section 6 Towing Procedures'], 
                                    [22, 26, 'Section 7 Preventive Maintenance part 1'], [27, 31, 'Section 7 Preventive Maintenance part 2'], [32, 34, 'Section 7 Preventive Maintenance part 3'], 
                                    [35, 40, 'Section 8 Alignment & Adjustments part 1'], [41, 44, 'Section 8 Alignment & Adjustments part 2'], [45, 48, 'Section 8 Alignment & Adjustments part 3'],
                                    [49, 55, 'Section 9 Component Replacement, part 1'], [56, 60, 'Section 9 Component Replacement, part 2'], [61, 66, 'Section 9 Component Replacement, part 3'], [67, 74, 'Section 9 Component Replacement, part 4'], [75, 80, 'Section 9 Component Replacement, part 5'], [81, 85, 'Section 9 Component Replacement, part 6' ], [86,90, 'Section 9 Component Replacement, part 7'], 
                                    [91,91, 'Section 10 Plumbing Diagrams'], [92, 93, 'Section 11 Troubleshooting Guide'], [94,97, 'Section 12 Torque Specifi cations'],
                                    [98,98, 'Section 13 Front Wheel Alignment Specifi cations'], [99, 100, 'Section 14 Reference Material']
                                    ]
split_pdf_by_bookmarks(input_pdf_path_CBR_2273_6_Tp_250d_1, page_ranges_CBR_2273_6_Tp_250d_1)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_4185_air_systems_schematic = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-418-5_air-systems-schematic-10-4-2016-1-pv776-89096970-1.pdf'
page_ranges_CBR_4185_air_systems_schematic = [[1, 10, 'Section 1 General and Tools'] , 
                                              [11, 18, 'Section 2 Specifications and Design and Function part 1'], 
                                              [19, 21, 'Section 2 Specifications and Design and Function part 2'], 
                                              [22, 37, 'Section 2 Specifications and Design and Function part 3'], 
                                              [38, 59, 'Section 2 Specifications and Design and Function part 4']]
split_pdf_by_bookmarks(input_pdf_path_CBR_4185_air_systems_schematic, page_ranges_CBR_4185_air_systems_schematic)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
# CBR_2274_5 and CBR CBR_2273_6_Tp_250d_1 are same?
input_pdf_path_CBR_2274_5 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-2274-5_Tp_247g.pdf'
page_ranges_CBR_2274_5 = [[1, 4, 'Section 1 Introduction, Section 2 Product Description'], 
                                    [5, 9, 'Section 3 Important Safety Notice'], 
                                    [10, 11, 'Section 4 Parts Lists part 1'], [12, 16, 'Section 4 Parts Lists part 2'],
                                    [17,17, 'Section 5 Special Tools'], [18,21, 'Section 6 Towing Procedures'], 
                                    [22, 26, 'Section 7 Preventive Maintenance part 1'], [27, 31, 'Section 7 Preventive Maintenance part 2'], [32, 34, 'Section 7 Preventive Maintenance part 3'], 
                                    [35, 40, 'Section 8 Alignment & Adjustments part 1'], [41, 44, 'Section 8 Alignment & Adjustments part 2'], [45, 48, 'Section 8 Alignment & Adjustments part 3'],
                                    [49, 55, 'Section 9 Component Replacement, part 1'], [56, 60, 'Section 9 Component Replacement, part 2'], [61, 66, 'Section 9 Component Replacement, part 3'], [67, 74, 'Section 9 Component Replacement, part 4'], [75, 80, 'Section 9 Component Replacement, part 5'], [81, 85, 'Section 9 Component Replacement, part 6' ], [86,90, 'Section 9 Component Replacement, part 7'], 
                                    [91,91, 'Section 10 Plumbing Diagrams'], [92, 93, 'Section 11 Troubleshooting Guide'], [94,97, 'Section 12 Torque Specifi cations'],
                                    [98,98, 'Section 13 Front Wheel Alignment Specifi cations'], [99, 100, 'Section 14 Reference Material']
                                    ]
split_pdf_by_bookmarks(input_pdf_path_CBR_2274_5, page_ranges_CBR_2274_5)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_2274_5_17730_254e = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-2274-5_17730-254e.pdf'
page_ranges_CBR_2274_5_17730_254e= [[1, 3, 'Section 1 and Section 2 Introduction and Section 2'] , 
                                              [4, 7, 'Section 3 Important Safety Notice'], 
                                              [8, 9, 'Section 4 Special Tools'], 
                                              [10, 14, 'Section 5 Parts Lists'], 
                                              [15, 22, 'Section 6 Preventive Maintenance'], 
                                              [23, 27, 'Section 7 Alignment & Adjustments'],
                                              [28, 31, 'Section 8 Component Replacement part 1'], [32, 35, 'Section 8 Component Replacement part 2'], [36, 42, 'Section 8 Component Replacement part 3'], [43, 47, 'Section 8 Component Replacement party 4'], [48, 51, 'Section 8 Component Replacement party 5'],
                                              [52, 55, 'Section 9 Torque Specifications'],
                                              [56, 60, 'Section 9 Torque Specifications']
                                              ]
split_pdf_by_bookmarks(input_pdf_path_CBR_2274_5_17730_254e, page_ranges_CBR_2274_5_17730_254e)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
# CBR-2273-6_17730-279c and CBR-2274-5_17730-254e are same?
input_pdf_path_CBR_2273_6_17730_279c = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-2273-6_17730-279c.pdf'
page_ranges_CBR_2273_6_17730_279c= [[1, 3, 'Section 1 and Section 2 Introduction and Section 2'] , 
                                              [4, 7, 'Section 3 Important Safety Notice'], 
                                              [8, 9, 'Section 4 Special Tools'], 
                                              [10, 14, 'Section 5 Parts Lists'], 
                                              [15, 22, 'Section 6 Preventive Maintenance'], 
                                              [23, 27, 'Section 7 Alignment & Adjustments'],
                                              [28, 31, 'Section 8 Component Replacement part 1'], [32, 35, 'Section 8 Component Replacement part 2'], [36, 42, 'Section 8 Component Replacement part 3'], [43, 47, 'Section 8 Component Replacement party 4'], [48, 51, 'Section 8 Component Replacement party 5'],
                                              [52, 55, 'Section 9 Torque Specifications'],
                                              [56, 60, 'Section 9 Torque Specifications']
                                              ]
split_pdf_by_bookmarks(input_pdf_path_CBR_2273_6_17730_279c, page_ranges_CBR_2273_6_17730_279c)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_511_5_wingman = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-511-5_wingman.pdf'
page_ranges_CBR_511_5_wingman= [[1, 5, 'The Bendix Wingman Fusion Driver Assistance System'] , 
                                [6,11, 'Section 1 Troubleshooting Section'], 
                                [12, 14, 'Section 2 Troubleshooting and Diagnostics Section part 1'], 
                                [15, 20, 'Section 2 Troubleshooting and Diagnostics Section part 2 Table 4A'],
                                [21, 26, 'Section 2 Troubleshooting and Diagnostics Section part 2 Table 4B'],
                                [27, 28, 'Section 2 Troubleshooting and Diagnostics Section part 3'],
                                [29, 32, 'Section 3 System Features Section'], 
                                [33, 22, 'Appendices'], 
                                ]
split_pdf_by_bookmarks(input_pdf_path_CBR_511_5_wingman, page_ranges_CBR_511_5_wingman)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_2334_1 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-2334-1_bendix-air-disc-brakes.pdf'
page_ranges_CBR_2334_1= [[1, 5, 'Section 1'] , 
                        [6,8, 'Section 2'], 
                        [9, 9, 'Section 3'], 
                        [10, 15, 'Section 4'],
                        [16, 18, 'Section 5 part 1 Maintenance Kits'], [19, 19, 'Section 5 part 2 Air Disc Brake Shield Kit'], [20, 21, 'Section 5 part 3 Pad Replacement'], 
                        [22, 23, 'Section 5 pat 4 Caliper, Carrier, Actuator Assembly'], [24, 24, 'Section 5 part 5 Spring, Service Brake'], 
                        [25, 28, 'Section 5 part 6 Tappet, Boot, and Tappet Inner Seal'],
                        [29, 34, 'Section 5 part 7 Guide Pin and Boot Assemblies'],
                        [35, 40, 'Section 5 part 8 Bendix Splined Disc Hub Rotor'],
                        ]
split_pdf_by_bookmarks(input_pdf_path_CBR_2334_1, page_ranges_CBR_2334_1)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_948_4 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-948-4_mack-ecs-mid150-fault-codes-pv776-89127445-1-pdf6-16-2016.pdf'
page_ranges_CBR_948_4= [[1, 6, 'Section 1 General'] , 
                        [7,8, 'Section 2 Specifications'], 
                        [9, 9, 'Section 3 Tools'], 
                        [10, 18, 'Section 4 System check part 1'], [19, 30, 'Section 4 System check part 2'], [31, 40, 'Section 4 System check part 3'] , [41, 51, 'Section 4 System check part 4']
                        ]
split_pdf_by_bookmarks(input_pdf_path_CBR_948_4, page_ranges_CBR_948_4)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_249_6 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-249-6_blindspottersdsheet-pdf-3-8-2016.pdf'
page_ranges_CBR_249_6= [[1, 7, 'Section 1 Operation Section'] , 
                        [8,8, 'Section 2 Maintenance Section'], 
                        [9, 20, 'Section 3 Troubleshooting Section'], 
                        ]
split_pdf_by_bookmarks(input_pdf_path_CBR_249_6, page_ranges_CBR_249_6)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_511_5 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-511-5_sdp.pdf'
page_ranges_CBR_511_5= [[1, 4, 'Section 1 Operation Section'] , 
                        [5,12, 'Section 2 Maintenance Section'], 
                        ]
split_pdf_by_bookmarks(input_pdf_path_CBR_511_5, page_ranges_CBR_511_5)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_511_5 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-511-5_sdp.pdf'
page_ranges_CBR_511_5= [[1, 4, 'Section 1 Operation Section'] , 
                        [5,12, 'Section 2 Maintenance Section'], 
                        ]
split_pdf_by_bookmarks(input_pdf_path_CBR_511_5, page_ranges_CBR_511_5)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_2316_1 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-2316-1_kc-2316.pdf'
page_ranges_CBR_2316_1= [[1, 7, 'Section 1 GENERAL INFORMATION'] , 
                        [8,9, 'Section 2 BASIC SAFETY INFORMATION'], 
                        [10,10, 'Section 3 TECHNICAL DESCRIPTION'], 
                        [11,17, 'Section 4 INSTALLATION AND REMOVAL'], 
                        [18,25, 'Section 5 MAINTENANCE'], 
                        [26,28, 'Section 6 TROUBLESHOOTING'], 
                        [29,32, 'Section 7 DISPOSAL'], 
                        ]
split_pdf_by_bookmarks(input_pdf_path_CBR_2316_1, page_ranges_CBR_2316_1)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_511_5_ec_80 = 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-511-5_ec-80.pdf'
page_ranges_CBR_511_5_ec_80= [[1, 2, 'Section 1 Introduction'], 
                            [2,3, 'Section 2 Component and ECU Mounting'],
                            [4,4, 'Section 2 ABS Off-Road Switch and Indicator Lamp Operation and Bendix EC-80 Controller Outputs'], 
                            [5,6, 'Section 3 Indicator Lamp Behavior'], 
                            [6,7, 'Section 4 Power-Up Sequence'],
                            [7,7, 'Section 5 ABS Operation'], 
                            [8,9, 'Section 6 ATC Operation '], 
                            [9,10, 'Section 7 Dynamometer Test Mode'],
                            [10,10, 'Section 8 Automatic Tire Size Calibration'], 
                            [10,10, 'Section 9 ABS Partial Shutdown'], 
                            [11,12, 'Section 10 System Reconfiguration'], 
                            [13,13, 'Section 11 Blink Codes'], 
                            [14,15, 'Section 12 Diagnostic Modes'], 
                            [16,17, 'Section 13 Using hand-held or PC-based diagnostics'], 
                            [18,31, 'Section 14 Diagnostic Trouble Code Index'], 
                            [32, 38, 'Section 15 Troubleshooting Wiring'], 
                            [39,39, 'Section 16 Glossary'],
                            [40,44, 'Section 17 Appendix J1939 SPN and FMI Codes'], 
                        ]
split_pdf_by_bookmarks(input_pdf_path_CBR_511_5_ec_80, page_ranges_CBR_511_5_ec_80)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_511_5_flc20= 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-511-5_flc20.pdf'
page_ranges_CBR_511_5_flc20= [[1, 3, 'Section 1'], 
                            [4,10, 'Section 2 part 1'],
                            [11,14, 'Section 2 part 2'],
                            [15,17, 'Section 2 part 3'],
                            [18, 20, 'Section 3 part 1'],
                            [21, 28, 'Section 3 part 2'] 
                        ]
split_pdf_by_bookmarks(input_pdf_path_CBR_511_5_flc20, page_ranges_CBR_511_5_flc20)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
input_pdf_path_CBR_260_5= 'C:\\Users\\A485205\\Desktop\\Hackathon\\openai-hackathon\\input_pdf\\CBR-260-5_apcs-codes-pv776-20177177-pdf7-28-2016.pdf'
page_ranges_CBR_260_5= [[1, 18, 'MID 186 (APCS) Fault Codes Part 1'], 
                            [19,32, 'MID 186 (APCS) Fault Codes Part 2'],
                        ]
split_pdf_by_bookmarks(input_pdf_path_CBR_260_5, page_ranges_CBR_260_5)



# Extract sections in TABLE OF CONTENTS into a list
pdf_reader = PdfReader(input_pdf_path)
number_of_pages = len(pdf_reader.pages)
page_table_of_content = 0
text= pdf_reader.pages[page_table_of_content].extract_text()
text = text.split('. ')
print(text)

res = re.findall(r'. \d+', text)
res = [re.findall(r'\d+', x)[0] for x in res]
res = [int(i) for i in res if int(i) < number_of_pages+1]

res = list(set(res))
print(res)



# page_ranges_CBR_2273_6_Tp_250d_1 = []
# for i,x in enumerate(text):
#     if x=='TABLE OF CONTENTS':
#         #print(i)
#         text=text[i:]
#         print(text)
#         break

for i in range(1, len(text)-1):
    name_list = text[i].split('. ')
    name_sections = name_list[0]
    start = int(name_list[-1])

    next_name_list = text[i+1].split('. ')
    end = int(next_name_list[-1])

    

    page_ranges_CBR_2273_6_Tp_250d_1.append([start,end,name_sections])


name_last_section = text[-1].split('. ')
start_last_section = int(name_last_section[-1])
name_sections = name_last_section[0]
end_last_section = number_of_pages
page_ranges_CBR_2273_6_Tp_250d_1.append([start_last_section,end_last_section, name_last_section])
print(page_ranges_CBR_2273_6_Tp_250d_1)



        



