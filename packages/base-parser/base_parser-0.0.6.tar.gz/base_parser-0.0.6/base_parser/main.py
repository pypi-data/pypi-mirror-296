import argparse
import threading
import config_parser.config as cnf
from json_parsable import ParserJson
from excel_parsable import ParserExcel
from pdf_parsable import ParserPDF
from xml_parsable import ParserXML
from custom_parsable import ParserCustom
from site_parsable import ParserHTML
from log.logger import Logger
import utils


def main(cnf):
    h = Logger()
    parser_name = cnf.get_source_type()

    match parser_name:
        case "0":
            h.Info("Found type 0. Starting parsing Custom...")
            parser = ParserCustom(cnf)
        case "1":
            h.Info("Found type 1. Starting parsing HTML...")
            parser = ParserHTML(cnf)
        case "2":
            h.Info("Found type 2. Starting parsing XML...")
            parser = ParserXML(cnf)
        case "3":
            h.Info("Found type 3. Starting parsing PDF...")
            parser = ParserPDF(cnf)
        case "4":
            h.Info("Found type 4. Starting parsing Excel...")
            parser = ParserExcel(cnf)
        case "5":
            h.Info("Found type 5. Starting parsing JSON...")
            parser = ParserJson(cnf)
        case _:
            h.Error(f"Unknown parser: {parser_name}")

    try:
        parser.parse()
    except Exception as error:
        h.Error("Error during parser starting: " + error.__str__())


if __name__ == "__main__":
    h = Logger()
    parser = argparse.ArgumentParser(
        prog='Base_Parser',
        description='Parsing based on config file',
        epilog='See logs in log/logs folder')
    parser.add_argument('-c', "--config", action='append', type=str, nargs='+')
    args = parser.parse_args()
    if len(args.config) >= 1:
        for path in args.config:
            if utils.check_path(path[0]):
                config = cnf.Config(path[0])
                config.load_yaml_config()
                h.Info(f"Provided config: {path[0]} exists. Starting parse task")
                # todo Handle yaml validation
                t = threading.Thread(target=main, args=(config,))
                t.start()
                t.join()
            else:
                continue
    else:
        h.Error(f"Arguments not provided")
        exit(1)
