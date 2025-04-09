import os
import stat


class ConfigProtector:

    @staticmethod
    def set_read_only(file_path: str) -> None:
        # Set the file to read-only mode
        os.chmod(file_path, stat.S_IREAD)

    @staticmethod
    def unset_read_only(file_path: str) -> None:
        # Set the file to read-only mode
        os.chmod(file_path, stat.S_IWRITE | stat.S_IREAD)

    @staticmethod
    def protect_all_json_files(folder_path: str) -> None:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    os.chmod(full_path, stat.S_IREAD)

    @staticmethod
    def unprotect_all_json_files(folder_path: str):
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    os.chmod(full_path, stat.S_IWRITE | stat.S_IREAD)


if __name__ == "__main__":
    # Example usage
    ConfigProtector.set_read_only("configs/users_configs/user_main_data.json")
