from logic.logger import logger as log


class Validator:

    @staticmethod
    def validate(rule_key, rule_value, value):
        match rule_key:
            case "min":
                log.info(f"Should be more than {rule_value}")
                try:
                    value = int(value)
                except ValueError:
                    log.error(f"{value} is not numeric")
                    return False
                if value < rule_value:
                    log.error(
                        f"{value} is less than min possible ({rule_value})"
                    )
                    return False
            case "max":
                log.info(f"'{rule_key}' should be less than {rule_value}")
                try:
                    value = int(value)
                except ValueError:
                    log.error(f"{value} is not numeric")
                    return False
                if value > rule_value:
                    log.error(
                        f"{value} is greater than max possible ({rule_value})"
                    )
                    return False
            case "numeric":
                log.info("Should be numeric")
                if not str(value).isnumeric():
                    log.error(f"{value} is not numeric")
                    return False
        log.info("This check is OK!")
        return True
