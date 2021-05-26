
def generate_zips(zip):
    num_plus = zip
    num_minus = zip
    while num_plus <= (zip + 50):
        yield num_plus
        num_plus += 10
    while num_minus >= (zip - 50):
        yield num_minus
        num_minus -= 10  

def get_zips(zip):
    all_zips = []
    for value in generate_zips(zip):
        all_zips.append(value)
    return all_zips



