import json
import os
import sys
from abc import abstractmethod
from datetime import datetime
from typing import final
import requests

from .MachineLogAnalytics import start_logging, stop_logging


class ParentMachineInterface:
    property_logger = None

    # LOG API HOST
    log_api_host = "http://ec2-35-171-134-229.compute-1.amazonaws.com:9291"

    # Mount storage folder
    main_folder = "/mnt/qwf-data"

    # Master args from YAML file
    master_args = None

    # File read/write variables
    workflow_name = ""
    machine_name = ""
    machinetemplate_name = ""
    machine_version = ""
    machine_ID = ""
    propertyid = ""
    property_code = ""
    prog_lang = ""
    file_folder = ""
    output_file = ""
    dependent_machine = ""

    # Oprational variables
    input_data = dict()
    dependent_machine_data = dict()

    # Output related variables
    output_data = dict()
    final_data = None
    error_list = []

    def __init__(self):
        print(f"\n\nInitialize an instance of {self.__class__.__name__}")

        try:
            if len(sys.argv) > 1:
                args_string = sys.argv[1]
                print(f"Received input: {args_string}")
                self.master_args = json.loads(args_string)

                self.workflow_name = self.master_args['workflow_name']
                self.machine_name = self.master_args['machine_name']
                self.machinetemplate_name = self.master_args['machinetemplate_name']
                self.machine_version = self.master_args['machine_version']
                self.machine_ID = self.master_args['machine_ID']

                self.prog_lang = self.master_args['prog_lang']
                self.input_data = self.master_args['input_data']
                self.output_file = self.master_args['output']
                self.dependent_machine = self.master_args['depends_machine']

                # Get property code and id from input data
                if self.input_data:
                    self.propertyid = self.input_data['property_id']
                    self.property_code = self.input_data['property_code']

                # Create Fodler with name of Workflow Name
                self.file_folder = os.path.join(self.main_folder, self.workflow_name)

                LOG_FOLDER = 'log_folder'
                os.makedirs(LOG_FOLDER, exist_ok=True)
                FILE_NAME = f'{self.workflow_name}_{self.__class__.__name__}.log'
                FILE_PATH = f'{LOG_FOLDER}/{FILE_NAME}'
                self.property_logger = start_logging(FILE_PATH, self.__class__.__name__)
                self.property_logger.info(f'Start Job For Machine ::{self.__class__.__name__}')

                # Check if the directory exists
                if not os.path.exists(self.file_folder):
                    self.property_logger.info(f"Volume path {self.file_folder} does not exist.")
                    os.makedirs(self.file_folder)
                    self.property_logger.info(f"Volume folder {self.file_folder} created")
                else:
                    self.property_logger.info(f"Volume path {self.file_folder} exists.")

                # Machine initialized
                self.__workflowmachinelogsave(machinetemplate=self.machinetemplate_name,
                                              workflowname=self.workflow_name,
                                              logdata=f'{self.machinetemplate_name} call initialized.', status='start',
                                              propertyid=self.propertyid)

        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
        except Exception as e:
            print(e)
        finally:
            print("INIT DONE")

    @abstractmethod
    def receiving(self):
        self.property_logger.info("CALL READING")
        # Clear error list, before start this step
        self.error_list = []

        # Machine receiving
        self.__workflowmachinelogsave(machinetemplate=self.machinetemplate_name, workflowname=self.workflow_name,
                                      logdata=f'{self.machinetemplate_name} call receiving.', status='start',
                                      propertyid=self.propertyid)
        try:
            self.property_logger.info(f"input data : {self.input_data}")
            self.property_logger.info(f"dependent_machine list : {self.dependent_machine}")
            if self.dependent_machine and len(self.dependent_machine) > 0:
                for i in self.dependent_machine:
                    file_path = f"{self.file_folder}/output_{i}.json"
                    if os.path.isfile(file_path):
                        self.property_logger.info(f"File '{file_path}' exists.")
                        with open(file_path) as json_file:
                            output_json = json.load(json_file)
                            if output_json and output_json['result'] == 'success':
                                if output_json['data']:
                                    self.dependent_machine_data = {**self.dependent_machine_data, **output_json['data']}
                    else:
                        self.property_logger.info(f"File '{file_path}' does not exist.")

            self.property_logger.info(f"dependent machine data : {self.dependent_machine_data}")
        except json.JSONDecodeError as e:
            msg = str(e)
            self.error_list.append(msg)
        except Exception as e:
            msg = str(e)
            self.error_list.append(msg)
        finally:
            pass

    @abstractmethod
    def pre_processing(self):
        self.property_logger.info("CALL PRE_PROCESSING")
        # Clear error list, before start this step
        self.error_list = []
        # Machine pre_processing
        self.__workflowmachinelogsave(machinetemplate=self.machinetemplate_name, workflowname=self.workflow_name,
                                      logdata=f'{self.machinetemplate_name} call pre_processing.', status='start',
                                      propertyid=self.propertyid)

    @abstractmethod
    def processing(self):
        self.property_logger.info("CALL PROCESSING")
        # Clear error list, before start this step
        self.error_list = []
        # Machine processing
        self.__workflowmachinelogsave(machinetemplate=self.machinetemplate_name, workflowname=self.workflow_name,
                                      logdata=f'{self.machinetemplate_name} call processing.', status='start',
                                      propertyid=self.propertyid)

    @abstractmethod
    def post_processing(self):
        self.property_logger.info("CALL POST_PROCESSING")
        # Clear error list, before start this step
        self.error_list = []
        # Machine post_processing
        self.__workflowmachinelogsave(machinetemplate=self.machinetemplate_name, workflowname=self.workflow_name,
                                      logdata=f'{self.machinetemplate_name} call post_processing.', status='start',
                                      propertyid=self.propertyid)

    @abstractmethod
    def packaging_shipping(self):
        self.property_logger.info("CALL PACKAGING_SHIPPING")
        # Clear error list, before start this step
        self.error_list = []
        # Machine packaging_shipping
        self.__workflowmachinelogsave(machinetemplate=self.machinetemplate_name, workflowname=self.workflow_name,
                                      logdata=f'{self.machinetemplate_name} call packaging_shipping.', status='start',
                                      propertyid=self.propertyid)

    # Use in Started Machine
    def workflow_start(self):
        self.__workflowlogsave(workflowname=self.workflow_name, logdata=f'{self.workflow_name} started.',
                               status='start', propertyid=self.propertyid)

    # Use in Exit Machine
    def workflow_end(self):
        self.__workflowlogsave(workflowname=self.workflow_name, logdata=f'{self.workflow_name} end.', status='end',
                               propertyid=self.propertyid)

    def __workflowlogsave(self, workflowname, logdata, status, propertyid):
        try:
            self.property_logger.info(f"API LOG:: Workflow Status Update")

            # Define the API endpoint
            url = f"{self.log_api_host}/api/v1/WorkFlow/workflowlogsave"

            # Define the payload (the data you're sending in the POST request)
            form_data = {
                "workflowname": workflowname,
                "logdata": logdata,
                "status": status,
                "propertyid": propertyid
            }

            # Make the POST request
            response = requests.post(url, data=form_data)

            self.property_logger.info(f"API LOG:: Request URL: {response.request.url}")
            self.property_logger.info(f"API LOG:: Request Body: {response.request.body}")
            self.property_logger.info(f"API LOG:: Response Status Code: {response.status_code}")
            self.property_logger.info(f"API LOG:: Response Content: {response.text}")
        except Exception as e:
            msg = f"API LOG:: An error occurred: {e}"
            self.property_logger.info(msg)

    def __workflowmachinelogsave(self, machinetemplate, workflowname, logdata, status, propertyid):
        try:
            self.property_logger.info(f"API LOG:: Machine Status Update")

            # Define the API endpoint
            url = f"{self.log_api_host}/api/v1/WorkFlow/workflowmachinelogsave"

            # Define the payload (the data you're sending in the POST request)
            form_data = {
                "machinetemplate": machinetemplate,
                "workflowname": workflowname,
                "logdata": logdata,
                "status": status,
                "propertyid": propertyid
            }

            # Make the POST request
            response = requests.post(url, data=form_data)

            self.property_logger.info(f"API LOG:: Request URL: {response.request.url}")
            self.property_logger.info(f"API LOG:: Request Body: {response.request.body}")
            self.property_logger.info(f"API LOG:: Response Status Code: {response.status_code}")
            self.property_logger.info(f"API LOG:: Response Content: {response.text}")
        except Exception as e:
            msg = f"API LOG:: An error occurred: {e}"
            self.property_logger.info(msg)

    @final
    def start(self):
        start_time = datetime.now()

        if len(self.error_list) == 0:
            if self.receiving():
                if self.pre_processing():
                    if self.processing():
                        if self.post_processing():
                            if self.packaging_shipping():
                                message = "All steps executed successfully!"
                                self.output_data = {
                                    'result': 'success',
                                    'message': message,
                                    'error_list': self.error_list,
                                    'data': self.final_data,
                                    'master_args': self.master_args
                                }
                            else:
                                message = "packaging_shipping step did not execute."
                                self.output_data = {
                                    'result': 'failed',
                                    'message': message,
                                    'error_list': self.error_list,
                                    'data': None,
                                    'master_args': self.master_args
                                }
                        else:
                            message = "post_processing step did not execute."
                            self.output_data = {
                                'result': 'failed',
                                'message': message,
                                'error_list': self.error_list,
                                'data': None,
                                'master_args': self.master_args
                            }
                    else:
                        message = "processing step did not execute."
                        self.output_data = {
                            'result': 'failed',
                            'message': message,
                            'error_list': self.error_list,
                            'data': None,
                            'master_args': self.master_args
                        }
                else:
                    message = "pre_processing step did not execute."
                    self.output_data = {
                        'result': 'failed',
                        'message': message,
                        'error_list': self.error_list,
                        'data': None,
                        'master_args': self.master_args
                    }
            else:
                message = "receiving step did not execute."
                self.output_data = {
                    'result': 'failed',
                    'message': message,
                    'error_list': self.error_list,
                    'data': None,
                    'master_args': self.master_args
                }
        else:
            message = "Machine init step did not execute."
            self.output_data = {
                'result': 'failed',
                'message': message,
                'error_list': self.error_list,
                'data': None,
                'master_args': self.master_args
            }

        end_time = datetime.now()
        output_file_path = os.path.join(self.file_folder, f"output_{self.output_file}")
        try:
            # Write output into output file
            with open(output_file_path, 'w') as json_file:
                json.dump(self.output_data, json_file, indent=4)
        except Exception as e:
            self.property_logger.info(str(e))

        completion_time = str(end_time - start_time).split('.')[0]
        self.property_logger.info(f"completion_time :: {completion_time}")
        # Stop Property Level logging
        stop_logging(self.property_logger)

        # Handle
        if self.output_data and self.output_data['result'] == 'success':
            # Machine success
            self.__workflowmachinelogsave(machinetemplate=self.machinetemplate_name, workflowname=self.workflow_name,
                                          logdata=f'{self.machinetemplate_name} successfully finished.', status='end',
                                          propertyid=self.propertyid)
            sys.exit(0)  # Zero exit code indicates success
        else:
            # Machine success
            self.__workflowmachinelogsave(machinetemplate=self.machinetemplate_name, workflowname=self.workflow_name,
                                          logdata=f'{self.machinetemplate_name} failed with error.', status='failed',
                                          propertyid=self.propertyid)
            sys.exit(1)  # Non-zero exit code indicates failure
