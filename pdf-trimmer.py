#INSTRUCTIONS
"""
Info:
- this cuts out the repeating slides in the lecture notes / lecture slides pdfs (they have a new page for each fade in) 
- it does this by keeping the page with the last slide for each slide: if the last slide doesn't contain all the information from the 
  previous pages this will erase information. I'm pretty sure that wont happen though...

- manipulates pdf using the PyPDF2 library from pypi (you have to download it, see below)
- ive commented the code in case you want to try to understand it (the core of it is under #FIND PAGES TO KEEP). its not that hard to understand

Installation: 
1. in the terminal, run: "pip3 install PyPDF2"
2. Put this file in a place you'll remember, maybe its own folder

Usage:
1. Download the pdf into the same folder as this file
2. Navigate to that folder in the terminal (windows command line or bash)
    a. type "cd" then the folder path (you could get it from clicking the nav bar on windows file explorer and copying) 
3. Run one of the two commands depending on OS (I think):
- python pdf-trimmer filename.pdf
- python3 pdf-trimmer filename.pdf 
    
    a. use the tab key to autocomplete the file names once you started typing it
    b. you can also just run 'python pdf-trimmer' and it will ask you for the file name
    c. you could also run 'python filename.pdf outputfilename.pdf'
    idk why I did it that way maybe it overcomplicates it

"""




#GET FILE NAMES
import sys
#try reading the input file name from the arguments given to python, otherwise ask the user
try: 
    input_file_name = sys.argv[1]
except: #(if the above failed)
    input_file_name = input("enter pdf name: ")
    #no input validation: if you put in something nonsensical there will probably be an error

#try reading the output file name from the arguments given to python, otherwise come up with a file name
try:
    output_file_name = sys.argv[2]
except:
    input_name_no_extension = input_file_name.rsplit(".", 1)[0]
    output_file_name = f"TRIMMED__{input_name_no_extension}.pdf"
# we are left with input_file_name and output_file_name



#OPEN THE INPUT FILE
from PyPDF2 import PdfFileReader
input_pdf = PdfFileReader(input_file_name) #store pdf object in input_pdf variable



#FIND PAGES TO KEEP
pages_to_keep = []   #an empty list
#each page has a real slide number at the bottom of the page, we want to keep the last page for each slide number (the page where everything has faded in)

#warning: if any slide has parts that fade in and obscure previous parts of the slide, this program will currently not show the obscured slide! hopefully thats not a big issue


num_pages = input_pdf.getNumPages()

for i in range(num_pages - 1):  # (we are skipping the last page)
    this_page_text = input_pdf.getPage(i).extractText()  #get the text from the (i)th page of the pdf
    this_page_slide_num = this_page_text.split("\n")[-1].split("/")[0][-2]   #get the slide number from within the page (its always in the same position). x.blanks are processed left to right, 
    
    next_page_text = input_pdf.getPage(i + 1).extractText()
    next_page_slide_num = next_page_text.split("\n")[-1].split("/")[0][-2]  #basically we are finding the last '/' and getting the number to the left of it
    
    if this_page_slide_num == next_page_slide_num:
        pass #if the next slide num is the same as this page num, do nothing
    else:  
        #if the next page num is different, then this is the last page
        pages_to_keep.append(i)  #add this page number to the keep list

pages_to_keep.append(num_pages - 1) #add the last page number to the pages to keep, since we skipped it before and we always want to keep it. since we start counting at 0 we have to subtract 1

#now we are left with a pages_to_keep list. If this were a function we would return that

print("keeping pages: " + str(pages_to_keep))



#WRITE OUTPUT FILE
#get pdf writer
from PyPDF2 import PdfWriter
output_pdf = PdfWriter()

#add pdf pages to the writer
for page_num in pages_to_keep: #one loop for each item in pages_to_keep (items are page numbers)
    page = input_pdf.pages[page_num]  #get page from input
    output_pdf.add_page(page)  #add it to output

#write the pdf data in output_pdf to the output file on system (will create if doesn't exist)
with open(output_file_name, 'wb') as output_file:
    output_pdf.write(output_file) #write the output pdf object into a real pdf

print("successfully wrote modified pdf to file named " + output_file_name)

#I learned how to use the PyPDF library by following instructions found through google on how to do each part