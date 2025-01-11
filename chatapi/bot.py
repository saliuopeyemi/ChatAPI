import re
from trainer import train,quick_train
import long_responses as long
import json
from threading import Thread


with open("misc.json","r") as file:
	responses = json.load(file)

exiter = ["close","quit","end",""]

train_pattern = '".*"'

stopwords = ["", "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can","can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "", "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "","something","anything","nothing","how","is","are","who","what","where","when","why","can","could","would","can", "could","do","don't", "may", "might", "should", "would", "must", "ought to", "am", "was", "have", "need", "dare", "shall", "will", "am", "was", "were", "been", "being", "has", "have", "had", "do","does","did","ca","wo","be","hello","hi","hey","what's up","!","howdy","g'day","sup","hiya","heya","good","hola","salut","aye","bye","goodbye","adios","bye-bye","bye bye", "good bye","cheerio","ciao","have a nice day","have a nice time","ta-ta","ta ta","adios","adieu","hasta la vista","hasta-la-vista","am","are","can","can","could","did","do","does","is","had","has","hasn't","have","haven't","may","might","should","was","were","will","would","ca","wo","hello","hi","hey","what's up","!","howdy","g'day","sup","hiya","heya","good","hola","salut","aye","bye","goodbye","adios","bye-bye","bye bye", "good bye","cheerio","ciao","have a nice day","have a nice time","ta-ta","ta ta","adios","adieu","hasta la vista","hasta-la-vista","n't","tell","say","explain","describe","itemize","know","mean","meaning","means","word","?","!",".","tell","say","describe","write","define","definition","wa"]

punctuations = ["!","?"]


class Chatbot():
	def __init__(self):
		self.learn_status = False
		self.training = False

	def message_probability(self,user_message,recognized_words,single_response=0,required_words=[]):
		message_certainty = 0
		has_required_words= True

		for word in user_message:
			if word in recognized_words:
				message_certainty += 1

		percentage = float(message_certainty)/float(len(recognized_words))

		for word in required_words:
			if word not in user_message:
				has_required_words = False
				break

		if has_required_words == True or single_response != 0:
			return int(percentage*100)
		elif has_required_words == False:
			return int(percentage*50)
		else:
			return int(percentage*20)


	def check_all_messages(self,message):
		highest_prob_list = {}

		def response(bot_response, list_of_words, single_response=False, required_words=[]):
			nonlocal highest_prob_list
			highest_prob_list[bot_response] = self.message_probability(message,list_of_words,single_response,required_words)

		for item in responses:
			response(item,responses[item]["identifier"],required_words=responses[item]["required_words"],single_response=responses[item]["single_response"])


		best_match = max(highest_prob_list, key=highest_prob_list.get)


		sorted_prob_list =  dict(sorted(highest_prob_list.items(), key=lambda item: item[1], reverse=True))
		value_range = (1,100)
		reply_list = [key for key, value in sorted_prob_list.items() if value >= value_range[0] and value <= value_range[1]]
		# print(sorted_prob_list)
		

		if highest_prob_list[best_match] == 0:
			return long.unknown()
		elif highest_prob_list[best_match] > 0 and highest_prob_list[best_match] < 30:
			if best_match != "action1":
				with open("convo_history.json","w") as file:
					json.dump(best_match,file)
				with open("history.json","w") as file:
					json.dump(reply_list,file)
				answer = best_match
				unsure_phrase = long.unsure()
				return f"{unsure_phrase}{answer}"
			else:
				with open("convo_history.json","r") as file:
					last_reply = json.load(file)
				with open("history.json","r") as file:
					last_convo = json.load(file)
				reply_index = last_convo.index(last_reply) +1
				if reply_index <= len(last_convo)-1:
					answer = last_convo[reply_index]
					with open("convo_history.json","w") as file:
						json.dump(answer,file)
					return answer
				else:
					return long.info_end()
		else:
			if best_match != "action1":
				with open("convo_history.json","w") as file:
					json.dump(best_match,file)
				with open("history.json","w") as file:
					json.dump(reply_list,file)
				return best_match
			else:
				with open("convo_history.json","r") as file:
					last_reply = json.load(file)
				with open("history.json","r") as file:
					last_convo = json.load(file)
				reply_index = last_convo.index(last_reply) +1
				if reply_index <= len(last_convo)-1:
					answer = last_convo[reply_index]
					with open("convo_history.json","w") as file:
						json.dump(answer,file)
					return answer
				else:
					return long.info_end()




	def get_response(self,user_input):
		split_sentence = re.split(r"\s+|[,;:?!.-_]\s*", user_input.lower())
		try:
			split_sentence.remove("")
		except:
			pass
		response = self.check_all_messages(split_sentence)
		return response

	def reply(self,statement):
		user_initial = statement
		if self.learn_status == False and self.training == False:
			learn = re.findall(train_pattern,user_initial)
			if len(learn) != 0:
				clean_data = learn[0].replace('"',"")
				with open("learning.json","w") as file:
					json.dump(clean_data,file)
				self.learn_status = True
				return long.learning_prompt()

			else:
				if user_initial.lower() in exiter:
					pass
				else:
					for item in punctuations:
						user_initial = user_initial.strip(item)
					user = user_initial.split(" ")
					result = []
					for word in user:
						if word.lower() not in stopwords:
							result.append(word)
					if len(result) > 0:
						user = " ".join(result)
						return f"{self.get_response(user)}"
					else:
						return f"{self.get_response(user_initial)}"

		elif self.learn_status == True and self.training == True:
			print(long.learning_progress())
		else:
			with open("learning.json","r") as file:
				data = json.load(file)
				self.training = True
			def process():
				train(user_initial,data)
				self.learn_status = False
				self.training = False
			funct = Thread(target=process)
			funct.start()

	def calculate_relationship(self,message,sentence2):
		quick_train(sentence2.lower(),sentence2.lower())
		highest_prob_list = {}

		def response(bot_response, list_of_words, single_response=False, required_words=[]):
			nonlocal highest_prob_list
			highest_prob_list[bot_response] = self.relationship_probability(message.lower(),list_of_words,single_response,required_words)
		with open("temp.json","r") as file:
			determiner = json.load(file)

			response(sentence2,determiner[sentence2]["identifier"],required_words=determiner[sentence2]["required_words"],single_response=determiner[sentence2]["single_response"])
		with open("temp.json","w") as file:
			json.dump({},file)
		return highest_prob_list

	def relationship_probability(self,user_message,recognized_words,single_response=0,required_words=[]):
		message_certainty = 0
		has_required_words= True

		for word in user_message:
			if word in recognized_words:
				message_certainty += 1

		percentage = float(message_certainty)/float(len(recognized_words))

		for word in required_words:
			if word not in user_message:
				has_required_words = False
				break

		if has_required_words == True or single_response != 0:
			return int(percentage*100)
		else:
			return int(percentage*100)/2

# for item in responses:
# 		response(item,responses[item]["identifier"],required_words=responses[item]["required_words"],single_response=responses[item]["single_response"])
	

	# def run():
	# 	while True:
	# 		you = input("YOU: ")
	# 		print(reply(you))

	# run()
# bot = Chatbot()

# while True:
# 	you = input("YOU: ")
# 	if you != "":
# 		print(bot.reply(you))
# 	else:
# 		break