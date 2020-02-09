from services.configManager import ConfigManager
from services.authenticationManager import AuthenticationManger
from services.reportFetcher import ReportFetcher
from services.storageManager import StorageManager

from datetime import datetime, timedelta

if __name__ == "__main__":

    config = ConfigManager().get_config()
    storage = StorageManager(config["params"]["storage"]).get_storage_client()

    for account in config["accounts"]:

        print("Starting report process for account: " + account["name"])

        try:

            auth_data = AuthenticationManger(account["auth"]).login()

            for client in account["clients"]:

                print("Client: " + client["name"])

                from_date = datetime.strptime(client["initial_report_date"], "%m/%d/%Y").date()
                to_date = from_date + timedelta(days=1)
                from_date_str = from_date.strftime("%m/%d/%Y")
                to_date_str = to_date.strftime("%m/%d/%Y")

                while to_date_str != datetime.utcnow().date().strftime("%m/%d/%Y"):

                    print("Fetching report for dates: " + from_date_str + " - " + to_date_str)

                    c = ReportFetcher().get_report(auth_data=auth_data, from_date=from_date_str, to_date=to_date_str)

                    storage.save_report(c, client["name"], from_date_str)

                    from_date = from_date + timedelta(days=1)
                    to_date = to_date + timedelta(days=1)
                    from_date_str = from_date.strftime("%m/%d/%Y")
                    to_date_str = to_date.strftime("%m/%d/%Y")

        except Exception:
            print("Report process failed for account: " + account["name"])
            continue
