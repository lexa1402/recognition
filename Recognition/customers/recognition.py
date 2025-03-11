from fastmrz import FastMRZ


def get_passport_data(data):
    fast_MRZ = FastMRZ(tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    passport_mrz = fast_MRZ.get_details(input_data=data, input_type='numpy', include_checkdigit=False)
    return passport_mrz


def get_text_data(text):
    fast_MRZ = FastMRZ(tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    return fast_MRZ.get_details(input_data=text, input_type='text')


def get_mrz(data):
    try:
        mrz_data = get_passport_data(data)
        if mrz_data['status'] == 'SUCCESS':
            return mrz_data['mrz_text']
    except Exception as e:
        print(e)
