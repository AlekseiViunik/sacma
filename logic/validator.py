class Validator:

    @staticmethod
    def validate(rul_key, rul_value, value):
        match rul_key:
            case "min":
                try:
                    value = int(value)
                except ValueError:
                    return False
                if value < rul_value:
                    return False
            case "max":
                try:
                    value = int(value)
                except ValueError:
                    return False
                if value > rul_value:
                    return False
            case "numeric":
                if not str(value).isnumeric():
                    return False
        return True
