import pyttsx3
import PyPDF2


# Open the PDF
# book = open(r'dataset\1621598158503.pdf', 'rb')
book = open(r'dataset\Shankar Hadimani Contract June 2020.pdf','rb')

# Read pdf file
pdf_reader = PyPDF2.PdfFileReader(book)
pages = pdf_reader.numPages

print("number of pages: {}".format(pages))

# initnialise speaker
speaker = pyttsx3.init()

# select particular page
page = pdf_reader.getPage(1)

# extract the tetx fromt the above page
text = page.extractText()

print(text)

# read out the text from the page
speaker.say(text)

# wait until the audio finishes
speaker.runAndWait()



