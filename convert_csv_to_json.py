import csv
import json
import argparse

def convert_csv_to_json_and_save(csv_file_path, json_file_path):
    result = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["input_query"] is None or row["nlu"] is None:
                continue
            if row["input_query"] == "" or row["nlu"] == "":
                continue
            
            # import pdb; pdb.set_trace()
            
            json_string = row["nlu"].replace("'", '"').replace('True', 'true').replace('False', 'false').replace('None', 'null')
            nlu_dict = json.loads(json_string)
            if nlu_dict["场景"]:
                try:
                    assert nlu_dict["场景"] in ["PC端banner", "手机淘宝banner", "移动端banner", "电商横版海报", "电商全屏海报", "电商竖版海报",
                                               "商品主图", "众号封面首图", "公众号封面小图", "横版海报", "每日一签", "竖版海报", "手机海报", "邀请函"]
                except:
                    print(nlu_dict["场景"])

            conversation = {
                "id": row["uuid"],
                "conversations": [
                    {
                        "from": "user",
                        "value": json_string
                    },
                    {
                        "from": "assistant",
                        "value": row["nlu"]
                    }
                ]
            }
            result.append(conversation)

    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(result, jsonfile, ensure_ascii=False, indent=4)

    return f"Data saved to {json_file_path}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file_path", type=str, required=True)
    parser.add_argument("--json_file_path", type=str, required=True)
    args = parser.parse_args()
    csv_file_path = args.csv_file_path
    json_file_path = args.json_file_path
    message = convert_csv_to_json_and_save(csv_file_path, json_file_path)