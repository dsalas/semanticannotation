import urllib.request as urllib
import re
import pickle

def scrap_yanuq():
    #scrapping and encoding/decoding to utf-8
    s1_url = 'https://www.yanuq.com/recetasperuanasp.asp#Carn'
    s1_request = urllib.Request(s1_url, headers={'User-Agent': 'Mozilla/57.0'})
    s1_webpage = urllib.urlopen(s1_request).read()
    s1_htmltext = s1_webpage.decode('latin-1')
    s1_htmltext = (s1_htmltext.encode("utf-8")).decode('utf-8')
    s1_strips = re.findall('buscador\.asp\?idreceta.*?>(.*?)<', s1_htmltext, flags=re.S)
    #preprocessing some dishes 
    s1_strips = [s.replace('N° 1', '') for s in s1_strips]
    s1_strips = [s.replace('N° 2', '') for s in s1_strips]
    s1_strips = [s.replace('No. 1', '') for s in s1_strips]
    s1_strips = [s.replace('No. 2', '') for s in s1_strips]
    s1_strips = [s.replace('No.1', '') for s in s1_strips]
    s1_strips = [s.replace('No.2', '') for s in s1_strips]
    s1_strips = [s.replace('al estilo Yanuq', '') for s in s1_strips]
    s1_strips = [s.replace(u'\xa0', u'') for s in s1_strips]  # Eliminar caracter latin-1 \xa0 de items
    s1_strips = [s.replace(u'\x93A', u'') for s in s1_strips]
    s1_strips = [s.replace(u'\x93', u'') for s in s1_strips]
    s1_strips = [s.replace(u'\x94', u'') for s in s1_strips]
    s1_strips = [s.lower() for s in s1_strips]
    s1_strips = [s.strip() for s in s1_strips]
    #print log of urls scrapped
    print(s1_url)
    return s1_strips

def scrap_enjoyperu():
    # scrapping and encoding/decoding to utf-8
    s2_list_url = []
    s2_strips_accum = []
    s2_list_url.append('http://www.enjoyperu.com/recetas/entradas.htm')
    s2_list_url.append('http://www.enjoyperu.com/recetas/sopas-y-cremas.htm')
    s2_list_url.append('http://www.enjoyperu.com/recetas/pescados-y-mariscos.htm')
    s2_list_url.append('http://www.enjoyperu.com/recetas/comida-china.htm')
    s2_list_url.append('http://www.enjoyperu.com/recetas/comida-de-la-selva.htm')
    s2_list_url.append('http://www.enjoyperu.com/recetas/postres.htm')
    s2_list_url.append('http://www.enjoyperu.com/recetas/platos-de-fondo.htm')  # !!!!!

    for url in s2_list_url:
        s2_request = urllib.urlopen(url)
        s2_webpage = s2_request.read()
        s2_htmltext = s2_webpage.decode('ISO-8859-1')
        s2_htmltext = (s2_htmltext.encode("utf-8")).decode('utf-8')
        s2_strips = re.findall('recetasindfond.*?enjoyperu\.com\/recetas.*?>(.*?)<', s2_htmltext, flags=re.S)
        s2_strips_accum = s2_strips_accum + s2_strips
        s2_nextsubpag = re.findall('enjoyperu\.com\/recetas\/.*images\/recetas\/flechsiguiente', s2_htmltext, flags=re.S)
        if len(s2_nextsubpag) > 0:
            nexturl = re.findall(
                '(http:\/\/www\.enjoyperu\.com\/recetas\/(?!.*http:\/\/www\.enjoyperu\.com\/recetas\/).*)\">',
                s2_nextsubpag[0], flags=re.S)
            s2_list_url.append(nexturl[0])
        # print log of urls scrapped
        print(url)
    # preprocessing
    s2_strips_accum = [s.lower() for s in s2_strips_accum]
    s2_strips_accum = [s.strip() for s in s2_strips_accum]
    return s2_strips_accum
          
