import logging
import os

import pandas as pd

from previsedx_esopredict_qc_utils import constants
from previsedx_esopredict_qc_utils.qc.auditor import Auditor
from previsedx_esopredict_qc_utils.qc.reporter import Reporter
from previsedx_esopredict_qc_utils.qc.record import Record
from previsedx_esopredict_qc_utils.esopredict.analysis.results.file.helper import Helper
from previsedx_esopredict_qc_utils.esopredict.analysis.results.intermediate.file.tsv.parser import Parser


class Manager:
    """Class for auditing the QC checks for esopredict."""

    def __init__(self, **kwargs):
        """Constructor for Manager"""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.indir = kwargs.get("indir", None)
        self.infile = kwargs.get("infile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self.actin_file = None
        self.fbn1_file = None
        self.hpp1_file = None
        self.p16_file = None
        self.runx3_file = None
        self.gene_files = []
        self.run_id_list = None

        self.helper = Helper(**kwargs)
        self.auditor = Auditor(**kwargs)
        self.reporter = Reporter(**kwargs)

        self.intermediate_file_records = None

        logging.info(f"Instantiated Manager in file '{os.path.abspath(__file__)}'")

    def _load_dataset_files(self) -> None:
        self.dataset = self.helper.get_dataset()
        self.run_id_list = self.dataset.get_run_ids()

        for run_id in self.run_id_list:
            logging.info(f"Found run_id {run_id}")
            if run_id in self.dataset.run_id_to_actin_file_lookup:
                self.actin_file = self.dataset.run_id_to_actin_file_lookup.get(run_id)
                self.gene_files.append(self.actin_file)
                logging.info(f"Found ACTIN file {self.actin_file}")
            else:
                logging.error(f"Could not find ACTIN file for run_id {run_id}")

            if run_id in self.dataset.run_id_to_fbn1_file_lookup:
                self.fbn1_file = self.dataset.run_id_to_fbn1_file_lookup.get(run_id)
                self.gene_files.append(self.fbn1_file)
                logging.info(f"Found FBN1 file {self.fbn1_file}")
            else:
                logging.error(f"Could not find FBN1 file for run_id {run_id}")

            if run_id in self.dataset.run_id_to_hpp1_file_lookup:
                self.hpp1_file = self.dataset.run_id_to_hpp1_file_lookup.get(run_id)
                self.gene_files.append(self.hpp1_file)
                logging.info(f"Found HPP1 file {self.hpp1_file}")
            else:
                logging.error(f"Could not find HPP1 file for run_id {run_id}")

            if run_id in self.dataset.run_id_to_p16_file_lookup:
                self.p16_file = self.dataset.run_id_to_p16_file_lookup.get(run_id)
                self.gene_files.append(self.p16_file)
                logging.info(f"Found P16 file {self.p16_file}")
            else:
                logging.error(f"Could not find P16 file for run_id {run_id}")

            if run_id in self.dataset.run_id_to_runx3_file_lookup:
                self.runx3_file = self.dataset.run_id_to_runx3_file_lookup.get(run_id)
                self.gene_files.append(self.runx3_file)
                logging.info(f"Found RUNX3 file {self.runx3_file}")
            else:
                logging.error(f"Could not find RUNX3 file for run_id {run_id}")

    def run_qc_checks(self) -> None:
        # pprint(self.dataset)
        # import sys
        # sys.exit(1)

        self._run_pre_report_generation_qc_checks()

        self._run_post_report_generation_qc_checks()

        self.reporter.generate_report(records=self.auditor.get_records())

    def _run_pre_report_generation_qc_checks(self) -> None:
        """Run QC checks on the gene files."""
        self._load_dataset_files()

        self._run_standard_curve_checks()

        self._run_ntc_neg_empty_quantity_mean_checks()

        self._run_dilution_for_standards_checks()

    def _run_post_report_generation_qc_checks(self) -> None:
        """Run QC checks on the esopredict generated intermediate tab-delimited file."""
        self._load_intermediate_file_records()
        self._run_nmv_checks()
        self._run_actin_threshold_checks()

    def _load_intermediate_file_records(self) -> None:
        """Parse the esopredict generated intermediate tab-delimited file."""
        parser = Parser(
            config=self.config,
            config_file=self.config_file,
            logfile=self.logfile,
            outdir=self.outdir,
            verbose=self.verbose,
        )
        self.intermediate_file_records = parser.get_records(self.infile)

    def _get_audit_record(self, id: str) -> Record:
        """Create an audit record.

        Args:
            id (str): The ID of the check.

        Returns:
            Record: The audit record.
        """
        desc = self.config.get("checks").get(id).get("desc")

        name = self.config.get("checks").get(id).get("name")

        record = Record(
            id=id,
            name=name,
            desc=desc,
        )

        return record

    def _run_standard_curve_checks(self, check_id: str = "check_1") -> None:
        """Perform the Standard Curve QC checks.

        Args:
            check_id (str): The ID of the check.
        """
        logging.info("Performing Standard Curve QC checks")
        efficiency_min_threshold = self.config.get("checks").get("efficiency_threshold").get("min")
        efficiency_max_threshold = self.config.get("checks").get("efficiency_threshold").get("max")
        r_squared = self.config.get("checks").get("r_squared")

        pass_list = []
        fail_list = []

        r_squared_lookup = {}
        efficiency_lookup = {}

        error_ctr = 0

        for gene_file in self.gene_files:
            logging.info(f"Processing gene file '{gene_file.basename}'")
            records = self.helper.get_gene_file_records(gene_file)
            for record in records:
                if not record.rsuperscript2 > r_squared:
                    logging.error(f"R-squared value '{record.rsuperscript2}' is not greater than {r_squared} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                    fail_list.append(f"R-squared value '{record.rsuperscript2}' is not greater than {r_squared} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                    error_ctr += 1
                else:
                    if record.rsuperscript2 not in r_squared_lookup:
                        r_squared_lookup[record.rsuperscript2] = True
                        logging.info(f"R-squared value '{record.rsuperscript2}' is greater than {r_squared} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"R-squared value '{record.rsuperscript2}' is greater than {r_squared} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")

                if efficiency_min_threshold < record.efficiency < efficiency_max_threshold:
                    if record.efficiency not in efficiency_lookup:
                        efficiency_lookup[record.efficiency] = True
                        logging.info(f"Efficiency value '{record.efficiency}' is within the range of {efficiency_min_threshold} to {efficiency_max_threshold} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"Efficiency value '{record.efficiency}' is within the range of {efficiency_min_threshold} to {efficiency_max_threshold} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                else:
                    logging.error(f"Efficiency value '{record.efficiency}' is not within the range of {efficiency_min_threshold} to {efficiency_max_threshold} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                    fail_list.append(f"Efficiency value '{record.efficiency}' is not within the range of {efficiency_min_threshold} to {efficiency_max_threshold} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                    error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _run_ntc_neg_empty_quantity_mean_checks(self, check_id: str = "check_2") -> None:
        # Standard curve checks
        # Curve QC
        # Check 1 standard curve
        # R-squared value

        pass_list = []
        fail_list = []

        error_ctr = 0

        for gene_file in self.gene_files:
            logging.info(f"Processing gene file '{gene_file.basename}'")
            records = self.helper.get_gene_file_records(gene_file)
            for record in records:
                if record.samplename.upper().startswith("NTC") or record.samplename.upper().startswith("NEG"):
                    # TODO: Ask Lisa abou EXT-NEG
                    if record.quantitymean is None or pd.isna(record.quantitymean):
                        logging.info(f"Quantity Mean value 'ND' is empty for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"Quantity Mean value 'ND' is empty for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                    else:
                        logging.error(f"Quantity Mean value '{record.quantitymean}' should be empty for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Quantity Mean value '{record.quantitymean}' should be empty for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _run_dilution_for_standards_checks(self, check_id: str = "check_3") -> None:
        """Perform dilution checks for standards.

        Review the five-point standard curve to ensure there are all five standards
        labeled as Standards in the Quantstudio software.  All other sampels should be labeled as
        unknown.  Check the values for the standard curve:

            Standard 1 = 1 in wells A11, A12

            1:5 = 0.2 in wells B11, B12

            1:25 = 0.04 in wells C11, C12

            1:125 = 0.008 in wells D11, D12

            1:625 = 0.0016 in wells E11, E12

        Args:
            check_id (str): The ID of the check.
        """
        # Standard curve checks
        # Curve QC
        # Check 1 standard curve
        # R-squared value

        pass_list = []
        fail_list = []

        error_ctr = 0
        good_ctr = 0

        for gene_file in self.gene_files:

            logging.info(f"Processing gene file '{gene_file.basename}'")
            records = self.helper.get_gene_file_records(gene_file)

            for record in records:
                if record.samplename.upper() == "STD 1":
                    if record.wellposition.upper() == "A11" or record.wellposition.upper() == "A12":
                        if round(record.quantity, 3) == 1.000:
                            logging.info(f"Quantity value '{round(record.quantity, 3)}' is 1.000 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            pass_list.append(f"Quantity value '{round(record.quantity, 3)}' is 1.000 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            good_ctr += 1
                        else:
                            logging.error(f"Quantity value '{round(record.quantity, 3)}' is not 1.000 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            fail_list.append(f"Quantity value '{round(record.quantity, 3)}' is not 1.000 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            error_ctr += 1
                    else:
                        logging.error(f"Sample '{record.samplename}' should be in well position 'A11' or 'A12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Sample '{record.samplename}' should be in well position 'A11' or 'A12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1
                elif record.samplename.upper() == "STD 2":
                    if record.wellposition.upper() == "B11" or record.wellposition.upper() == "B12":
                        if round(record.quantity, 3) == 0.200:
                            logging.info(f"Quantity value '{round(record.quantity, 3)}' is 0.200 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            pass_list.append(f"Quantity value '{round(record.quantity, 3)}' is 0.200 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            good_ctr += 1
                        else:
                            logging.error(f"Quantity value '{round(record.quantity, 3)}' is not 0.200 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            fail_list.append(f"Quantity value '{round(record.quantity, 3)}' is not 0.200 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            error_ctr += 1
                    else:
                        logging.error(f"Sample '{record.samplename}' should be in well position 'B11' or 'B12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Sample '{record.samplename}' should be in well position 'B11' or 'B12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1
                elif record.samplename.upper() == "STD 3":
                    if record.wellposition.upper() == "C11" or record.wellposition.upper() == "C12":
                        if round(record.quantity, 3) == 0.040:
                            logging.info(f"Quantity value '{round(record.quantity, 3)}' is 0.040 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            pass_list.append(f"Quantity value '{round(record.quantity, 3)}' is 0.040 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            good_ctr += 1
                        else:
                            logging.error(f"Quantity value '{round(record.quantity, 3)}' is not 0.040 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            fail_list.append(f"Quantity value '{round(record.quantity, 3)}' is not 0.040 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            error_ctr += 1
                    else:
                        logging.error(f"Sample '{record.samplename}' should be in well position 'C11' or 'C12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Sample '{record.samplename}' should be in well position 'C11' or 'C12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1
                elif record.samplename.upper() == "STD 4":
                    if record.wellposition.upper() == "D11" or record.wellposition.upper() == "D12":
                        if round(record.quantity, 3) == 0.008:
                            logging.info(f"Quantity value '{round(record.quantity, 3)}' is 0.008 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            pass_list.append(f"Quantity value '{round(record.quantity, 3)}' is 0.008 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            good_ctr += 1
                        else:
                            logging.error(f"Quantity value '{round(record.quantity, 3)}' is not 0.008 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            fail_list.append(f"Quantity value '{round(record.quantity, 3)}' is not 0.008 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            error_ctr += 1
                    else:
                        logging.error(f"Sample '{record.samplename}' should be in well position 'D11' or 'D12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Sample '{record.samplename}' should be in well position 'D11' or 'D12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1
                elif record.samplename.upper() == "STD 5":
                    if record.wellposition.upper() == "E11" or record.wellposition.upper() == "E12":
                        if round(record.quantity, 4) == 0.0016:
                            logging.info(f"Quantity value '{round(record.quantity, 4)}' is 0.0016 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            pass_list.append(f"Quantity value '{round(record.quantity, 4)}' is 0.0016 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            good_ctr += 1
                        else:
                            logging.error(f"Quantity value '{round(record.quantity, 4)}' is not 0.0016 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            fail_list.append(f"Quantity value '{round(record.quantity, 4)}' is not 0.0016 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                            error_ctr += 1
                    else:
                        logging.error(f"Sample '{record.samplename}' should be in well position 'E11' or 'E12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Sample '{record.samplename}' should be in well position 'E11' or 'E12', not '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0 or good_ctr != 50:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _run_nmv_checks(self, check_id: str = "check_4") -> None:
        """Perform checks on the intermediate tab-delimited file.

        Check the ACTIN value in the intermediate file to ensure it is greater than 0.0016.

        Args:
            check_id (str): The ID of the check.
        """
        logging.info("Performing NMV checks")

        hpp1_nmv_min_threshold = self.config.get("checks").get("nmv_thresholds").get("hpp1").get("min")
        hpp1_nmv_max_threshold = self.config.get("checks").get("nmv_thresholds").get("hpp1").get("max")

        fbn1_nmv_min_threshold = self.config.get("checks").get("nmv_thresholds").get("fbn1").get("min")
        fbn1_nmv_max_threshold = self.config.get("checks").get("nmv_thresholds").get("fbn1").get("max")

        p16_nmv_min_threshold = self.config.get("checks").get("nmv_thresholds").get("p16").get("min")
        p16_nmv_max_threshold = self.config.get("checks").get("nmv_thresholds").get("p16").get("max")

        runx3_nmv_min_threshold = self.config.get("checks").get("nmv_thresholds").get("runx3").get("min")
        runx3_nmv_max_threshold = self.config.get("checks").get("nmv_thresholds").get("runx3").get("max")

        error_ctr = 0

        pass_list = []
        fail_list = []

        for record in self.intermediate_file_records:

            if not record.sample_id.startswith("POS"):
                continue

            converted_hpp1_nmv = record.hpp1_nmv * 100
            converted_fbn1_nmv = record.fbn1_nmv * 100
            converted_p16_nmv = record.p16_nmv * 100
            converted_runx3_nmv = record.runx3_nmv * 100

            if hpp1_nmv_min_threshold < converted_hpp1_nmv < hpp1_nmv_max_threshold:
                logging.info(f"HPP1 NMV value '{converted_hpp1_nmv}' is within the range of {hpp1_nmv_min_threshold} to {hpp1_nmv_max_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"HPP1 NMV value '{converted_hpp1_nmv}' is within the range of {hpp1_nmv_min_threshold} to {hpp1_nmv_max_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"HPP1 NMV value '{converted_hpp1_nmv}' is not within the range of {hpp1_nmv_min_threshold} to {hpp1_nmv_max_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"HPP1 NMV value '{converted_hpp1_nmv}' is not within the range of {hpp1_nmv_min_threshold} to {hpp1_nmv_max_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

            if fbn1_nmv_min_threshold < converted_fbn1_nmv < fbn1_nmv_max_threshold:
                logging.info(f"FBN1 NMV value '{converted_fbn1_nmv}' is within the range of {fbn1_nmv_min_threshold} to {fbn1_nmv_max_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"FBN1 NMV value '{converted_fbn1_nmv}' is within the range of {fbn1_nmv_min_threshold} to {fbn1_nmv_max_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"FBN1 NMV value '{converted_fbn1_nmv}' is not within the range of {fbn1_nmv_min_threshold} to {fbn1_nmv_max_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"FBN1 NMV value '{converted_fbn1_nmv}' is not within the range of {fbn1_nmv_min_threshold} to {fbn1_nmv_max_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

            if p16_nmv_min_threshold < converted_p16_nmv < p16_nmv_max_threshold:
                logging.info(f"P16 NMV value '{converted_p16_nmv}' is within the range of {p16_nmv_min_threshold} to {p16_nmv_max_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"P16 NMV value '{converted_p16_nmv}' is within the range of {p16_nmv_min_threshold} to {p16_nmv_max_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"P16 NMV value '{converted_p16_nmv}' is not within the range of {p16_nmv_min_threshold} to {p16_nmv_max_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"P16 NMV value '{converted_p16_nmv}' is not within the range of {p16_nmv_min_threshold} to {p16_nmv_max_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

            if runx3_nmv_min_threshold < converted_runx3_nmv < runx3_nmv_max_threshold:
                logging.info(f"RUNX3 NMV value '{converted_runx3_nmv}' is within the range of {runx3_nmv_min_threshold} to {runx3_nmv_max_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"RUNX3 NMV value '{converted_runx3_nmv}' is within the range of {runx3_nmv_min_threshold} to {runx3_nmv_max_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"RUNX3 NMV value '{converted_runx3_nmv}' is not within the range of {runx3_nmv_min_threshold} to {runx3_nmv_max_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"RUNX3 NMV value '{converted_runx3_nmv}' is not within the range of {runx3_nmv_min_threshold} to {runx3_nmv_max_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _run_actin_threshold_checks(self, check_id: str = "check_5") -> None:
        """Perform checks on the intermediate tab-delimited file.

        Check the ACTIN value in the intermediate file to ensure it is greater than 0.0016.

        Args:
            check_id (str): The ID of the check.
        """
        logging.info("Performing Beta-ACTIN threshold checks")
        actin_min_threshold = self.config.get("checks").get("actin_threshold").get("min")

        error_ctr = 0

        pass_list = []
        fail_list = []

        for record in self.intermediate_file_records:
            # logging.info(f"Processing record '{record}'")
            if record.sample_id.startswith("POS"):
                continue

            if record.sample_id.startswith("NEG"):
                continue

            if record.actin_fbn1 > actin_min_threshold:
                logging.info(f"ACTIN FBN1 value '{record.actin_fbn1}' is greater than {actin_min_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"ACTIN FBN1 value '{record.actin_fbn1}' is greater than {actin_min_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"ACTIN FBN1 value '{record.actin_fbn1}' is not greater than {actin_min_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"ACTIN FBN1 value '{record.actin_fbn1}' is not greater than {actin_min_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

            if record.actin_hpp1 > actin_min_threshold:
                logging.info(f"ACTIN HPP1 value '{record.actin_hpp1}' is greater than {actin_min_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"ACTIN HPP1 value '{record.actin_hpp1}' is greater than {actin_min_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"ACTIN HPP1 value '{record.actin_hpp1}' is not greater than {actin_min_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"ACTIN HPP1 value '{record.actin_hpp1}' is not greater than {actin_min_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

            if record.actin_p16 > actin_min_threshold:
                logging.info(f"ACTIN P16 value '{record.actin_p16}' is greater than {actin_min_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"ACTIN P16 value '{record.actin_p16}' is greater than {actin_min_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"ACTIN P16 value '{record.actin_p16}' is not greater than {actin_min_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"ACTIN P16 value '{record.actin_p16}' is not greater than {actin_min_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

            if record.actin_runx3 > actin_min_threshold:
                logging.info(f"ACTIN RUNX3 value '{record.actin_runx3}' is greater than {actin_min_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"ACTIN RUNX3 value '{record.actin_runx3}' is greater than {actin_min_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"ACTIN RUNX3 value '{record.actin_runx3}' is not greater than {actin_min_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"ACTIN RUNX3 value '{record.actin_runx3}' is not greater than {actin_min_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

        record = self._get_audit_record(check_id)

        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)
