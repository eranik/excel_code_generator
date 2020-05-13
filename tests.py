import excel_code_generator as ecg


def test_UniqueRandomGenerator():
    urg_config: ecg.UniqueRandomGenerator.Config = ecg.UniqueRandomGenerator.Config(
        True, True, 1)
    numbers: ecg.Numbers = ecg.Numbers([1, 2, 3, 4])
    urg: ecg.UniqueRandomGenerator = ecg.UniqueRandomGenerator(
        urg_config, numbers)
    urg.generate()
    print(numbers.output_numbers)


# test_UniqueRandomGenerator()

def test_ExcelFileHandler():
    config: ecg.ExcelFileHandler.Config = ecg.ExcelFileHandler.Config(
        "input.xlsx", "output.xlsx")
    numbers: ecg.Numbers = ecg.Numbers()
    file_handler: ecg.ExcelFileHandler = ecg.ExcelFileHandler(config, numbers)
    file_handler.read()
    print(numbers.input_numbers)
    print(numbers.output_numbers)


# test_ExcelFileHandler()

def test_ExcelCodeGenerator():
    config: ecg.ExcelCodeGenerator.Config = ecg.ExcelCodeGenerator.Config(
        "input.xlsx", "output.xlsx", True, True, 8)
    worker: ecg.ExcelCodeGenerator = ecg.ExcelCodeGenerator(config)
    worker.do_the_work()


test_ExcelCodeGenerator()
