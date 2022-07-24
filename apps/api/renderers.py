from rest_framework.renderers import JSONRenderer

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        print(status_code)
        response = {
          "status": "success",
          "code": status_code,
          "data": data,
          "message": None
        }
        if not str(status_code).startswith('2'):
            print("here")
            response["status"] = "error"
            response["data"] = None
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["data"] = data
            data["details"] = []
            for i in data:
                if i != "details":
                    if data[i][0] == "This field must be unique.":
                        data["details"].append(f"{i}: This {i} is already taken")
                    else:
                        data["details"].append(f"{i}: {data[i][0]}")
            for i in list(data.keys()):
                if i != "details":
                    del data[i]


        return super(CustomRenderer, self).render(data, accepted_media_type, renderer_context)