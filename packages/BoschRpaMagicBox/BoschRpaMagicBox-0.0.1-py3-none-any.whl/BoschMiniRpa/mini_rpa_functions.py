from mini_rpa_core import *


class MiniRpaFunction(MiniRPACore):
    def __init__(self, user_name: str, user_password: str, server_ip: str, server_name: str, share_name: str, port: int,
                 from_period: str, to_period: str, report_save_path: str, report_process_folder_path: str, process_cache_data: dict, process_number: int,
                 file_name_suffix_type: str, process_dict: dict, update_file_condition_setting: dict, from_file_condition_setting: dict, data_type_dict: dict,
                 is_download=False, is_process: bool = False, is_delivery: bool = False):
        """This function is used to initial parameters

        Args:
            user_name(str): This is the username
            user_password(str): This is the password
            server_ip(str): This is the ip address of the public folder, which can be same as server name
            server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
            share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
            port(int): This is the port number of the server name

            from_period(str):This is the start month
            to_period(str): This is the end month
            report_process_folder_path(str): This is the file path for process excel
            report_save_path(str): This is the folder path for original data
            is_delivery(bool): This is the indicator whether to delivery files to folders, receivers or api
            is_process(bool): This is the indicator whether to process data
            process_cache_data(dict): This is the dict that save the process data
            data_type_dict(dict): This is the dict that save the data type
            process_number(int): This is the number of process
            file_name_suffix_type(str): This is the suffix type of file name. e.g. period, current_date,no_suffix
            process_dict(dict): This is the dict that save the process logic data
            update_file_condition_setting(list): This is the list of update file condition setting
            from_file_condition_setting(list): This is the list of from file condition setting
        """
        super().__init__(user_name, user_password, server_ip, server_name, share_name, port, from_period, to_period, report_save_path,
                         report_process_folder_path, process_cache_data, process_number, file_name_suffix_type, process_dict, update_file_condition_setting,
                         from_file_condition_setting, data_type_dict, is_download, is_process, is_delivery)

    def keep(self, file_path: str, sheet_name: str, process_number: int, is_save: bool, file_name: str) -> Union[pandas.DataFrame, None]:
        """This function is used to remove data from loaded file

        Args:
            file_path(str): This is the file path of target Excel file path
            sheet_name(str): This is the sheet name of Excel file
            process_number(int): This is the process number
            is_save(bool): This is indicator whether to save processed data
            file_name(str): This is the file name of current file
        """
        target = None
        if os.path.exists(file_path):
            target, target_dtype_dict = self.get_from_or_update_data(file_path, file_name, sheet_name, process_number, True, 'from_file')
            self.process_cache_data[process_number][file_name] = target
            self.save_file(process_number, file_name, target_dtype_dict, target, 'keep', is_save)
            print(f'---------------keep result of process no {process_number}---------------')
            print(target)
            print('\n')
        return target

    def start_bot(self):
        """This function is used to collect all function and start to run bot

        """
        time_start = perf_counter()
        if self.is_process:
            self.prepare_data_type()
            self.initial_process_cache_data()

            process_number = self.process_number
            function_name = self.process_dict['function_name']
            is_save = self.process_dict['is_save']

            if function_name == 'keep':
                self.keep(self.from_file_name, self.from_sheet_name, process_number, is_save, self.from_file_name)

        time_end = perf_counter()
        total_time_in_minutes = round((time_end - time_start) / 60, 2)
        print(f'Congratulations, all work has been completed successfully!\nTotal Time: {total_time_in_minutes} minutes.')
