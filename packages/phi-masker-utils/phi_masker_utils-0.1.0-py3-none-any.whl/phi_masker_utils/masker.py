# -*- coding: utf-8 -*-
"""TBD."""
import csv
import logging
import os

from datetime import datetime
from faker import Faker

from phi_masker_utils import constants
from phi_masker_utils.file_utils import check_infile_status


class Masker:
    """Class for masking tab-delimited files, comma-separated files and Excel worksheets."""

    def __init__(self, **kwargs):
        """Constructor for Masker."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.infile = kwargs.get("infile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        check_infile_status(self.infile)
        check_infile_status(self.config_file)

        self._masked_lookup = {}

        self.faker = Faker()

        if self.outfile is None or self.outfile == "":
            self._derive_outfile()

        self.extension = os.path.splitext(self.infile)[1]
        if self.extension.startswith("."):
            self.extension = self.extension[1:]

        logging.info(f"Instantiated Masker in file '{os.path.abspath(__file__)}'")

    def _derive_outfile(self):
        basename = os.path.basename(self.infile)
        extension = os.path.splitext(self.infile)[1]
        self.outfile = os.path.join(
            self.outdir,
            f"{basename}.{extension}"
        )

        if self.infile == self.outfile:
            self.outfile = os.path.join(
                self.outdir,
                f"{basename}_masked.{extension}"
            )

        logging.info(f"Derived outfile '{self.outfile}' for infile '{self.infile}'")

    def mask_phi_values(self):
        """Mask the PHI values in the input file."""
        if self.extension == "csv":
            self._mask_csv()
        elif self.extension == "tsv" or self.extension == "txt":
            self._mask_tsv()
        elif self.extension == "xlsx":
            self._mask_xlsx()
        else:
            raise Exception(f"Unsupported file extension '{self.extension}'")
        self._write_masked_values()

    def _write_masked_values(self):
        """Write the masked values to the output file."""
        outfile = os.path.join(self.outdir, "masked_values.txt")

        with open(outfile, 'w') as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## config_file: {self.config_file}\n")
            of.write(f"## infile: {self.infile}\n")
            of.write(f"## outfile: {self.outfile}\n")
            of.write(f"## logfile: {self.logfile}\n")

            for key, value in self._masked_lookup.items():
                of.write(f"{key} -> {value}\n")

        logging.info(f"Wrote masked values file '{outfile}'")
        if self.verbose:
            print(f"Wrote masked values file '{outfile}'")

    def _load_delimited_rules(self):
        """Load the delimited mask rules from the config file."""
        if "rules" not in self.config:
            raise Exception(f"Missing 'rules' section in config file '{self.config_file}'")

        if "delimited" not in self.config["rules"]:
            raise Exception(f"Missing 'delimited' section in 'rules' section in config file '{self.config_file}'")

        self.rules = self.config.get("rules").get("delimited")

        logging.info(f"Loaded delimited rules from config file '{self.config_file}'")

    def _load_xlsx_rules(self):
        """Load the Excel xlsx file mask rules from the config file."""
        if "rules" not in self.config["rules"]:
            raise Exception(f"Missing 'rules' section in config file '{self.config_file}'")

        if "xlsx" not in self.config["rules"]:
            raise Exception(f"Missing 'xlsx' section in 'rules' section in config file '{self.config_file}'")

        self.rules = self.config.get("rules").get("xlsx")

        logging.info(f"Loaded xlsx rules from config file '{self.config_file}'")

    def _mask_delimited_value(self, value: str, field_name: str) -> str:
        """Mask the value of a delimited field."""
        if field_name not in self.rules:
            logging.info(f"Missing rule for field '{field_name}' in config file '{self.config_file}'")
            return value

        if value not in self._masked_lookup:

            logging.info(f"Will attempt to mask '{value}' for field '{field_name}'")

            datatype = self.rules[field_name].get("datatype", None)

            if datatype is None:
                if "values" not in self.rules[field_name]:
                    datatype = "string"
                    logging.warning(f"Missing 'datatype' for field '{field_name}' in config file '{self.config_file}' so set to default '{datatype}'")
                else:
                    # Randomly select a value from the list of values
                    values = self.rules[field_name].get("values")
                    new_value = self.faker.random_element(elements=values)
                    self._masked_lookup[value] = new_value
                    return new_value

            if datatype.lower() == "date":
                format = self.rules[field_name].get("format", None)
                if format is None:
                    format = "YYYY-MM-DD"
                    logging.warning(f"Missing 'format' for field '{field_name}' in config file '{self.config_file}' so set to default '{format}'")
                if format.upper() == "YYYY-MM-DD":
                    date = self.faker.date_object()
                    new_value = date.strftime("%Y-%m-%d")
                    self._masked_lookup[value] = new_value

                else:
                    raise Exception(f"Unsupported date format '{format}' for field '{field_name}' in config file '{self.config_file}'")
            elif datatype.lower() == "age":
                new_value = self.faker.random_int(min=1, max=100)
                self._masked_lookup[value] = new_value
            elif datatype.lower() == "email":
                new_value = self.faker.email()
                self._masked_lookup[value] = new_value
            elif datatype.lower() == "first_name":
                new_value = self.faker.first_name()
                self._masked_lookup[value] = new_value
            elif datatype.lower() == "full_name":
                new_value = self.faker.name()
                self._masked_lookup[value] = new_value
            elif datatype.lower() == "last_name":
                new_value = self.faker.last_name()
                self._masked_lookup[value] = new_value
            elif datatype.lower() == "phone_number":
                new_value = self.faker.phone_number()
                self._masked_lookup[value] = new_value
            elif datatype.lower() == "gender":
                new_value = self.faker.random_element(elements=("Male", "Female"))
                self._masked_lookup[value] = new_value
            elif datatype.lower() == "uuid":
                new_value = self.faker.uuid4()
                self._masked_lookup[value] = new_value
            elif datatype.lower() == "zipcode":
                new_value = self.faker.zipcode()
                self._masked_lookup[value] = new_value
            elif datatype.lower() == "dob":
                new_value = self.faker.date_of_birth()
                self._masked_lookup[value] = new_value

        return self._masked_lookup[value]

    def _mask_csv(self):
        """Mask the PHI values in the input CSV file."""
        logging.info(f"Will mask PHI values in CSV file '{self.infile}'")

        self._load_delimited_rules()

        position_to_header_lookup = {}
        header_to_position_lookup = {}
        header_list = []
        out_records = []
        record_ctr = 0

        with open(self.infile) as f:
            reader = csv.reader(f)
            for row_ctr, row in enumerate(reader):
                if row_ctr == 0:
                    for field_ctr, field in enumerate(row):
                        header_list.append(field)
                        header_to_position_lookup[field] = field_ctr
                        position_to_header_lookup[field_ctr] = field
                        field_ctr += 1
                    logging.info(f"Processed the header of csv file '{self.infile}'")
                else:
                    for field_ctr, field_value in enumerate(row):
                        field_name = position_to_header_lookup[field_ctr]
                        if field_name in self.rules:
                            field_value = self._mask_delimited_value(field_value, field_name)
                            row[field_ctr] = field_value
                    out_records.append(row)

                    record_ctr += 1

            logging.info(f"Processed '{record_ctr}' records in csv file '{self.infile}'")

        with open(self.outfile, 'w') as of:
            header = ",".join(header_list)
            of.write(f"{header}\n")

            for out_record in out_records:
                record = [str(field) for field in out_record]
                line = ",".join(record)
                of.write(f"{line}\n")

        logging.info(f"Wrote masked csv file '{self.outfile}'")
        if self.verbose:
            print(f"Wrote masked csv file '{self.outfile}'")

        logging.info(f"Masked PHI values in CSV file '{self.infile}'")

    def _mask_tsv(self):
        """Mask the PHI values in the input tab-delimited file."""
        logging.info(f"Will mask PHI values in tab-delimited file '{self.infile}'")

        self._load_delimited_rules()

        position_to_header_lookup = {}
        header_to_position_lookup = {}
        header_list = []
        out_records = []
        record_ctr = 0

        with open(self.infile) as f:
            reader = csv.reader(f, delimiter='\t')
            for row_ctr, row in enumerate(reader):
                if row_ctr == 0:
                    for field_ctr, field in enumerate(row):
                        header_list.append(field)
                        header_to_position_lookup[field] = field_ctr
                        position_to_header_lookup[field_ctr] = field
                        field_ctr += 1
                    logging.info(f"Processed the header of tab-delimited file '{self.infile}'")
                else:
                    for field_ctr, field_value in enumerate(row):
                        field_name = position_to_header_lookup[field_ctr]
                        if field_name in self.rules:
                            field_value = self._mask_delimited_value(field_value, field_name)
                            row[field_ctr] = field_value
                    out_records.append(row)

                    record_ctr += 1

            logging.info(f"Processed '{record_ctr}' records in tab-delimited file '{self.infile}'")

        with open(self.outfile, 'w') as of:
            header = "\t".join(header_list)
            of.write(f"{header}\n")

            for out_record in out_records:
                record = [str(field) for field in out_record]
                line = "\t".join(record)
                of.write(f"{line}\n")

        logging.info(f"Wrote masked tab-delimited file '{self.outfile}'")
        if self.verbose:
            print(f"Wrote masked tab-delimited file '{self.outfile}'")

        logging.info(f"Masked PHI values in tab-delimited file '{self.infile}'")
