import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # make 2 empty sets
        self.positives = set()
        self.negatives = set()

        # populate positives set
        with open(positives) as lines:
            for line in lines:
                if not line.startswith(";") and not line.startswith('\n'):
                    self.positives.add(line.strip())

        # populate negative set
        with open(negatives) as lines:
            for line in lines:
                if not line.startswith(";") and not line.startswith('\n'):
                    self.negatives.add(line.strip())

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        # split text into list of words
        tokenizer = nltk.tokenize.TweetTokenizer()
        words = tokenizer.tokenize(text)

        # use str.lower() to make each word lowercase
        words = [word.lower() for word in words]

        score = 0

        # for each word in words...
        for word in words:
            if word in self.positives:
                score += 1
            elif word in self.negatives:
                score -= 2

        return score