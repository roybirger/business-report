import requests
import pandas as pd
import io


class ReportFetcher:

    report_url = "https://sellercentral.amazon.com/gp/site-metrics/load/csv/check123.csv"

    def get_report(self, auth_data, from_date, to_date):

        payload = {
            "reportID": "102:DetailSalesTrafficByChildItem",
            "sortIsAscending": 0,
            "sortColumn": 12,
            "fromDate": from_date,
            "toDate": to_date,
            "cols": "/c0/c1/c2/c3/c4/c5/c6/c7/c8/c9/c10/c11",
            "dateUnit": 1,
            "currentPage": 0,
        }

        headers = {}

        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        headers["Accept-Encoding"] = "gzip, deflate, br"
        headers["Accept-Language"] = "en-US,en;q=0.9,he;q=0.8"
        headers["Cache-Control"] = "no-cache"
        headers["Connection"] = "keep-alive"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Host"] = "sellercentral.amazon.com"
        headers["Origin"] = "https] =//sellercentral.amazon.com"
        headers["Pragma"] = "no-cache"
        headers["Referer"] = "https] =//sellercentral.amazon.com/gp/site-metrics/report.html"
        headers["Sec-Fetch-Mode"] = "navigate"
        headers["Sec-Fetch-Site"] = "same-origin"
        headers["Sec-Fetch-User"] = "?1"
        headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        headers["Cookie"] = "aws-account-alias=feedvisor-production-account; " +\
                            "aws-ubid-main=204-5143614-0315015; " +\
                            "; ".join(list(map(lambda cookie: cookie["name"] + "=" + cookie["value"], auth_data)))

        r = requests.post(self.report_url, data=payload, headers=headers)
        c = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        return c
