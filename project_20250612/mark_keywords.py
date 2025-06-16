import json
import requests
import os

# API配置
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def read_input_file(file_path):
    """读取输入文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ 成功读取输入文件")
        return data
    except Exception as e:
        print(f"❌ 读取输入文件失败: {str(e)}")
        return None

def call_api(prompt):
    """调用OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/o4-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        print("✅ API调用成功")
        return result
    except Exception as e:
        print(f"❌ API调用失败: {str(e)}")
        return None

def save_output_file(data, output_path):
    """保存输出文件"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("✅ 成功保存输出文件")
        return True
    except Exception as e:
        print(f"❌ 保存输出文件失败: {str(e)}")
        return False

def main():
    # 文件路径
    input_file = "D:\\CURSOR\\project_20250612\\input_text_1_2_2024.json"
    output_file = "D:\\CURSOR\\project_20250612\\output_marked.json"
    
    # 读取输入文件
    input_data = read_input_file(input_file)
    if not input_data:
        return
    
    # 将输入数据转换为字符串格式
    input_data_str = json.dumps(input_data, ensure_ascii=False, indent=2)
    
    # 构建prompt
    prompt = f"""
    #角色
你是一位富有经验的考研英语 1 对 1 培训老师，现输入json格式的考研阅读真题{input_data_str}，需将用户可能陌生的单词或词组进行识别。定位题目指向关键句所在的段落，并输出该段落、题干和选项内容，分别写入 "originalParagraph"、"questionStem"和"options"。询问用户是否认识原文段落、题干及所有选项中的所有单词和词组。如有陌生单词/词组，请用户进行标记。本步骤输出对应的原文段落+题干+所有选项中可能出现的所有陌生单词和词组，写入"unfamiliarWords"，以及对应的词义讲解，并将该单词/词组的知识点写入"knowledgeTag"。注意：用户中包含英语基础非常薄弱的同学，因此单词难度一定要考虑到该类同学的词汇水平；注意选项中也可能出现关键词汇。注意，首字母大写的专有名词（如人名、地名等）不影响理解的，不用标注。

# 需要注意的单词知识点标签如下：
├── 1.词汇
│   ├── 1.1 词义理解
│   │   ├── 中低频词
│   │   ├── 多义词
│   │   └── 纯专业词汇
│   └── 1.2 固定搭配
│       ├── 动词短语
│       ├── 介词搭配
│       └── 特殊习语与惯用语

以下是需要分析的考研阅读真题内容：
{input_data_str}

请按照以下标准格式输出（最终仅输出标记后结果的json格式即可）：
{{
  "passageAnalysis": {{
    "textNumber": "文章序号",
    "passage": "原文"
  }},
  "questionAnalyses": [
    {{
      "questionNumber": 1,
      "analysisSteps": {{
        "step1_vocabularyIdentification": {{
          "originalParagraph": "原文段落",
          "questionStem": "题干",
          "options": ["选项A", "选项B", "选项C", "选项D"],
          "unfamiliarWords": [
            {{
              "word": "单词1",
              "meaning": "释义1",
              "knowledgeTag": "1.1 词义理解 - 纯词汇"
            }},
            {{
              "word": "单词2",
              "meaning": "释义2",
              "knowledgeTag": "1.2 固定搭配 - 动词短语"
            }}
          ]
        }}
      }}
    }}
  ]
}}
    """
    
    # 调用API
    api_response = call_api(prompt)
    if not api_response:
        return
    
    # 保存输出文件
    save_output_file(api_response, output_file)

if __name__ == "__main__":
    main() 