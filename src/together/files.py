import requests
import urllib.parse
import posixpath
from typing import Optional


def dispatch_files(args):
    files = Files(args.key)

    if args.files == "list_files":
        response = files.list_files()
        print(response)

    elif args.files == "upload_file":
        response = files.upload_file(args.file)
        print(response)

    elif args.files == "delete_file":
        response = files.delete_file(args.file_id)
        print(response)

    elif args.files == "retrieve_file":
        response = files.retrieve_file(args.file_id)
        print(response)

    elif args.files == "retrieve_file_content":
        response = files.retrieve_file_content(args.file_id, args.output)
        print(response)


class Files:
    def __init__(
        self,
        together_api_key: str,
        endpoint_url: Optional[str] = "https://api.together.xyz/",
    ) -> None:
        self.together_api_key = together_api_key
        self.endpoint_url = urllib.parse.urljoin(endpoint_url, "/v1/files/")

    def list_files(self):
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(self.endpoint_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def upload_file(self, file):
        files = {"file": open(file, "rb")}

        data = {"purpose": "fine-tune"}
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.post(
                self.endpoint_url, headers=headers, files=files, data=data
            ).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def delete_file(self, file_id):
        delete_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.delete(delete_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def retrieve_file(self, file_id):
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def retrieve_file_content(self, file_id, output_file):
        relative_path = posixpath.join(file_id, "content")
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, relative_path)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        # write to file
        open(output_file, "wb").write(response.content)

        return response  # this should be null
