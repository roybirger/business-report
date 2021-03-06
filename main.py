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

            auth_mgr = AuthenticationManger(account["auth"])
            auth_mgr.login()

            to_date = datetime.utcnow().date().strftime("%m/%d/%Y")
            from_date = (datetime.utcnow() - timedelta(days=2)).date().strftime("%m/%d/%Y")

            print("Fetching report for dates: " + from_date + " - " + to_date)

            for client in account["clients"]:

                print("Client: " + client["name"])

                auth_data = auth_mgr.select_client(client["name"])

                c = ReportFetcher().get_report(auth_data=auth_data, from_date=from_date, to_date=to_date)

                storage.save_report(c, client["name"], from_date)

        except Exception:
            print("Report process failed for account: " + account["name"])
            if auth_mgr is not None:
                auth_mgr.logout()
            continue

        auth_mgr.logout()
