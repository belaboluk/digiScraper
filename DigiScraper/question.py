from .seller import Seller
from .utils import getIfExists

class QuestionCollection():
    def __init__(self, product, internet) -> None:
        """
        download nd manage the questions
        """
        self.__internet = internet
        self._product = product
        self.totalQuestoins = 0
        self.totalPages = 0
        self.questionsCount = 0
        self.questions = []


    def _addQuestions(self, data:list):
        self.questionsCount += len(data)
        for q in data:
            self.questions.append(Question(q))

    
    def getQuestionPage(self, page) -> None:
        """
        download and save a page of questions
        alse updating total question cound and total pages
        """
        data = self.__internet.getQuestions(self._product.id, page)
        self.totalPages = data["pager"]["total_pages"]
        self.totalQuestoins = data["pager"]["total_items"]
        self._addQuestions(data["questions"])
    

    def toCSV(self, path=None):
        if path and path[-4:] != ".csv":
            path = path + ".csv"
        if not path:
            path = "questions.csv"
        
        with open(path, "w", encoding="utf8") as f:
            f.write(f"id,sender,text,date,answers count,answers\n")
            for item in self.questions:
                f.write(f"\"{item.id}\",\"{item.sender}\",\"{item.text}\",\"{item.date}\",\"{item.answerCount}\",\"")
                for ans in item.answers:
                    f.write(f"{ans.text}\n")
                f.write("\"\n")


class Question():
    def __init__(self, data) -> None:
        """
        class for saving a question and all answer to it
        """
        self.id = data["id"]
        self.sender = data["sender"]
        self.text = data["text"]
        self.answerCount = data["answer_count"]
        self.date = data["created_at"]
        self.answers = []
        for i in range(self.answerCount):
            self.answers.append(Answer(data["answers"][i]))


class Answer():
    def __init__(self, data:dict) -> None:
        """
        answer of a question with all infos
        """
        self.id = data["id"]
        self.sender = getIfExists(data, "sender")
        self.text = data["text"]
        self.likes = data["reactions"]["likes"]
        self.dislikes = data["reactions"]["dislikes"]
        self.date = data["created_at"]
        self.type = data["type"]

        if self.isSeller():
            self.seller = Seller(data["seller"])


    def isSeller(self) -> bool:
        """
        is this answer submeted from a seller or not (buyer)
        """
        return True if self.type == "seller" else False
