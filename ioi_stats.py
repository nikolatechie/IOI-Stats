import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt

class IOIStats:
    def __init__(self):
        self.scrapeData()
        self.data = pd.read_csv("C:/Users/Nikola/Desktop/Python/IOI Stats/data.csv") # load stats
        self.year = self.data.year
        self.minBronze = self.data.minBronze
        self.minSilver = self.data.minSilver
        self.minGold = self.data.minGold
        self.maxPoints = self.data.maxPoints
        self.convertToPercentage()

    def scrapeData(self): # scrape data and put it into data.csv file
        urlMain = "http://stats.ioinformatics.org/olympiads/" # main part

        try:
            print("Scraping data from the IOI website...")
            f = open("C:/Users/Nikola/Desktop/Python/IOI Stats/data.csv", 'w')
            f.write("year,minBronze,minSilver,minGold,maxPoints\n")

            for year in range(1989, 2020):
                print(year)
                url = urlMain + str(year)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                listItems = soup.select("div.maincontent ul li")
                minBronze = minSilver = minGold = maxPoints = 0

                # go through all list items and search for needed keywords
                for item in listItems:
                    item = str(item)
                    lineSplit = item.split(" ")
                    firstWord = lineSplit[0][4:]
                    
                    if firstWord == "Maximum":
                        maxPoints = float(lineSplit[len(lineSplit)-1][:3])
                    elif firstWord == "Gold":
                        minGold = float(lineSplit[4])
                    elif firstWord == "Silver":
                        minSilver = float(lineSplit[4])
                    elif firstWord == "Bronze":
                        minBronze = float(lineSplit[4])
                
                f.write(str(year) + ',' + str(minBronze) + ',' + str(minSilver) + ',' + str(minGold) + ',' + str(maxPoints))
                if (year < 2019): f.write('\n')
        except:
            print("Error!")
        finally:
            f.close()

    def convertToPercentage(self): # use percentage instead of points
        for i in range(len(self.year)):
            self.minBronze[i] = self.minBronze[i] / self.maxPoints[i] * 100
            self.minSilver[i] = self.minSilver[i] / self.maxPoints[i] * 100
            self.minGold[i] = self.minGold[i] / self.maxPoints[i] * 100

    def showData(self):
        plt.style.use("dark_background")
        plt.title("IOI Statistics")
        plt.xlabel("Year")
        plt.ylabel("Percentage")
        plt.plot(self.year, self.minGold, label = "Gold medal", color = "gold")
        plt.plot(self.year, self.minSilver, label = "Silver medal", color = "silver")
        plt.plot(self.year, self.minBronze, label = "Bronze medal", color = "#cd7f32")
        plt.legend()
        plt.show()


stats = IOIStats()
stats.showData()