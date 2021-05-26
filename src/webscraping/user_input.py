import pandas as pd
from sklearn import preprocessing




def make_df_from_input():
    welcome = "------Hej og velkommen til den smarteste house-price-predictor------"
    print(welcome)
    house_type= input("---Vælg boligtype---\nTryk 0 for ejerlejlighed \nTryk 1 for rækkehus \nTryk 2 for villa \nTryk 3 for villalejlighed ")
    house_zip_code= int(input("Indtast dit postnr: "))
    house_rooms= int(input("Indtast antal værelser: "))
    house_square_meters= int(input("Indtast kvm: "))
    house_year= int(input("Indtast opførelsesår: "))
    house_year = 2021-int(house_year)
    house_taxes= int(input("Indtast ejerafgift: "))
    house_energy= int(input("---Vælg energimærke---\nTryk 1 for mærke A1\nTryk 2 for mærke F\nTryk 3 for mærke G\nTryk 4 for mærke A10\nTryk 5 for mærke A15\nTryk 6 for mærke A2\nTryk 7 for mærke A20\nTryk 8 for mærke B\nTryk 9 for mærke C\nTryk 10 for mærke D\nTryk 11 for mærke E\n "))
    house_ground_area= int(input("Indtast grundstørrelse: "))

    data = [[house_type, house_zip_code, house_rooms, house_square_meters, house_year, house_taxes, house_energy, house_ground_area]]
    df = pd.DataFrame (data, columns = ["house_type", "house_zip_code", "house_rooms", "house_square_meters", "house_year", "house_taxes", "house_energy", "house_ground_area"])
    return df