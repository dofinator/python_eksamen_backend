class FileWriteIterator:
    def __init__(self, recidense_list, file_path, labels):
        self.i = 0
        self.count = len(recidense_list)
        self.recidense_list = recidense_list
        self.file_path = file_path
        self.labels = labels
        file = open(self.file_path, "w")
        file.write(self.labels + "\n")
        file.close()
        
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.count:
            file = open(self.file_path, "a")
            r = self.recidense_list[self.i]
            csv_text = "{house_type};{house_zip_code};{house_rooms};{house_square_meters};{house_year};{house_taxes};{house_energy};{house_ground_area};{house_price};".format(
            house_type=r.house_type, house_price=r.house_price, house_rooms=r.house_rooms, house_square_meters=r.house_square_meters, house_year=r.house_year, house_zip_code=r.house_zip_code, house_taxes=r.house_taxes, house_energy=r.house_energy, house_ground_area=r.house_ground_area)
            file.write(csv_text + "\n")
            file.close()
            self.i += 1
        else:
            StopIteration()
        