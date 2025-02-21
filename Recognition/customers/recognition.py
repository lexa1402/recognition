from fastmrz import FastMRZ


def get_passport_data(passport_path):
    fast_MRZ = FastMRZ(tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    passport_mrz = fast_MRZ.get_details(passport_path, include_checkdigit=False)
    return passport_mrz
