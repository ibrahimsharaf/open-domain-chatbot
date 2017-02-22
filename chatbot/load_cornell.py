"""
Load the cornell movie dialog corpus
For more info on dataset's structure, check readme file inside cornell
http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html
"""
import re

class LoadCornell:
    """
    Load cornell movie conversations in the correct order
    """
    def __init__(self, directory):
        """
        :param directory: dataset directory
        """
        # dict with the lines id as key, line utterance as value
        self.lines = {}
        # list of dicts, each one holds related lines
        self.conversations= []

        line_fields = ['lineID','characterID', 'movieID', 'character_name', 'text']
        conv_fields = ['character1ID', 'character2ID', 'movieID', 'linesID']

        self.lines = self.load_lines(directory+"movie_lines.txt", line_fields)
        self.conversations = self.load_conversations(directory+"movie_conversations.txt", conv_fields)

    def load_lines(self, filename, fields):
        """
        Populate lines dictionary
        :param filename: lines file
        :param fields: list of fields names
        :return: Dict of line id with each utterance
        """

        lines = {}
        with open(filename, 'r') as f:
            for each_line in f:
                line_vals = each_line.split('+++$+++')
                line_vals[0] = line_vals[0][:-1]
                line_meta = {}
                for i in range(len(line_vals)):
                    line_meta[fields[i]] = line_vals[i]
                #print line_meta['lineID'] + " " + line_meta['text']
                lines[line_meta['lineID']] = line_meta['text']
                #print lines[line_meta['lineID']]

        #for debugging
        #for key, value in lines.iteritems():
        #   print key + value
        return lines

    def load_conversations(self, filename, fields):
        """
        Get ordered conversation lines
        :param filename: conv file
        :param fields: list of fields names
        :return: list of lists, contains related coversation lines
        """
        conversations = []
        with open(filename, 'r') as f:
            for each_line in f:
                line_vals = each_line.split('+++$+++')
                conv_meta = {}
                for i in range(len(line_vals)):
                    conv_meta[fields[i]] = line_vals[i]

                conv_lines = (re.findall(r"'(.*?)'", conv_meta['linesID'], re.DOTALL))
                #print conv_lines
                one_conv = []
                for i in range(len(conv_lines)):
                    one_conv.append(self.lines[conv_lines[i]])
                conversations.append(one_conv)

        #for debugging
        #for i in range(30):
        #   for j in range(len(conversations[i])):
        #       print conversations[i][j]

        return conversations

    def get_conversations(self):
        return self.conversations