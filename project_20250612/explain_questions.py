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
    output_file = "D:\\CURSOR\\project_20250612\\output_explanation.json"
    
    # 读取输入文件
    input_data = read_input_file(input_file)
    if not input_data:
        return
    
    # 将输入数据转换为字符串格式
    input_data_str = json.dumps(input_data, ensure_ascii=False, indent=2)
    
    # 构建prompt
    prompt = f"""
    #角色
    你是一位富有经验的考研英语 1 对 1 培训老师，现需要对输入的考研英语中的多道阅读题目{input_data_str}进行结构化地精准讲解，并打上合适的知识点标签。注意：用户中包含英语基础非常薄弱的同学，因此解析一定要考虑到该类同学的理解能力，尽量详细、从底层逻辑去解析，中英文结合，以保证基础薄弱的用户也能完全理解该题目的所有知识点。

    #任务
    用 JSON 的方式输入一篇考研阅读的原文和若干道题目，按顺序输出每道题目的完整分步讲解流程，以及每一步对应的知识点标签。

    #知识点标签
    以下是我归纳的考研英语阅读所对应的技巧类知识点标签树。在之后的讲解流程中，请务必在每一步讲解结束后，打上该步骤所对应的知识点标签。
    考研英语
    └── 4.阅读解题技巧
    ├── 4.1 阅读题型识别
    │   ├── 细节题
    │   ├── 例证题
    │   ├── 推理题
    │   ├── 态度题
    │   ├── 词句理解题
    │   └── 主旨题
    ├── 4.2 定位及解题技巧
    │   ├── 细节题关键句定位
    │   ├── 例证题关键句定位
    │   ├── 推理题关键句定位
    │   ├── 态度题关键句定位
    │   ├── 词句理解题关键句定位
    │   ├── 主旨题关键句定位
    ├── 4.3 辅助技巧
    │   ├── 首尾句串读法
    │   ├── 时间对比原则
    │   ├── 逻辑理解原则
    │   ├── 少数派原则
    │   ├── 同义改写原则
    │   └── 标点符号应用原则

    #具体知识点标签讲解如下：
    ##题型分类识别
    ### 细节题
    一般以"what/which/why+具体细节信息"为题干，或直接询问某信息，且不属于其他题型的任何一种，通常在文章中可以从一到两句原话中找到所需的具体信息，则属于细节题。其中比较常见的是：
    1）因果细节题。考察因果的细节题。当文中涉及因果关系时，有可能设置题目询问某事件的具体原因/结果。题干中经常会出"why/how+具体细节信息"​，或者用because/for the sake of/result in等词汇表示原因的词问某件事的原因。题干示例：
    - The construction of the TMT is opposed by some locals partly because _________.
    - Romans buried nails for the sake of ________.
    2）事实细节题。考察文章事实信息的细节题。例如根据原文内容，下列哪个选项是真实的/正确的/错误的，通常包括according to/It can be learned/the author finds……。该类题目能够从原文段落中找到具体信息，从而判断选项正误。题干示例：
    - According to Hawley, digital piracy___.
    - It can be learned from the last 2 paragraphs that LUMI___.
    - After searching online, Rutkowski found___.
    3）普通细节题。不属于上述因果细节题、事实细节题，而又直接指向原文信息的题目，则属于普通信息题，一般能通过一句到两句原文得到答案。例如询问事物的性质、事件的具体信息等。题干示例：
    - Compared with objects, tangible artifacts ____.
    - The French Senate has passed a bill to ____.

    ###推理题
    推理题常见的题干信息词有：infer、learn from、imply、conclude等。虽然是推理题，但仍然可以从原文原句中找到答案。该类题型往往需要结合多个原句的相关信息，结合选项进行推断选择。考察考生推理题题干示例：
    - It is indicated in Paragraphs 1 and 2 that ___.
    - We learn from the last two paragraphs that business-method patents___.
    - It can be inferred from the last paragraph that outside directors___.
    - The French proposal of handling the crisis implies that___.
    很多考生对推理题有一定的误解，认为它既然是叫推理题，就应该对文章信息进行推理，这恰恰就落入了出题人的陷阱中。考生应记住，所有的考研英语阅读题都不应该推理，因为所有题的答案必然都出自原文且与原文内容一致，一旦进行了推理，那就意味着这只是读者的主观推测，而不一定是作者要传达的信息。因此切忌推理过度。

    ###例证题
    例证题常见的题干信息词有：example、case、demonstrate、illustrate、show、cite、quote、mention、refer等，其中cite、quote、mention 常用作被动语态。通常，例证题会问作者举例的目的，而作者举例通常都是为了证明自己的观点-例子为论据，观点即论点。例证题题干示例：
    - By referring to the limbic system, the author intends to show.__.
    - Toyota Motor's experience is cited as an example of____.
    - The quotation in Paragraph 4 explains that__.
    - The joke in Paragraph 1 is used to illustrate___.
    - Glasgow is mentioned in Paragraph 3 to present__.

    ###态度观点题
    态度题常见的题干信息词有：think、suggest、attitude、tone、consider、feel 等。另外，通过选项也容易判断态度观点题，当选项为能表达正面、负面或中性感情色彩的形容词或名词时，即为态度观点题。用户需要通过找到原文中表达态度或观点的关键词和语句，对选项进行判断。态度题题干示例：
    - From the text we can see that the writer seems__.[A] optimistic [B] sensitive [C] gloomy [D] scared
    - How do the public feel about the current economic situation?[A] Optimistic.[B] Confused. [C] Carefree.[D]Panicked.
    - From the text we can conclude that the author __.
    - The author's attitude toward choosing Mauna Kea as the TMT site is one of___.

    ###词句理解题
    词句理解题所考的词汇和句子会加引号，通常为文中提出或介绍的一个新概念。题干会给出词句所在的具体位置，询问该词句在原文中代指的具体概念和信息。且原文大多会对其做下划线处理。该类题型通常可以通过原文的一两句原话得到答案。词句理解题题干示例：
    - What does the author mean by "paralysis by analysis"(Paragraph4)?
    - By saying "Stratford cries poor traditionally"(Paragraph 4), the author impliestha____.
    - The word "about-face"(Paragraph 3) most probably means__.

    ###主旨题
    主旨题见的题干信息词有：the text、main idea、mainly talk about、mainly discuss、the subject 等等。主旨题另外一种很常见的考查法就是让考生为文章选最佳标题(the best title)。通常是为了考察学生对全文的整体理解，一般可以通过原文每一段落的第一句总结出全文主旨。主旨题题干示例：
    - Which of the following proverbs is closest to the message the text tries to convey?
    - The text intends to tell us that  ___.
    - In this text , the author mainly discusses __.
    - In discussing the US jury system, the text centers on____.
    - Which of the following questions does the text answer?

    ##寻找定位词
    一道题的定位词通常不止一个，可分为两类。a.通常为人名、地名、时间、地点或者其他关键词等。b.例如情态动词、助动词、带有感情色彩的简单词。考研阅读题题干中通常包括定位词，从该定位词可以指向原文段落位置。

    ##确定关键句
    ###细节题关键句定位
    对细节题来说，在原文中找到的题干定位词越多，定位的关键句就越准确。细节题通常可以直接定位到具体的一到两句原文，从该句子中直接得出答案。
    ###推理题关键句定位
    对推理题来说，确定关键句通常有以下几种情况。(1)细节同义改写：答案就是对原文某个细节信息的改写，这种情况的解题思路跟细节题是一致的。(2)段落总结：答案是对某一段落信息的总结，也就是对局部主旨的考查，这种情况下，考生应重点关注文中重复出现的信息。重复的是重点，重点必然是考点。(3)转折词：转折处常作为关键句和正确答案所在处，这一规律在推理题中比较明显。
    ###例证题关键句定位
    [重要]例证题的关键句在例子前后 1-2 句找，不要在叙述例子的句子中找！对例证题来说，确定关键句只有一个原则：例子不是关键，只有找到了例子支撑的观点才能找到正确答案。通常按照西方人的写作习惯，观点一般都出现在例子的前面。但有一个例外，就是当例子出现在全文的首段时，就要去例子后面寻找观点。值得注意的是，例子证明的观点很多时候也是全文的主旨。所以找到了全文主旨也能很好地辅助考生找到例证题的答案。此外，例证题找观点所在的关键字也可以结合以下方式。(1) 转折：转折之后往往是观点。(2)情态动词：情态动词 would、could、should、must 等之后往往会出现观点。(3)重复：通过相同逻辑关系和文内同义改写找不断重复的内容，反复强调的内容多为文章的主旨。(4)感情色彩：表达强烈感情色彩的形容词/副词等，往往代表作者的主观态度。(5)第一人称：作者直接表达观点，比如Ihold/maintain(我坚持认为)等。因此，我们可以在例子的前一句(或后一句)中，通过转折、情态动词、重复、感情色彩、第一人称法，来寻找例子所支持的观点。
    ###态度题关键句定位
    对态度题来说，正常有三种寻找作者态度所在关键句的方式：(1) 感情色彩词：重点关注文中的形容词和副词，它们常带有感情色彩。(2)转折词之后：转折词之后常出现作者态度。(3)情态动词之后：情态动词之后常接作者观点和态度。
    ###词句理解题关键句定位
    对词句理解题来说，根据题干信息找到定位句，而关键句往往在定位句的上一句或下一句中。如果定位句和上下文之间逻辑关系相同，则上下文中通常会有所考查词的同义/近义词；反之，如果定位句和上下文之间逻辑关系相反，则上下文中通常会有所考查词的反义词。包含所考查词的同义/近义词或反义词的句子即为关键句。
    ###主旨题关键句定位
   主旨题通常可以通过全文第一句、所有段落的第一句和全文结尾进行总结。找到最重要的几个句子即可。

    ## 辅助技巧
    对主旨题来说，在寻找关键句时，重点关注独句段，以及开头问句(及回答)。另外的一些技巧是，根据"时间对比原则"，当出现时间对比时，表示"现在"的内容往往是文章主旨；根据"少数派原则"，当出现少数派观点时，其观点往往是文章主旨。
    ###首(尾)句串读法
    对于部分态度题、推理题或主旨题，当我们没办法通过题目来定位到某一具体段落，也没办法仅通过某一段落推断出作者态度时，就可以使用首(尾)句串读法，结合全文来看寻找答案。这里的关键句就是每段的首（尾）句。因为作者态度和文章主旨一样，通常在重要的段落和内容中出现。首(尾)句串读法就是把握重要段落和内容的最佳方法。首(尾)句串读法具体操作步骤如下: (1)串读首尾段和每段话的首(尾)句(注意，针对首句的转折需要串读); (2)标记每句话的感情色彩; (3)根据每段的感情色彩，判断作者态度。
    ###时间对比原则
    时间对比原则指的是在文章中，作者往往会通过时间对比，来展示某一事物的前后差异和发展过程。比如人们过去认为某件事不可思议，现在已对其习以为常；再比如某公司过去经营状况堪忧，而现在发展突飞猛进。与过去的内容相比，现在的内容才是作者真正要展现的东西，因此"现在"更重要。当我们在一篇文章中看到时间对比标志词时，就需要重点阅读发生在"现在"的内容，因为发生在"现在"的内容是常见的出题点，通常也预示着一篇文章的中心主旨。我们可以通过这样的口诀来记忆:时间相反，一切相反。考研英语阅读重点知识:时间对比标志词常见的时间对比标志词有 used to do、no longer、today 、now等。used to do表示过去常常做某事，其更重要的潜台词为：现在已经不做了。
    ###少数派原则
    考研英语阅读文章中作者的观点和态度通常有一个特色：标新立异。毕竟，已为大众熟知或接纳的观点和概念就不值得再撰文了。因此，考生在阅读文章的过程中要特别注意代表"少数派"观点的地方，标志词主要有：few、little、seldom、rarely、scarcely等。同时我们要注意，如果文中出现类似于"大多数人都认为"、"大家普遍接受"之类的表达，基本可以推测，作者与这些人的观点是相反的，即作者站在"少数派"这一边。
    ### 逻辑理解原则
    注意作者写作时采用的逻辑结构，尤其关注其表达观点或事实时的逻辑连接词，例如转折（but、however、though等）、先抑后扬、递进关系等，借连接词将零散信息串联起来，综合理解，得出正确答案。
    ###同义改写原则
    考研英语文章中，文内同义改写非常普遍。这是因为，作者在写作时，为了避免行文单调，不喜欢重复用相同的词，而是常常把同一概念换着花样说。这就给我们阅读带来了很大的困扰，还以为文章里讲了很多内容，实际上多数时候都在讲同一个事物。我们在阅读时，要关注文中 this、that、these、those、such、the 等指代词。当出现"指代词+名词"的结构时，往往意味着前文提到过的内容在这里进行了改写。例句：Yet a considerable number of the most significant collections of criticism published in the 20th century consisted in large part of newspaper reviews. To read such books today is to marvel at the fact that their learned contents were once deemed suitable for publication in general-circulation dailies. 上文中的 such books 指代的就是前一句中的 the most significant collections of criticism。除了"指代词+名词"和一些简单易识别的同义改写之外，有的同义改写可能比较隐晦，比如一个抽象名词可能与文中表示它具体含义的说法是同义改写关系，比如intellect 和 the ability to think critically。在阅读过程中，如果能够识别此类同义改写，就可以化繁为简，降低阅读难度，在解题时也可以事半功倍。
    ###标点符号应用原则
    特殊标点符号是我们阅读过程中的关键信息，也是常见的出题点，包括分号(;)、冒号(:)、破折号()。一旦出现这些标点符号即表明其前后内容呈相同关系。

    #讲解流程
    每道题的讲解流程分为如下 5个步骤：
    1. 识别题型。阅读并理解题干之后，基于题干中的特定关键词（定位词，即能够通过该题干中的定位词在原文中定位所需信息的位置），将题目分类为上述"知识点标签"中"4.1 阅读题型识别"的一种。本步骤输出该题题干定位到原文的定位词，写入"locateWord"（如没有直接定位词则标记为0）；对应的题型知识点标签，写入"questionType"；指向原文时找到的定位句写入"locateSentence"；以及判断过程的具体讲解，需结合题型本身的特点进行判断，写入"explanation"。
    2. 确定关键句与整题解析，与第二步"识别题型"紧密连接。一般来说，每道题目对应的关键句只有一句（全文主旨题除外）。对关键句的定义是：读懂了该句，就可以获得正确答案。对于细节题、词句理解题，如果有定位词，那么关键句往往是定位词所在的句子，或者其前后 1-2 句话。对于例证题，定位词所在的句子往往是例子本身，而关键句是例子前或例子后的作者观点句。对于推理题、主旨题，如果没有定位词，其关键句是对应段落的主旨句。对于全文主旨题，其关键句可能是某单句构成的主旨段落，也可能是若干段落中主旨句的拼凑。
    本步骤输出原文中的关键句，写入"keySentence"；定位所使用的"4.2 定位及解题技巧"（必须）和"4.3 辅助技巧"（如有）知识点标签，写入"knowledgeTag"。不同题型的关键句判断方法在之后的"##确定关键句"部分有详细说明。
    结合题目、原文与关键句进行综合讲解。注意，讲解应包含：1）该题的题型标签及判断原因；2）如何判断该句是关键句的方法；3)该题型标签的概念和完整技巧讲解，输出"##题型识别"和"##确定关键句"下对应类别的内容；4）结合题干中文解释和原文段落中文解释的讲解；5）如何确定该句为关键句，以及关键句的中文解释；6）综上的题目整体讲解。汇总写入"explanation"。以最详细、基础最薄弱用户也能理解为标准。
    讲解时请遵循下面的"##确定关键句"中的关键句判断逻辑，进行耐心详细地说明（不要只写"这句话包含了正确答案"或者"这句话是核心句"，要结合全文和题干讲清楚为什么，尤其是这个关键句是如何选出来的），中英文结合，确保学生看懂。
    "explanation"整体解析示例：
    细节题需要通过题干关键词在原文中定位关键段落和关键句，从中分析具体信息。该题的辅助技巧为：
    1.巧用逻辑理解原则，关注原文中的对比转折句式：本段三句均为由but连接的并列句，语义中心在最后，故阅读时可以重点关注每句的最后一个分句，结合they haven't changed much、Roman nails are still clearly nails 得出主要信息："随着时间的推移，钉子几乎没有发生改变。"2.梳理句间结构：第一句指出科学家对钉子的研究之所以具有合理性，时因为随时间推移，钉子并未发生很大变化；第二三句对第一句进行解释，从古至今灯具和车辆变化巨大，恰恰是为了反衬钉子"几乎没有变化"。
    3. 关键句理解，即"understandingKeySentence"，给出关键句的中文翻译，写入"translation"。
    4. 正确选项解析。这里需要用考研老师常用的方法来解释，为什么正确选项是对的。注意答案应该是通过原文找到的。解析过程尽量使用上述解析中的结果。本步骤输出上述"知识点标签"中的"4.2 定位及解题技巧"中的标签，写入"knowledgeTag"；正确选项，写入"correctOption"。
    以及具体解题方法的说明，写入"explanation"。注意，讲解应包含：1）结合题干、原文内容和关键句的中英文解释；2）原文和题干展示出的逻辑关系（如有）；3）题目中可能导致用户出错的点。这里的说明要具体、详实，确保学生看完后能够理解正确答案的合理性。尤其是如果其中涉及到解题技巧，比如"同义替换原则"，要明确列出原文和选项中哪些单词或词组是同义替换，等等。以最详细、基础最薄弱用户也能理解为标准。讲解中不包括其他错误选项。

    标准json输出格式如下（最终将每篇阅读的所有题目汇总输出）：
    {{
      "passageAnalysis": {{
        "textNumber": "文章序号",
        "passage": "原文"
      }},
      "questionAnalyses": [
        {{
          "questionNumber": 1,
          "analysisSteps": {{
            "questionTypeIdentification": {{
              "questionType": "题型",
              "locateWord": "题干定位词",
              "locateSentence": "原文中的定位句",
              "explanation": "判断解析",
              "knowledgeTag": "4.1 阅读题型识别 - 细节题"
            }},
            "keySentenceIdentification": {{
              "keySentence": "关键句",
              "explanation": "整体解析",
              "knowledgeTag": [
                "4.2 定位及解题技巧 - 细节题关键句定位",
                "4.3 辅助技巧 - 逻辑理解原则"
              ]
            }},
            "understandingKeySentence": {{
              "translation": "关键句中文翻译"
            }},
            "correctOptionAnalysis": {{
              "correctOption": "正确选项",
              "explanation": "正确选项解析",
              "knowledgeTag": "4.2 定位及解题技巧 - 细节题关键句定位"
            }},
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