import App.util.SparkApi as SparkApi


class ChatBot:
    def __init__(self, appid, api_key, api_secret, Spark_url, domain):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.Spark_url = Spark_url
        self.domain = domain
        self.text = []  # 存储对话历史

    def getText(self, role, content):
        """ 将用户输入或模型输出添加到对话历史 """
        jsoncon = {"role": role, "content": content}
        self.text.append(jsoncon)

    def getlength(self):
        """ 获取对话历史的总长度 """
        length = sum(len(content["content"]) for content in self.text)
        return length

    def checklen(self):
        """ 如果对话历史长度超过8000，则删除最早的对话 """
        while self.getlength() > 8000:
            del self.text[0]

    def ask_question(self, question):
        """ 发送用户问题并获取模型回答 """
        self.getText("user", question)  # 记录用户提问
        self.checklen()  # 确保历史记录不会超长

        SparkApi.answer = ""  # 清空上一轮的答案

        # 调用 SparkApi 进行 WebSocket 通信
        SparkApi.main(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, self.text)

        # 获取模型的回答并记录
        answer = SparkApi.answer
        self.getText("assistant", answer)  # 记录模型回答

        return answer


