import asyncio
from enum import Enum
import time
import pandas as pd
from typing import List
import random
from dataclasses import dataclass, field


@dataclass
class Numbers:
    '''Data class for input and output numbers'''
    input_numbers: List[int] = field(default_factory=list)
    output_numbers: List[int] = field(default_factory=list)


class ExcelCodeGenerator:
    class Config:
        def __init__(self, input_file_path: str, output_file_path: str, should_be_unique: bool, should_have_no_conflict_with_input_numbers: bool, digits: int):
            self.execl_file_handler_config: ExcelFileHandler.Config = ExcelFileHandler.Config(
                input_file_path, output_file_path)
            self.unique_random_generator_config: UniqueRandomGenerator.Config = UniqueRandomGenerator.Config(
                should_be_unique, should_have_no_conflict_with_input_numbers, digits)

    def __init__(self, config: Config):
        self.config: ExcelCodeGenerator.Config = config
        self.numbers: Numbers = Numbers()
        self.file_handler: ExcelFileHandler = ExcelFileHandler(
            self.config.execl_file_handler_config, self.numbers)
        self.generator: UniqueRandomGenerator = UniqueRandomGenerator(
            self.config.unique_random_generator_config, self.numbers)

    def do_the_work(self, show_progress: bool = True):
        print("reading", end="\n", flush=True)
        self.file_handler.read()
        print("generating", end="", flush=True)
        self.generator.generate()
        print("\nwriting", end="\n", flush=True)
        self.file_handler.write()


class ExcelFileHandler:
    class Config:
        def __init__(self, input_file_path: str, output_file_path: str):
            self.input_file_path: str = input_file_path
            self.output_file_path: str = output_file_path
            self._check()

        def _check(self):
            if self.input_file_path == self.output_file_path:
                print("Error: input[{}] file is same as output[{}], choose different output name".format(
                    self.input_file_path, self.output_file_path))
                exit(-1)

    def __init__(self, config: Config, numbers: Numbers):
        self.config = config
        self.numbers = numbers

    def read(self):
        xl = pd.ExcelFile(self.config.input_file_path)
        sheet1 = xl.parse(0)

        self.numbers.input_numbers.extend(
            list(map(lambda x: int(x), sheet1.iloc[:, 0])))

    def write(self):
        df = pd.DataFrame({'input': self.numbers.input_numbers,
                           'output': self.numbers.output_numbers})

        writer = pd.ExcelWriter(self.config.output_file_path)
        df.to_excel(writer, 'Sheet1', index=False)
        writer.save()


class UniqueRandomGenerator:
    @dataclass
    class Config:
        should_be_unique: bool = True
        should_have_no_conflict_with_input_numbers: bool = True
        digits: int = 8

    def __init__(self, config: Config, numbers: Numbers):
        self.config = config
        self.numbers = numbers

    def _generate_n_digit_random(self):
        lower_value: int = 10**(self.config.digits - 1)
        if lower_value == 1:
            lower_value = 0
        upper_value: int = 10**self.config.digits - 1
        number: int = random.randint(lower_value, upper_value)
        return number

    def generate(self):
        number: int = 0
        progress_prev: int = 0
        progress_current: int = 0

        while len(self.numbers.output_numbers) < len(self.numbers.input_numbers):
            progress_current = int(len(self.numbers.output_numbers) // (len(self.numbers.input_numbers) // 100 ))
            if progress_current > progress_prev:
                if progress_current % 5 == 0:
                    print(" %{} ".format(progress_current), end="", flush=True)
                else:
                    print(".", end="", flush=True)
                progress_prev=progress_current
            number=self._generate_n_digit_random()
            if self.config.should_be_unique:
                if number in self.numbers.output_numbers:
                    continue
            if self.config.should_have_no_conflict_with_input_numbers:
                if number in self.numbers.input_numbers:
                    continue
            self.numbers.output_numbers.append(number)
