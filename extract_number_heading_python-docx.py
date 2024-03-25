# %pip install python-docx
from docx import Document

def add_sections(doc_path: str):
    '''
    Input: path of a docx file 
    Output: a list of heading names and their number headings corresponding chapters, sections, subsections,... 
    '''
    doc = Document(doc_path)
    # Extract chapters, section, subsection numbers
    heading_numbers=[]
    heading_name=[]

    for paragraph in doc.paragraphs:
        # Check if the paragraph is a heading
        if paragraph.style.name.startswith('Heading'):            # Heading for all chapters, sections, subsections,.., Heading 1 for chapter, Heading 2 for subsections, Heading 3 for subsubsections
            # Save heading numbers and heading names      
            heading_numbers.append(paragraph.style.name.split()[1])
            heading_name.append((paragraph.text))
    #print(heading_numbers)
    
    # Map heading_numbers to heading sections
    heading_sections_result = []
    chapter = 1
    for i in range(len(heading_numbers)):
        if heading_numbers[i] =='1':
            heading_sections_result.append(str(chapter))
            chapter+=1
        else:
            if int(heading_numbers[i]) > int(heading_numbers[i-1]):

                if int(heading_numbers[i]) == 2:
                    heading_sections_result.append(heading_sections_result[-1]+'.1')
                else:
                    heading_sections_result.append(heading_sections_result[-1] + '.1'*(int(heading_numbers[i])-2))


            elif int(heading_numbers[i]) == int(heading_numbers[i-1]):
                u = heading_sections_result[-1].split('.')
                u[-1] = str(int(u[-1])+1)
                heading_sections_result.append('.'.join(u))
       
            elif int(heading_numbers[i]) < int(heading_numbers[i-1]):
                u = heading_sections_result[-1].split('.')
                u = u[:int(heading_numbers[i])]
                u[-1] = str(int(u[-1])+1)
                heading_sections_result.append('.'.join(u))
    
    # Combine heading_name and heading_sections_result 
    total_heading = []
    for i in range(len(heading_numbers)):
        total_heading.append(heading_sections_result[i] + ' ' + heading_name[i])


    return total_heading