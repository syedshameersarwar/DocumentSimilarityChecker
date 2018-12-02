from pdfReader import pdfToTxt #import for Simple PDF

from PIL import Image as PI    #imports for Scanned PDF
from wand.image import Image
import pyocr
import pyocr.builders
import io

import docx   #import for Word documents

import magic


from nltk.corpus import stopwords

import sys
import math




def pdfReader(filename): 

    try:
        pdfFileObject = open(filename,'rb')
        
    except IOError as e:
        print("Failed to open file, ",e)
        sys.exit(1)

    try:
        pdfText = pdfToTxt(pdfFileObject)
        
    except Exception as e:
        print(e)
        sys.exit(1)
    
    
    if '\x0c'*len(str(pdfText)) == str(pdfText):  #test for scanned pdf
        pdfText = getTextScannedPdf(filename)
    

    pdfFileObject.close()
    
    return pdfText


def getTextScannedPdf(filename):

    pyocr_tools = pyocr.get_available_tools()[0]
    language = pyocr_tools.get_available_languages()[0]  # 0 for english


    images_list = []


    pdf_images = Image(filename = filename,resolution = 500)
    pdf_jpegs = pdf_images.convert('jpeg')

    for image in pdf_jpegs.sequence:
        image_page = Image(image = image)
        images_list.append(image_page.make_blob('jpeg'))


    pages_txt = ''
    
    for image in images_list:
        pages_txt += pyocr_tools.image_to_string(PI.open(io.BytesIO(image)), \
                                        lang = language, \
                                        builder = \
                                        pyocr.builders.TextBuilder())

    return pages_txt

        
def docxReader(filename):

    try:
        document = docx.Document(filename)
        
    except IOError as e:
        print("Failed to open file, ",e)

    fullText = []

    for paragraph in document.paragraphs:
        fullText.append(paragraph.text)
    
    return fullText


def txtReader(filename):

    try:
        textFile = open(filename,'r')
        
    except IOError as e:
        print("Failed to open file, ",e)


    textFileLines = textFile.readlines()
    
    textFile.close()
    
    return textFileLines


def getNormalizeDocxText(listOfParagraphs):

    word_list = []
    paragraph_words_list = []
    character_list = []
    
    for paragraph in listOfParagraphs:
        if paragraph == '':
            continue
        
        for character in paragraph:

            if character.isalnum():
                character_list.append(character)     
            elif len(character_list)>0:
                word = "".join(character_list)
                word = word.lower()
                paragraph_words_list.append(word)
                character_list = []
                
        if len(character_list)>0:
            word = "".join(character_list)
            word = word.lower()
            paragraph_words_list.append(word)

    word_list.extend(paragraph_words_list)

    return word_list


def getNormalizeText(listOflines):

    wordlist = []
    character_list = []

    for line in listOflines:
        for character in line:

            if character.isalnum():
                character_list.append(character)
            elif len(character_list)>0:
                word = "".join(character_list)
                word = word.lower()
                wordlist.append(word)
                character_list = []

        if len(character_list)>0:
            word = "".join(character_list)
            word = word.lower()
            wordlist.append(word)

    return wordlist


def getNormalizeTextPdf(ExtractedPdfText):

    word_list = []
    character_list = []

    for character in ExtractedPdfText:

        if character.isalnum():
            character_list.append(character)
        elif len(character_list)>0:
            word = "".join(character_list)
            word = word.lower()
            word_list.append(word)
            character_list = []

    if len(character_list)>0:
        word = "".join(character_list)
        word = word.lower()
        word_list.append(word)

    return word_list


def getValidateWords(wordList):

    punctuations = ['(',')',';',':','[',']',',','.','-','_','&','|']
    stop_words = stopwords.words('english')

    validate_wordList = []

    for word in wordList:
        if (word not in punctuations) and (word not in stop_words):
            validate_wordList.append(word)

    return validate_wordList


def getPdfDataWrapper(filename):

    word_list = pdfReader(filename)
    
    normalized_wordlist = getNormalizeTextPdf(word_list)

    validated_wordlist = getValidateWords(normalized_wordlist)

    return validated_wordlist


