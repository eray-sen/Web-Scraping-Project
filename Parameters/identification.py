class parameters:
    """Contains 'header' to identify the User-Agent and the base urls that are used during running the project"""

    def __init__(self):
        super().__init__()
        self.header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"}
        self.url = "https://remote.co/remote-jobs/"
        self.base_url = "https://remote.co"
