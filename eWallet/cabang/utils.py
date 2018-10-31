from rest_framework.routers import SimpleRouter

quorum_path_file = 'cabang/quorum_dummy.json'

class OptionalSlashRouter(SimpleRouter):

    def __init__(self):
        self.trailing_slash = '/?'
        super(SimpleRouter, self).__init__()