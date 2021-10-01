import requests
from bs4 import BeautifulSoup

## get the raw data from the provide remote source
def getRawSalaryInfo():

    try:
        response = requests.get("https://questionnaire-148920.appspot.com/swe/data.html")
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all("td", class_="player-salary")
    except:
        print("Error: Issue retrieving remote salary data. Check your internet connection!")
        exit(1)

## clean the raw data and calculate the qualifying offer
def calcQualifyingOffer(rawSalaryData):

    if len(rawSalaryData) < 125:
        print("Error: Not enough salary information was found.")
        exit(1)
    try:
        cleanedSalaries = list()
        for row in rawSalaryData:
            ## check for nullness, emptyness, or any letters
            if row.text is None or len(row.text) == 0 or any(char.isalpha() for char in row.text):
                continue
            # remove all dollar signs and commas
            cleanedSalaries.append(int(row.text.replace("$", "").replace(",", "")))
        cleanedSalaries.sort(reverse=True)
        return round(sum(cleanedSalaries[:125]) / 125, 2)
    except:
        print("Error: Issue calculating qualifying offer")
        exit(1)


def main():

    rawSalaryData = getRawSalaryInfo()
    qualifyingOffer = calcQualifyingOffer(rawSalaryData)
    formattedOffer = "${:,.2f}".format(qualifyingOffer)
    print(f'Qualifying Offer: {formattedOffer}')

if __name__ == '__main__':
    main()