import nltk

class Analyzer():
    """ Topic analyzer"""
    def __init__(self, related, differentTopic, keywords):
        """related should be words related to the topic, differentTopic, words that change the topic"""
        # make empty sets
        self.related = set()
        self.differentTopic = set()
        self.keywords = set()

        # populate related set
        with open(related) as lines:
            for line in lines:
                if not line.startswith(";") and not line.startswith('\n'):
                    self.related.add(line.strip())

        # populate differentTopic set
        with open(differentTopic) as lines:
            for line in lines:
                if not line.startswith(";") and not line.startswith('\n'):
                    self.differentTopic.add(line.strip())
                    
        # populate keywords set
        with open(keywords) as lines:
            for line in lines:
                if not line.startswith(";") and not line.startswith('\n'):
                    self.keywords.add(line.strip())

    def analyze(self, text):
        """Analyze text for a certain topic, returning its score."""

        # split text into list of words
        tokenizer = nltk.tokenize.TweetTokenizer()
        words = tokenizer.tokenize(text)

        # use str.lower() to make each word lowercase
        words = [word.lower() for word in words]

        score = 0

        # for each word in words...
        for word in words:
            if word in self.keywords:
                score += 2
            elif word in self.related:
                score += 1
            elif word in self.differentTopic:
                score -= 6

        return score