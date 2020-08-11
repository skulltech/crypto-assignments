import string
import numpy as np
from sympy import Matrix
from hill import encrypt, chars
import itertools


CSTHRESH = 150


def chisquared(txt):
	expected = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
	expected = [x * len(txt) for x in expected]
	given = [0] * 26
	for c in txt:
		given[chars.index(c)] += 1

	cs = 0
	for i in range(26):
		cs = cs + (((given[i] - expected[i]) ** 2) / expected[i])
	return cs


def crack(cipher, bsize):
	words = cipher.split(' ')
	lenwords = [len(word) for word in words]
	cipher = ''.join(words)
	if len(cipher) % bsize:
		cipher = cipher.ljust(((len(cipher) // bsize) + 1) * bsize, 'a')

	rows = []
	for row in itertools.product(range(0, 26), repeat=bsize):
		plain = ''
		for j in range(len(cipher) // bsize):
			block = cipher[j*bsize : (j+1)*bsize]
			q = np.array([chars.index(char) for char in block]).T
			plain = plain + chars[int(np.mod(np.array(row) @ q, 26))]
		
		cs = chisquared(plain)
		if cs < CSTHRESH:
			rows.append(row)

	for matrix in itertools.permutations(rows, bsize):
		key = np.array(matrix)
		plain = ''
		for j in range(len(cipher) // bsize):
			block = cipher[j*bsize : (j+1)*bsize]
			q = np.array([chars.index(char) for char in block]).T
			dec = np.mod(key @ q, 26)
			plain = plain + ''.join([chars[int(i)] for i in dec])

		cs = chisquared(plain)
		if cs < CSTHRESH:
			ret = ''
			for lw in lenwords:
				ret = ret + plain[:lw] + ' '
				plain = plain[lw:]
			print(key)
			print(cs)
			print(ret)


plaintext1 = 'a very large number of published documents contain text only they often look boring and they are often written in obscure language using milelong sentences and cryptic technical terms using one font only perhaps even without headings such style or lack of style might be the one you are strongly expected to follow when writing eg scientific or technical reports legal documents or administrative papers it is natural to think that such documents would benefit from a few illustrative images however just adding illustration might be rather useless if the text remains obscure and unstructured it is too easy to go to the other extreme when trying to avoid the boring plain text syndrome this is especially true on the web where it is relatively easy technically to add illustration for instance by picking images from various existing collections many people seem to think that you cant have too many images if they cant find a suitable image they use an unsuitable one when people say that one image tells more than a thousand words they tend to overlook the fact that what the image says might be true or false relevant or offtopic useful or disturbing constructive or tasteless i wont bother to refute the saying by pointing out that there are images which say nothing however i cannot resist the temptation to remark that oddly enough the saying itself is expressed using words'
plaintext2 = 'while eating at a restaurant is an enjoyable and convenient occasional treat most individuals and families prepare their meals at home to make breakfast lunch and dinner daily these persons must have the required foods and ingredients on hand and ready to go foods and ingredients are typically purchased from a grocery store or an establishment that distributes foods drinks household products and other items thatre used by the typical consumer'
plaintext3 = 'once upon a time there were three little pigs who left their mummy and daddy to see the world all summer long they roamed through the woods and over the plainsplaying games and having fun none were happier than the three little pigs and they easily made friends with everyone wherever they went they were given a warm welcome but as summer drew to a close they realized that folk were drifting back to their usual jobs and preparing for winter autumn came and it began to rain the three little pigs started to feel they needed a real home sadly they knew that the fun was over now and they must set to work like the others or theyd be left in the cold and rain with no roof over their heads they talked about what to do but each decided for himself the laziest little pig said hed build a straw hut it wlll only take a day he said the others disagreed its too fragile they said disapprovingly but he refused to listen not quite so lazy the second little pig went in search of planks of seasoned wood clunk clunk clunk it took him two days to nail them together but the third little pig did not like the wooden house thats not the way to build a house he said it takes time patience and hard work to buiid a house that is strong enough to stand up to wind rain and snow and most of all protect us from the wolf the days went by and the wisest little pigs house took shape brick by brick from time to time his brothers visited him saying with a chuckle why are you working so hard why dont you come and play but the stubborn bricklayer pig just said no i shall finish my house first it must be solid and sturdy and then ill come and play he said i shall not be foolish like you for he who laughs last laughs longest it was the wisest little pig that found the tracks of a big wolf in the neighbourhood the little pigs rushed home in alarm along came the wolf scowling fiercely at the laziest pigs straw hut come out ordered the wolf his mouth watering i want to speak to you id rather stay where i am replied the little pig in a tiny voice ill make you come out growled the wolf angrily and puffing out his chest he took a very deep breath then he blew wlth all his might right onto the house and all the straw the silly pig had heaped against some thin poles fell down in the great blast excited by his own cleverness the wolf did not notice that the little pig had slithered out from underneath the heap of straw and was dashing towards his brothers wooden house when he realized that the little pig was escaping the wolf grew wild with rage come back he roared trying to catch the pig as he ran into the wooden house the other little pig greeted his brother shaking like a leaf i hope this house wont fall down lets lean against the door so he cant break in outside the wolf could hear the little pigs words starving as he was at the idea of a twocourse meal he rained blows on the door open up open up i only want to speak to you inside the two brothers wept in fear and did their best to hold the door fast against the blows then the furious wolf braced himself a new effort he drew in a really enormous breath and went whooooo the wooden house collapsed like a pack of cards luckily the wisest little pig had been watching the scene from the window of his own brick house and he rapidly opened the door to his fleeing brothers and not a moment too soon for the wolf was already hammering furiously on the door this time the wolf had grave doubts this house had a much more solid air than the others he blew once he blew again and then for a third time but all was in vain for the house did not budge an lnch the three little pigs watched him and their fear began to fade quite exhausted by his efforts the wolf decided to try one of his tricks he scrambled up a nearby ladder on to the roof to have a look at the chimney however the wisest little pig had seen thls ploy and he quickly said quick light the fire with his long legs thrust down the chimney the wolf was not sure if he should slide down the black hole it wouldntbe easy to get in but the sound of the little pigs voices below only made him feel hungrier im dying of hunger im goin to try and get down and he let himself drop but landing was rather hot too hot the wolf landed in the fire stunned by his fall the flames licked his hairy coat and his tail became a flaring torch never again never again will i go down a chimneyl he squealed as he tried to put out the flames in his tail then he ran away as fast as he could the three happy little pigs dancing round and round the yard began to sing tralala tralala the wicked black wolf will never come back from that terrible day on the wisest little pigs brothers set to work with a will in less than no time up went the two new brick houses the wolf did return once to roam in the neighbourhood but when he caught sight of three chimneys he remembered the terrible pain of a burnt tail and he left for good now safe and happy the wisest little pig called to his brothers no more work come on lets go and play'
plaintext4 = 'speaking of dreams in a figurative sense then slowly talking about its impact in the literal sense thewriter keeps stressing on one very important point that dreams have an important role to play inamerican politics after all a liberal society is formed on the basis of ones imagination these imaginationsare a result of ones free thoughts which can be related to dreams as dreaming provides a picture of thereal world uncovering things which otherwise might not have been pondered upon due to narrowed andlimited freedom of imagining it may seem reckless to consider the possibility of turning to dreams towork through the political conditions today but ignoring them altogether might even be more recklesssays the author'


plaintext = plaintext4
k = np.array([[10, 6, 11], [19, 13, 8], [12, 11, 16]])
ciphertext = encrypt(plaintext, k)
crack(ciphertext, 3)
