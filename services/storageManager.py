import os


class FsStorageClient:

    def __init__(self, config):
        self.config = config

    def save_report(self, data, client, date):

        date = date.replace("/", "-")

        base_dir = self.config["base_dir"] + client

        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        date_dir = base_dir + "/" + date

        if not os.path.exists(date_dir):
            os.mkdir(date_dir)

        file_name = date_dir + "/" + client + "_" + date + ".csv"

        data.to_csv(file_name, index=False)


class StorageManager:

    def __init__(self, config):
        self.config = config

    def get_storage_client(self):

        if self.config["type"] == "fs":
            return FsStorageClient(self.config)
