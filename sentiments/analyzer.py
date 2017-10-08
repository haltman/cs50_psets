import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positives = positives
        self.negatives = negatives

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        self.text = text
        self.positives = list()
        self.negatives = list()
        score = 0
        i = 0

        # instantiate tokenizer with tweet
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        if tokens == None:
            exit(1)

        # port valid positive words from input file to output file
        with open("positive-words.txt") as pLines:
            for line in pLines:
                if line.startswith(";") or line.startswith(" ") or not line.strip():
                    continue
                else:
                    self.positives.append(line.strip())

        # port valid negative words from input file to output file
        with open("negative-words.txt") as nLines:
            for line in nLines:
                if line.startswith(";") or line.startswith(" ") or not line.strip():
                    continue
                else:
                    self.negatives.append(line.strip())

        # add to total score for each positive word in tweet
        for pos in self.positives:
            for tk in tokens:
                if tokens[i].lower() == pos:
                    score += 1
                i += 1
            i = 0

        # subtract from total score for each negative word in tweet
        for neg in self.negatives:
            for tk in tokens:
                if tokens[i].lower() == neg:
                    score -= 1
                i += 1
            i = 0

        return score
