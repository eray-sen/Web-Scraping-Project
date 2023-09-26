import time


class array:
    """Contains the arrays that are used during running the project"""
    def __init__(self):
        super().__init__()
        self.main_rec = []
        self.det_rec = []
        self.urls = []
        self.urls_co = []
        self.main_rec_co = []
        self.det_rec_co = []
        self.expired_links = []
        self.rec_fields = []
        self.fields_amount = []
        self.fields = ["Accounting", "Customer-Service", "Online-Data-Entry", "Design", "Developer", "Online-Editing",
                       "Healthcare", "Recruiter", "IT", "Legal", "Marketing", "Project-Manager", "QA", "Sales",
                       "Online-Teaching", "Virtual-Assistant", "Writing", "Other"]
        self.start_time = time.time()
