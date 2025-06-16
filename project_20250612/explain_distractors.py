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
        "model": "anthropic/claude-sonnet-4",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        print("✅ API调用成功")
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"❌ API调用失败: {str(e)}")
        return None

def save_output_file(data, output_path):
    """保存输出文件"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ 成功保存输出文件")
        return True
    except Exception as e:
        print(f"❌ 保存输出文件失败: {str(e)}")
        return False

def main():
    # 设置文件路径
    input_file = "D:\\CURSOR\\project_20250612\\input_text_1_2024.json"
    output_file = "D:\\CURSOR\\project_20250612\\output_distractors.json"
    
    # 读取输入文件
    input_data = read_input_file(input_file)
    if not input_data:
        return
    
    # 将输入数据转换为字符串
    input_data_str = json.dumps(input_data, ensure_ascii=False, indent=2)
    
    # 构建prompt
    prompt = f"""
    #角色
    你是一位富有经验的考研英语 1 对 1 培训老师，我需要你帮我一起探索如何使用在线 App 来对考研英语中的阅读题目进行结构化地精准讲解，并打上合适的知识点标签。现需要对已经包含正确答案解析的阅读题进行干扰项的详细讲解。
    注意：用户中包含英语基础非常薄弱的同学，因此解析一定要考虑到该类同学的理解能力，尽量详细、从底层逻辑去解析，中英文结合，以保证基础薄弱的用户也能完全理解该题目的所有知识点。

    #任务
    用 JSON 格式输入一篇考研阅读的原文和若干道题目，按顺序输出每道题目的完整分步讲解流程，以及每一步对应的知识点标签。

    #知识点标签
    以下是我归纳的考研英语阅读中干扰项所对应的技巧类知识点标签树。在之后的讲解流程中，请务必在每一步讲解结束后，打上该步骤所对应的知识点标签。
    └── 4.3 干扰项识别
        ├── 绝对化用词
        ├── 反向干扰
        ├── 偷换概念
        ├── 过度推理
        ├── 无中生有
        ├── 信息歪曲
        ├── 信息拼凑
        ├── 以偏概全
        ├── 范围太大
        ├── 一词多义干扰（词句理解题）
        ├── 望文生义（词句理解题）
        ├── 形近干扰（词句理解题）
        ├── 墓碑选项（作者态度题）
        └── 讨论例子本身（例证题）

    其中各个标签的解析如下：
    ##干扰选项解析
    ###绝对化用词
    除非文章中明确提到过，否则出现only、must、exclusively、never、all这样绝对化词汇的选项通常都是错误选项，需要加以警惕。比如某道题问文章第一、第二段表明了什么。A选项说"arts criticism has disappeared from big-city newspapers"(大城市的报纸上已经看不到艺术评论了)，其中的disappear这个词太绝对化了，文中只提到艺术报道的衰落(decline)，二者不是一个概念。

    ###反向干扰
    反向干扰命题人会编出语义或者情感态度与原文相反的选项，来测试考生理解的准确性。比如题目问为什么森林大火会成为国家问题。第二段句子提到用于林务局其他工作(如基础设施维护)的联邦拨款现在已经减少了(fewer federal funds today are going towards the agency'sother work--such as ... infrastructure upkeep)，也就是说基础设施方面的支出减少了，C选项却说更加频繁的森林大火"导致基础设施支出大幅增加"​，与原文正好相反，属于反向干扰。另外，如果文章主旨遵循"少数派原则"，在设置选项时常常会编一个与"少数派"相反的观点，用"符合常识"的选项来误导考生。这也是为什么当选项内容出现"两两相反"的情况时，其中通常有一个为正确答案。

    ###偷换概念
    偷换概念的选项将原文中行为的施动者，或主语、宾语等进行偷换，以此迷惑考生。比如某道题的题干问原文中"任何消费都变得极其不合时宜"这句话是什么意思。根据原文，这指的是"在艺术品上花钱"这种行为变得不合时宜，D选项却将其解读为"艺术品普遍已经过时，所以不值得购买"​，偷换了主语，是典型的偷换概念。
    比较级概念偷换是干扰选项设计的重要思路，面对这样的选项，要谨记：除非原文中有明确的比较，否则慎选。比如某道题的题干问哪一项"增加了攻读法律的费用"​，选项A说"更高的本科学费"。首先原文只提到攻读法律的费用(costs)，而没有提及tuitionfees(学费)。其次higher是一个比较级的概念，而原文虽然强调了费用高，但从未说本科学费更高，更没有将其与其他费用相比，此处属于比较级概念的偷换。

    ###过度推理
    考研英语阅读中，正确选项必然是能在原文中找到依据的。之所以有"过度推理"这种选项，正是命题人利用了考生喜欢"路见不平，拔刀相助"这种心理。命题人根据原文信息，做了一种貌似合理的推理，让考生掉入陷阱。实际上，做题时一定要注意，正确选项拒绝推理，要"有一说一"。比如某道阅读题目，考生需要选本文的最佳标题。原文只是说中产阶级家庭有财务风险，A选项却说本文的最佳标题是"时刻警惕的中产阶级"​，这是出题人站在考生的角度，在原文基础上做了一步貌似合理的推理一有风险，要警惕。但实际上原文中并未提及"要警惕"这一信息，该选项是典型的过度推理。

    ###无中生有
    无中生有也是细节题干扰选项很常见的设计思路。命题人从原文部分信息出发，编出一些貌似正确但原文没有提及的信息构成选项，对考生进行干扰。比如某道题目问本文的最佳标题是什么，C选项说的是"冲突之下的中产阶级"​，但原文中只是说中产阶级家庭有财务风险，并没有提到中产阶级家庭的冲突，因此该选项属于无中生有，是命题人编造的内容。想要排除此类选项，只需要回到原文进行对比，如果发现原文中根本没有出现该选项的信息，那么该选项就是错误的。

    ###信息拼凑
    信息拼凑，就是从原文不同的句子中截取碎片信息进行胡乱拼凑，拼凑后的意思完全不符合原文。比如2011年英语(二)阅读Text1的一道题，题目问外部董事突然离职后，公司有可能怎么样，原文第三段句⑤说的是"公司在联邦集体诉讼中被点名的可能性也有所增加，而且公司股票也有可能表现更差"(The likelihood ofbeing named in a federal class-action lawsuit also increases, and the stock is likely toperform worse)，D选项却将这句话逗号前后的lawsuit和perform worse两个细节信息拼凑在一起，说公司有可能"在诉讼中表现更差"​，属于典型的信息拼凑。

    ###信息歪曲
    信息歪曲，就是从原文中截取部分碎片信息，故意对其进行歪曲，造成看似和原文很像，但实际上意思已经发生改变的情况。比如2014年英语(一)阅读Text2的一道题，其中一个选项将原文的costs of a legal education改写为tuitionfees(学费)，但tuition fees并不等同于costs(费用)，costs的概念更加广泛，这里属于故意歪曲部分信息以迷惑考生。

    ###以偏概全
    这是最常见的主旨题干扰选项。命题人通常会用仅在文章某一段或者某两段中出现的细节信息来设置干扰，这样的选项以偏概全，无法充当文章的主旨。

    ###范围扩大
    有的干扰选项会扩大文章的主题范围，比如2010年英语(一)阅读Text1的主旨题中，文章只是在讨论关于"报纸衰落"的话题，选项却将文章主题扩大到整个"新闻业"。

    ###望文生义（词句理解题）
    用考查词或句的字面含义进行干扰。

    ###一词多义干扰（词句理解题）
    所考词非常简单，但文中出现的是它熟词僻义的用法，而干扰选项往往与它较为常见的含义相关。

    ###形近干扰（词句理解题）
    用与画线词形近的词来进行干扰。

    ###墓碑选项（作者态度题）
    主要包括以下 3 类态度：(1) 不感兴趣类，例如uninterested、unconcerned、indifferent 等；(2)不知所措类，例如 confused、puzzled 等；(3) 主观偏激类：subjective、biased、prejudice、contemptuous 等；(4) 容忍类：tolerant、indulgent 等。如果作者写文章的目的是把一个问题客观分析清楚，上述态度都是不合适的。

    ###讨论例子本身（例证题）
    例证题最常见的干扰信息就是讨论例子本身。因为例子本身的信息不是举例的目的。所以例证题定位好的句子不仅不是答案，反而是设计干扰选项的常见位置。只要掌握了这一点，在面对例证题时，我们就可以快速排除那些利用例子细节信息来设置干扰的选项，从而缩小选择范围。

    解析步骤：
    对每个干扰项进行详细讲解，包括：1）结合原文内容理解，解释该项错因；2）该项属于哪个类型的干扰项（参考上述知识点标签）；3）学生识别该类干扰项时应注意的问题和技巧，结合本题和原文的中英文进行综合讲解。

    最终输出格式：
    {{
      "passageAnalysis": {{
        "textNumber": "文章序号",
        "passage": "原文"
      }},
      "questionAnalyses": [
        {{
          "questionNumber": 1,
          "analysisSteps": {{
            "distractorAnalysis": {{
              "distractors": [
                {{
                  "option": "干扰选项1",
                  "explanation": "干扰原因解析",
                  "knowledgeTag": "4.3 干扰项识别 - 无中生有"
                }}
              ]
            }}
          }}
        }}
      ]
    }}

    请确保分析详细、准确，并给出具体的例子和解释。
    """
    
    # 调用API
    result = call_api(prompt)
    if not result:
        return
    
    # 解析API返回的JSON字符串
    try:
        output_data = json.loads(result)
    except json.JSONDecodeError as e:
        print(f"❌ 解析API返回结果失败: {str(e)}")
        return
    
    # 保存输出文件
    save_output_file(output_data, output_file)

if __name__ == "__main__":
    main() 