#!/usr/bin/env python3
# encoding: utf-8

import json
import eml_parser
import datetime
from cortexutils.analyzer import Analyzer
import email
from email import policy
from email.parser import BytesParser

class EMLParserV2(Analyzer):

    def __init__(self):
        Analyzer.__init__(self)

    def analyse(self, sample, samplename):
        try:
            def json_serial(obj):
                if isinstance(obj, datetime.datetime):
                    serial = obj.isoformat()
                    return serial

            with open(sample, 'rb') as fhdl:
                raw_email = fhdl.read()

            #Lets Grab All Dem Headers
            ep = eml_parser.EmlParser()
            parsed_eml = ep.decode_email_bytes(raw_email)

            jsonEML = json.dumps(parsed_eml, default=json_serial)
            jsonEML = json.loads(jsonEML)
            
            #Grab the email body and pass into the report
            with open(sample, 'rb') as fp:
                msg = BytesParser(policy=policy.default).parse(fp)
            text = msg.get_body(preferencelist=('plain')).get_content()

            self.build_report(jsonEML, text)

        except Exception as e:
            self.unexpectedError(e)

    def build_report(self, report, body):
        raw_report = {}

        # Basic Header Information
        raw_report["subject"] = report["header"]["subject"]
        raw_report["from"] = report["header"]["from"]
        raw_report["to"] = report["header"]["to"]
        raw_report["date"] = report["header"]["date"]

        # Email Routing Information
        raw_report["received"] = report["header"]["received"]

        try:
            raw_report["received_domain"] = report["header"]["received_domain"]
        except:
            raw_report["received_domain"] = "[]"

        try:
            raw_report["received_ip"] = report["header"]["received_ip"]
        except:
            raw_report["received_ip"] = "[]"

        try:
            raw_report["x-mid"] = report["header"]["header"]["x-mid"]
        except:
            raw_report["x-mid"] = "[]"

        try:
            raw_report["authentication-results"] = report["header"]["header"]["authentication-results"]
        except:
            raw_report["authentication-results"] = "[]"

        try:
            raw_report["dkim-signature"] = report["header"]["header"]["dkim-signature"]
        except:
            raw_report["dkim-signature"] = "[]"

        try:
            raw_report["cc"] = report["header"]["cc"]
        except:
            raw_report["cc"] = "No CC"

        try:
            raw_report["attachment"] = report["attachment"]
        except:
            raw_report["attachment"] = "No Attachments"
            
        try:
            raw_report["body"] = body
        except:
            raw_report["body"] = []

        self.report(raw_report)

    def run(self):
        dataType = self.get_param("dataType")

        # Check For Type = File
        if dataType == "file":
            sample = self.get_param("file")
            samplename = self.get_param("filename")
            self.analyse(sample, samplename)

        else:
            self.error("Data type currently not supported")

    def summary(self, raw):
        taxonomies = []
        namespace = "EML"
        predicate = "Analysis"

        taxonomies.append(self.build_taxonomy(
            namespace, predicate, value="Completed"))
        return {"taxonomies": taxonomies}


if __name__ == "__main__":
    EMLParserV2().run()
