import json


class AbstractProfileSerializer(object):

    def __init__(self, profile_obj):
        self._profile_obj = profile_obj

    def write_profile_to_file(self, target_file):
        with open(target_file, "w") as out_stream:
            json.dump(self._profile_obj, out_stream, indent=2)

    def get_string_representation(self):
        return json.dumps(self._profile_obj, indent=2)
