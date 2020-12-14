from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractor import MasterExtractor

# don`t forget to start up core_nlp_host
# giveme5w1h-corenlp


class Text5W1H(object):
    """
    A Text5W1H object is an object that uses the 5W1H class to get
    info from text.

    Don't forget to run `giveme5w1h-corenlp` on command line before calling
    this class.

    Example Usage:
    ```
    text = ".. .." # put your text here
    answers = Text5W1H(text)

    who = answers.who()
    print(who) # outputs the best answer to "who" given the text
    ```
    """

    def __init__(self, text):
        self.text = text
        extractor = MasterExtractor()
        doc = Document.from_text(self.text)
        self.doc = extractor.parse(doc)
        self.answers = doc.get_answers()

    def get_text(self):
        return self.text

    def get_doc(self):
        return self.doc

    def get_answers(self):
        return self.answers

    def who(self):
        """ 
        Returns: The top answer to the question, None if no answers exist.
        """
        who = self.answers['who']
        return self._get_top_answer('who') if len(who) else None

    def what(self):
        """ 
        Returns: The top answer to the question, None if no answers exist.
        """
        what = self.answers['what']
        return self._get_top_answer('what') if len(what) else None

    def when(self):
        """ 
        Returns: The top answer to the question, None if no answers exist.
        """
        when = self.answers['when']
        return self._get_top_answer('when') if len(when) else None

    def where(self):
        """ 
        Returns: The top answer to the question, None if no answers exist.
        """
        where = self.answers['where']
        return self._get_top_answer('where') if len(where) else None

    def why(self):
        """ 
        Returns: The top answer to the question, None if no answers exist.
        """
        why = self.answers['why']
        return self._get_top_answer('why') if len(why) else None

    def how(self):
        """ 
        Returns: The top answer to the question, None if no answers exist.
        """
        how = self.answers['how']
        return self._get_top_answer('how') if len(how) else None

    def what_index(self):
        """
        Returns: the index for the what question in a given sentence.
        """
        try:
            what = self.doc.get_top_answer('what')
            return what.get_parts_character_offset()
        except IndexError:
            return None

    def who_index(self):
        """
        Returns: the index for the what question in a given sentence.
        """
        try:
            what = self.doc.get_top_answer('who')
            return what.get_parts_character_offset()
        except IndexError:
            return None

    def where_index(self):
        """
        Returns: the index for the what question in a given sentence.
        """
        try:
            what = self.doc.get_top_answer('where')
            return what.get_parts_character_offset()
        except IndexError:
            return None

    def _get_top_answer(self, question):
        return self.doc.get_top_answer(question).get_parts_as_text()
