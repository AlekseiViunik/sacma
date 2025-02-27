from logic.logger import logger as log


class Validator:

    @staticmethod
    def validate(rule_key, rule_value, value):
        log.info(f"Check {rule_key} = {value}")
        match rule_key:
            case "min":
                log.info(f"'{rule_key}' should be more than {rule_value}")
                try:
                    value = int(value)
                except ValueError:
                    log.error(f"{rule_key}={value} is not numeric")
                    return False
                if value < rule_value:
                    log.error(
                        f"{rule_key}={value} is less than min possible"
                        f"({rule_value})"
                    )
                    return False
            case "max":
                log.info(f"'{rule_key}' should be less than {rule_value}")
                try:
                    value = int(value)
                except ValueError:
                    log.error(f"{rule_key}={value} is not numeric")
                    return False
                if value > rule_value:
                    log.error(
                        f"{rule_key}={value} is greater than max possible"
                        f"({rule_value})"
                    )
                    return False
            case "numeric":
                log.info(f"'{rule_key}' should be numeric")
                if not str(value).isnumeric():
                    log.error(f"{rule_key}={value} is not numeric")
                    return False
        log.info("Data's been checked. Everithing's OK!")
        return True