def scrap_cocinaperu():
    # scrapping and decoding to utf-8
    s3_list_url = []
    s3_strips_accum = []
    s3_list_url.append('http://www.cocinaperu.com/recetas-peruanas/recetas-entradas/')
    s3_list_url.append('http://www.cocinaperu.com/recetas-peruanas/recetas-sopas/')
    s3_list_url.append('http://www.cocinaperu.com/recetas-peruanas/chupes/')
    s3_list_url.append('http://www.cocinaperu.com/recetas-peruanas/recetas-postres/')
    s3_list_url.append('http://www.cocinaperu.com/recetas-peruanas/platos-de-fondo/')

    for url in s3_list_url:
        s3_request = urllib.urlopen(url)
        s3_webpage = s3_request.read()
        s3_htmltext = s3_webpage.decode('utf-8')
        s3_strips = re.findall('<li><a href\=\"http\:\/\/www\.cocinaperu\.com\/recetas-peruanas\/.*?>(.*?)<',
                               s3_htmltext, flags=re.S)
        s3_strips.pop(0)  # Eliminar titulo de la categoría
        s3_strips = [s.replace("Receta ", "") for s in s3_strips]  # Eliminar prefijo de algunos items
        s3_strips_accum = s3_strips_accum + s3_strips
        # print log of urls scrapped
        print(url)
    # preprocessing
    s3_strips_accum = [s.lower() for s in s3_strips_accum]
    s3_strips_accum = [s.strip() for s in s3_strips_accum]
    return s3_strips_accum

def scrap_wikipedia():
    # scrapping and encoding/decoding to utf-8
    s4_url = 'https://en.wikipedia.org/wiki/List_of_Peruvian_dishes'
    s4_request = urllib.urlopen(s4_url)
    s4_webpage = s4_request.read()
    s4_htmltext = s4_webpage.decode('utf-8')
    s4_strips = re.findall('<li><a href="\/w\/index\.php\?title.*?>(.+?)<', s4_htmltext, flags=re.S)
    # preprocessing
    s4_strips = [s.lower() for s in s4_strips]
    s4_strips = [s.strip() for s in s4_strips]
    # print log of urls scrapped
    print(s4_url)
    return s4_strips

def delete_stop_words(strips):
    with open('stopwordsES.txt','r') as f:
        stopwords = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    stopwords = [x.strip() for x in stopwords]
    aux_strips = []
    flg_stwd = 0
    word_erase = []
    for food in strips:
        for word in food.split():
            if word in stopwords:
                food.replace(" ","")
                flg_stwd = 1
                word_erase.append(word)
        if flg_stwd != 1:
            aux_strips.append(food)
        else:
            n_food = food
            for w in word_erase:
                #n_food = n_food.replace(w,"")
                n_food = re.sub(r"\b%s\b" % w, "", n_food)
            aux_strips.append(n_food)

    n_strips = []
    for strip in aux_strips:
        n_strips.append(re.sub(' +',' ',strip))
    print(n_strips)
    return n_strips

def scrap_peruvian_food():
    #scrap 4 sources of peruvian food and drinks
    s1_strips = scrap_yanuq()
    s2_strips = scrap_enjoyperu()
    s3_strips = scrap_cocinaperu()
    s4_strips = scrap_wikipedia()
    #combine and index the list
    all_strips = s3_strips + s4_strips + s2_strips + s1_strips
    all_strips.sort()
    all_strips = list(set(all_strips))
    # delete stop words
    all_strips = delete_stop_words(all_strips)
    #save peruvian dishes and drinks corpus
    perfydcorpus = open('perfydcorpus.txt', 'wb')
    pickle.dump(all_strips, perfydcorpus)
    perfydcorpus.close()
    print("Número de platos y bebidas extraídos: " + str(len(all_strips)))

def find_peruvian_dish_drink(tips):
    perfydcorpus = open('perfydcorpus.txt', 'rb')
    corpus = pickle.load(perfydcorpus)
    corpus.sort()
    output = {}
    for tip in tips:
        output[tip] = []
        for bigram in tips[tip]:
            flg = False
            s_word = ''
            for word in bigram:
                s_word = s_word + " " + word
            n_word = s_word.lower()
            if n_word.strip() in corpus:
                flg = True
            output[tip].append(flg)
    perfydcorpus.close()
    return output

"""
Prueba
tips  = {
        "v1": [
            [
                "Un",
                "buen"
            ],
            [
                "pollo",
                "brasa"
            ],

        ],
        "v2": [
            [
                "aji",
                "gallina"
            ],
            [
                "grande",
                "todo"
            ],

        ]
        }
print(find_peruvian_dish_drink(tips))
"""



