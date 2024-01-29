# -*- coding:utf8 -*-
import pandas as pd
import json
import argparse


def convert_csv_to_json_and_save(csv_file_path, json_file_path):
    """转换数据格式
    把csv格式的数据转换为用于训练的格式

    Args:
        csv_file_path:
        json_file_path:

    csv的columns: [uuid, input_query, nlu]
    ['ecdebffbaf084160a9d7bba2af12bc9b', '体育招生宣传海报，横版海报', '{"有效": true, "场景": "横版海报", "颜色": null, "设计用途": "体育招生宣传海报", "人物": null, "时间": null, "地点": null, "关键词": "体育招生宣传", "主标题": null}']

    json格式:
    [
      {
        "id": "identity_0",
        "conversations": [
          {
            "from": "user",
            "value": "你好"
          },
          {
            "from": "assistant",
            "value": "我是一个语言模型，我叫通义千问。"
          }
        ]
      }
    ]
    """
    origin_datas = pd.read_csv(csv_file_path, usecols=["uuid", "input_query","nlu"]).dropna().values.tolist()
    datas = []
    for n, (uuid, input_query, nlu_result) in enumerate(origin_datas, start=1):
        print(f"进度: {n}/{len(origin_datas)}", end="\r")
        if not input_query or not nlu_result:
            print(f"uuid: {uuid}\ninput_query: {input_query}\nnlu_result:{nlu_result}")
            continue

        data = {"id":f"{uuid}",
                "conversations":[
                    {"from": "user", "value": input_query},
                    {"from": "assistant", "value":  str(json.loads(nlu_result))}]}
        datas.append(data)
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(datas, jsonfile, ensure_ascii=False)
    print(f"save to {json_file_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file_path", type=str, required=True)
    parser.add_argument("--json_file_path", type=str, required=True)
    args = parser.parse_args()
    csv_file_path = args.csv_file_path
    json_file_path = args.json_file_path
    message = convert_csv_to_json_and_save(csv_file_path, json_file_path)