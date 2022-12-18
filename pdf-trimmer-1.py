"""
Instructions:
In command line:
- pip install PyPDF2
- put the python file and downloaded pdf in same folder, open that folder in command line, and enter on the command line:
  python pdf-trimmer.py example.pdf

- navigate to that folder on windows command line is "cd FolderName" (change directory)
- (may need to put python3 or pip3 on mac/linux idk)
- you can use tab key to autocomplete file name once you started it




I tried to annotate whats going on for beginners reading this but 
I didn't put that much thought into the annotations / good language,

I made this code fairly quickly so it probably could be simpler/better but either way it works :)

"""




from PyPDF2 import PdfFileReader, PdfWriter, PageObject

#define a custom function that finds the page number of a page based on the entire text of that page as input
def get_page_num(page_text:str):  
    last_line = page_text.split("\n")[-1]  #get the last line by converting the string to a list of lines (split("\n")) and getting the last line (pop())
    page_num = last_line.split("/")[0].strip()[-1] #find the page num in last line essentially (based on format of document)
    return int(page_num)  #this is the output of our custom function

#define a custom function that tells us if 2 pages overlap (aka they are the same slide)
def page_overlaps(first_page:PageObject, last_page:PageObject):
    text_1 = first_page.extractText()
    page_num_1 = get_page_num(text_1)

    text_2 = last_page.extractText()
    page_num_2 = get_page_num(text_2)


    return page_num_1 == page_num_2  #if the page numbers are the same then the page overlaps
    

def find_pages_to_keep(pdf:PdfFileReader):
    num_pages = pdf.getNumPages()    #pdf is a custom object from the PyPDF library

    pages_to_keep = [0]   #a list with just the element 0 in it 

    last_page = pdf.getPage(0)   #first page to start, aka the page before the one we are looking at each time in the loop
    for i in range(1, num_pages):   #go through 2nd-last pages
        page = pdf.getPage(i)    #get page object

        if page_overlaps(last_page, page):
            #if the page is the same as the last then we get rid of the last page and keep the latest page instead
            x = pages_to_keep.pop()   #get rid    #variable is not necessary just for optional print below
            #print(f"removing page {x}")
            pages_to_keep.append(i)   #add the index to the list of pages to keep
        else:
            #if the page is new we decide to keep it
            pages_to_keep.append(i)

        last_page = page  #update the last page for next cycle of the loop

    return pages_to_keep   #output our list



# start of program |V|


#GET FILE NAMES
import sys
#try reading the input file name from the arguments given to python, otherwise ask the user
try: 
    input_file_name = sys.argv[1]
except:
    input_file_name = input("enter pdf name: ")

#try reading the input file name from the arguments given to python, otherwise come up with a file name
try:
    output_file_name = sys.argv[2]
except:
    input_name_no_extension = input_file_name.rsplit(".", 1)[0]
    output_file_name = f"TRIMMED_{input_name_no_extension}.pdf"


#OPEN THE INPUT FILE
input_pdf = PdfFileReader(input_file_name) #open the input pdf

#FIND PAGES TO KEEP
pages_to_keep = find_pages_to_keep(input_pdf) #get list of page numbers to keep

print(f"keeping: {pages_to_keep}")


#WRITE OUTPUT FILE
output_pdf = PdfWriter()  #output pdf data

for i in pages_to_keep:
    page = input_pdf.pages[i]  #get page from input
    output_pdf.add_page(page)  #add it to output

#write the output pdf to the output file on system (will create if doesn't exist)
with open(output_file_name, 'wb') as f:
    output_pdf.write(f)


