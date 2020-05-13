import excel_code_generator as ecg


def excel_code_generator_runner():
    config: ecg.ExcelCodeGenerator.Config = ecg.ExcelCodeGenerator.Config(
        "input.xlsx", "output.xlsx", True, True, 8)
    worker: ecg.ExcelCodeGenerator = ecg.ExcelCodeGenerator(config)
    worker.do_the_work()

excel_code_generator_runner()