def getDocxDataWrapper(filename):

    list_of_paragraphs = docxReader(filename)
    
    normalized_wordlist = getNormalizeDocxText(list_of_paragraphs)
    
    validated_wordlist = getValidateWords(normalized_wordlist)
    
    return validated_wordlist



def getTextDataWrapper(filename):

    list_of_lines = txtReader(filename)

    normalized_wordlist = getNormalizeText(list_of_lines)

    validated_wordlist = getValidateWords(normalized_wordlist)

    return validated_wordlist


def getDocumentType(filename):

    try:
        
        documentTypeString = magic.from_file(filename)

        if "PDF document" in documentTypeString:
            return "pdf"
        elif "Microsoft Word" in documentTypeString:
            return "docx"
        elif "ASCII text" in documentTypeString:
            return "txt"
        else:
            return None

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    

def SuitableDocReader(filename,docType):

    dic_documentFuncs = {"pdf":getPdfDataWrapper,"docx":getDocxDataWrapper, \
                         "txt":getTextDataWrapper}

    return dic_documentFuncs[docType](filename)



def count_frequency(wordlist):

    D = {}

    for word in wordlist:

        if word  in D:
            D[word]+= 1
        else:
            D[word] = 1

    return D


def inner_product(frequencyDict1,frequencyDict2):

    sum = 0.0

    for word in frequencyDict1:
        if word in frequencyDict2:
            sum += frequencyDict1[word]*frequencyDict2[word]

    return sum


def getVectorAngle(frequencyDict1,frequencyDict2):

    numerator = inner_product(frequencyDict1,frequencyDict2)

    denominator = math.sqrt(inner_product(frequencyDict1,frequencyDict1) * \
                            inner_product(frequencyDict2,frequencyDict2))

    return math.acos(numerator/denominator)


def DocumentDistance():

    document1 = input("\nEnter first file name : \n")

    document1_type = getDocumentType(document1)

    if document1_type != None:
        print("\n"+str(document1)+" is a valid '"+str(document1_type)+ \
                                                     "' document")
    elif document1_type =='empty':
        print("\n"+str(document1)+" is an empty document.")

        sys.exit(1)
    else:
        print("\n"+str(document1)+" is not a valid document.")
        sys.exit(1)
        
    print("\nSuitable document type for matching : '" + \
                                       str(document1_type)+"'")
    document2 = input("\nEnter second file name : \n")

    document2_type = getDocumentType(document2)

    if document2_type != None:
        print("\n"+str(document2)+" is a valid '"+str(document2_type) \
                                                        +"' document")
    elif document2_type =='empty':
        print("\n"+str(document2)+" is an empty document.")

        sys.exit(1)
    else:
        print("\n"+str(document2)+" is not a valid document.")

    
    document1_wordlist = SuitableDocReader(document1,document1_type)
    document2_wordlist = SuitableDocReader(document2,document2_type)


    document1_freq_mapping = count_frequency(document1_wordlist)
    document2_freq_mapping = count_frequency(document2_wordlist)

    
    document_distance = getVectorAngle(document1_freq_mapping, \
                                        document2_freq_mapping)

    return document_distance
    

def SimilarityCalculator():

    document_distance = DocumentDistance()

    similarity_percent = (1-(document_distance/1.57))*100

    return (document_distance,similarity_percent)


def SimilarityCalculatorInit():

    for i in range(26):
        print('*',end='')

    print('SIMILARITY CALCULATOR',end='')

    for i in range(26):
        print('*',end='')

    print("\n\nSupported Document Files : .txt,.pdf,.docx")

    print("\n\nNotes: 1) Same Document Type Files maps better output.")
    print("       2) Scanned Pdfs may take a while.")


def SimilarityCalcWrapper():

    SimilarityCalculatorInit()

    (DocumentDistance,SimilarityPercentage)= SimilarityCalculator()

    print("\nApproximate Document Distance(Max: 1.57) = %.2f"%DocumentDistance)
    print("Approximate Similarity Percent = %.2f"%SimilarityPercentage)


def main():
    
    SimilarityCalcWrapper()


if __name__ =='__main__':
    main()
    
