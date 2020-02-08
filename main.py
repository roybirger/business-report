from services.configManager import ConfigManager
from services.authenticationManager import AuthenticationManger
from services.reportFetcher import ReportFetcher

if __name__ == "__main__":

    config = ConfigManager().get_config()

    try:
        auth_data = AuthenticationManger(config["Auth"]).login()

        from_date = "12/26/2019"
        to_date = "12/27/2019"

        c = ReportFetcher().get_report(auth_data=auth_data, from_date=from_date, to_date=to_date)

        file_name = "test2.csv"

        c.to_csv(file_name, index=False)

    except Exception:
        print("Report process failed")
