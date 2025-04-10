import os
import stat


class ConfigProtector:

    @staticmethod
    def set_read_only(file_path: str) -> None:
        """
        Устанавливает файл в режим только для чтения.

        Parameters
        ----------
        - file_path: str
            Путь к файлу, который нужно сделать доступным только для чтения.
        """

        os.chmod(file_path, stat.S_IREAD)

    @staticmethod
    def unset_read_only(file_path: str) -> None:
        """
        Убирает режим только для чтения с файла.

        Parameters
        ----------
        - file_path: str
            Путь к файлу, с которого нужно убрать режим только для чтения.
        """

        os.chmod(file_path, stat.S_IWRITE | stat.S_IREAD)

    @staticmethod
    def protect_all_json_files(folder_path: str) -> None:
        """
        Устанавливает все файлы JSON в указанной папке в режим только для
        чтения.

        Parameters
        ----------
        - folder_path: str
            Путь к папке, содержащей файлы JSON, которые нужно защитить.
        """

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    os.chmod(full_path, stat.S_IREAD)

    @staticmethod
    def unprotect_all_json_files(folder_path: str):
        """
        Убирает режим только для чтения со всех файлов JSON в указанной папке.

        Parameters
        ----------
        - folder_path: str
            Путь к папке, содержащей файлы JSON, с которых нужно убрать защиту.
        """

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    os.chmod(full_path, stat.S_IWRITE | stat.S_IREAD)


if __name__ == "__main__":
    # Example usage
    ConfigProtector.unset_read_only("configs/windows_configs/main_window.json")
