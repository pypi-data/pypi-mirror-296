import json


def write_output_to_file(out_data, filename="data_output.json"):
    with open(filename, "w") as json_file:
        json.dump(out_data, json_file)


def write_html_report(file_path, url):
    response =requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Report saved to {file_path}")
    else:
        print(f"Failed to fetch the report. Status code: {response.status_code}")
