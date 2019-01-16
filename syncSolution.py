import requests
import csv, os, re, ast, time

# open csv file 
input = open('tactic.csv')
inputReader = csv.reader(input)

# helper function to clean URL before status code check
def cleanPixel(testUrl):
    # replace forward and back slash with single forward slash
    badSlash = re.compile(r'(\\\/)')
    goodSlash = badSlash.sub('/', testUrl)
    # replace escape character patterns on quotation marks
    badEscape = re.compile(r'\\\"')
    goodEscape = badEscape.sub('', goodSlash)
    # remove double quote marks
    badQuote = re.compile(r'(\"\")')
    goodQuote = badQuote.sub('', goodEscape)
    # remove whitespace
    badSpace = re.compile(r'\s')
    goodSpace = badSpace.sub('', goodQuote)
    # remove edge case bracket single quote error 
    badStart = re.compile(r'^(\[\D)')
    goodStart = badStart.sub('["', goodSpace)

    return goodStart

# create csv to write pixels with bad tactics
def badPixel(badResponse):
    with open('badPixels.csv', 'a', newline='') as f: 
        theWriter = csv.writer(f)
        theWriter.writerow(['id','tactic_id','creative_library_id','creative_asset_id','active','deleted','click_tracker_url','click_tracker_encoding_level','impression_pixel_json','js_pixel_json','clickthrough_pixel_json','viewability_pixel_json','last_modified'])
        for sublist in badResponse:
            theWriter.writerow(sublist)     

# Primary function to loop through each url and syncronously get the status code  
def findPixel(inputReader):
    print('Impression pixel analysis initiated...')
    badResponse = []
    badResponseCount = 0
    rowCount = 0
    for row in inputReader:
        rowCount+=1 
        impPixel = row[8] # impression_pixel_json column 
        statusCodes = []
        if rowCount % 10 == True:
            print(rowCount-1, 'pixels analyzed...')
        if inputReader.line_num == 1:
            continue 
        elif impPixel == '[]':
            continue
        elif impPixel == 'NULL':
            continue
        pixelList = ast.literal_eval(cleanPixel(impPixel))
        for url in pixelList: # syncronously loop through each url to get status code
            try:
                response = requests.head(url, timeout=0.5)
                statusCodes.append(response.status_code)
            except: 
                statusCodes.append(404)
        for code in statusCodes: # detect failures 
            if code >= 400:
                badResponseCount+=1
                badResponse.append(row)
    badPixel(badResponse)
    print('Pixel analysis complete. ',badResponseCount,' bad pixels found,', rowCount,' total pixels analyzed')

findPixel(inputReader)











