def Parameter_Validation_Checker(attribute, attribute_value, request):
    if attribute is None or attribute == "":
        Message = attribute_value + " Is Required"
        data = {
            "Message": Message,
            "data": request.data
        }
        return data

    return False


def RegisterView_Validation(request):

    first_name = request.data.get("first_name")
    Response = Parameter_Validation_Checker(first_name, "first_name", request)
    if Response:
        return Response

    last_name = request.data.get("last_name")
    Response = Parameter_Validation_Checker(last_name, "last_name", request)
    if Response:
        return Response

    email = request.data.get("email")
    Response = Parameter_Validation_Checker(email, "email", request)
    if Response:
        return Response

    password = request.data.get("password")
    Response = Parameter_Validation_Checker(password, "password", request)
    if Response:
        return Response

    return False


def SendEmail_Validation(request):
    email = request.data.get("email")
    Response = Parameter_Validation_Checker(email, "email", request)
    if Response:
        return Response

    return False
