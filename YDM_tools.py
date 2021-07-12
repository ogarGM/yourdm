import random
import re
import itertools   
import xlrd

#loadup dictionary 
wb2 = xlrd.open_workbook(u'words.xls')
wb3 = xlrd.open_workbook(u'word_maker.xls')

shPlaces = wb2.sheet_by_name(u'NamedPlace')
shLOSTEMP = wb2.sheet_by_name(u'lostEmpire')
shNumber = wb2.sheet_by_name(u'Numbers')
shMobAtk = wb2.sheet_by_name(u'MobsVerbs')
shKings = wb2.sheet_by_name(u'kings')
shAdvice = wb2.sheet_by_name(u'Advice')
shAdjecs = wb2.sheet_by_name(u'adjective')
shDrinks = wb2.sheet_by_name(u'drink')
shFREQ = wb2.sheet_by_name(u'letFreq')
shCOMP = wb2.sheet_by_name(u'testComp')
shBOOK = wb2.sheet_by_name(u'booky')
shBITS = wb2.sheet_by_name(u'bits')

shWORDMAKER = wb3.sheet_by_name(u'langCaesar')

def pick_random(prob_list):
    #takes a list of tuples, index followed by probability (out of one)
    #and returns the index or something
    r, s = random.random(), 0
    for num in prob_list:
        s += num[1]
        if s >= r:
            return num[0]
    print("Error WHAT:", file=sys.stderr)
    
def PickAdjPhrase(numCol):
    strOut = ""
    if numCol == 0:    #if no adjectives needed break out
        #print "woah 0"
        pass
    else:            #pick columns randomly!#
        listColn = range(1, 3)
        listAdjCol = random.sample(listColn,numCol)#dont pick same column twice
        #pick one adj from each selected column
        for k in sorted(listAdjCol):
            adj_list = list(filter(None, shAdjecs.col_values(k-1,1)))
            iAdj = random.randint(0,len(adj_list)-1)
            strAdj = adj_list[iAdj]
    #slam them into one adjective string
            strOut = strOut + " " + strAdj
    return strOut

def SimplePicker(sheet, column):
    #Pick a random element from the specified sheet and coloumn
    col_list = list(filter(None, sheet.col_values(column,1)))
    strOut = col_list[random.randint(0,len(col_list)-1)]
    return strOut

def PickRandomMob():
    ### MONSTER PICKER ###
    #pick monster category#
    iMobType = random.randint(0,2)
    #pick monster#
    #mob_list = filter(None, shMobAtk.col_values(iMobType,1))
    mob_list = list(filter(None, shMobAtk.col_values(iMobType,1)))
    iMob = random.randint(0,len(mob_list)-1)
    strOut = mob_list[iMob]
    return strOut

def PickAnimalMob():
    strOut = SimplePicker(shMobAtk,0)
    return strOut
    
def PickSuperMob():
    strOut = SimplePicker(shMobAtk,1)
    return strOut
    
def PickHumanoidMob():
    strOut = SimplePicker(shMobAtk,2)
    return strOut
    
def VowConMatch(letterList,matchstr):
    #takes a composition template and returns a random string
    #matching that composition
    strVowels = "aeiouy"
    strConsos = "bcdfghjklmnpqrstvwxz"
    strLetterToMatch = str(pick_random(letterList)).lower()
    k = 1
    while k <= 1:
        if matchstr != 'v' and matchstr != 'c':
            strLetter = matchstr
            return strLetter
            k = 6
        elif strLetterToMatch in strVowels and matchstr == 'v':
            strLetter = strLetterToMatch
            return strLetter
            k = 6
        elif strLetterToMatch in strConsos and matchstr == 'c':
            strLetter = strLetterToMatch
            return strLetter
            k = 6
        else:
            strLetterToMatch = str(pick_random(letterList)).lower()
                
def buildRule( pattern, search, replace ): 
    #enables Pluralizer() and similar to apply a list of regular expressions
    #to a string via map()
    return lambda word: re.search(pattern, word, flags=re.I) and re.sub(search, replace, word, flags=re.I)
    
def Pluralizer(strIn):
    #pluralizes input string
    if strIn.lower() == 'brain in a jar':
        return 'brains in jars'
    
    strTail = ''.join([x for x in re.split(r'( of +)',strIn)[1:]])    #cut off tail of strings when they are like <thing> of <thing>
    strIn  = re.split(r'( of +)',strIn)[0]                            #the first word <thing> of <thing> strings
    patterns = \
    (
    ('folk$', '' , '' ),                    #folk    
    ('(?<!h)ouse$','ouse$','ice'),        #mice and houses
    ('(?<!hu)man(?!\w)',r'an\b','en'),    #men,women,mantises,humans
    ('[\w\D]us$','us$','i'),            #octopi,cacti
    ('[sxz]$', '$', 'es'),                #horcruxes, mantises
    ('[^aeioudgkprt]h$', '$', 'es'),    #attaches
    ('(qu|[^aeiou])y$', 'y$', 'ies'),    #harpies
    ('[(?<=oo)(?<=f)]f$', '$','s'),        #roofs,hoofs
    ('[\w\D]f$','f$', 'ves'),            #elves, dwarves
    ('$', '$', 's')                    #everything else??
    )
    #ruleList = map(buildRule, list(patterns))
    ruleList = list(itertools.starmap(buildRule, patterns))

    for rule in ruleList:
        strOut = rule(strIn)
        if strOut: return strOut + strTail
    
def Verber(strIn):
    #turns a verb into a verber
    #for use in flavor names
    #like walrusstabber or orclicker
    
    #strTail = ''.join([x for x in re.split(r'( +)',strIn)[1:]])    #cut off tail of strings when they are like <verb> at
    strIn = re.split(r'( +)',strIn)[0]#[:-1]                        #the first word <verb> at strings
    
    patterns = \
    (
    #(r'ea[t]$|ou[t]$','$','er'),
    (r'[aeiou]t$','$','ter'),
    #(r'[aeiou]p$','$','per'),
    #(r'[aeiou]b$','$','ber'),
    #(r'bber$|tter$','$','er'),
    #(r'[s|p]t$|[p|s]p$', '$','er'),    
    #(r't$|p$|b$', '$', 'er'),
    (r'e$', '$', 'r'),
    #(r'h$','$','er'),
    ('$', '$', 'er'),                    #everything else??
    )
    #ruleList = map(buildRule, patterns)
    ruleList = list(itertools.starmap(buildRule, patterns))
    for rule in ruleList:
        strOut = rule(strIn)
        if strOut: return strOut# + strTail
        
def Verbed(strIn):
    #turns a verb into a verbed
    #for use in flavor names
    #like walrusstabbed or orclicked
    
    strTail = ''.join([x for x in re.split(r'( +)',strIn)[1:]])    #cut off tail of strings when they are like <verb> at
    strIn = re.split(r'( +)',strIn)[0][:-1]                        #the first word <verb> at strings
    
    patterns = \
    (
    (r'ea[t]$|ou[t]$','$','ed'),
    (r'[aeiou]t$','$','ted'),
    (r'[aeiou]p$','$','ped'),
    (r'[aeiou]b$','$','bed'),
    (r'bber$|tter$','$','ed'),
    (r'[s|p]t$|[p|s]p$', '$','ed'),    
    (r't$|p$|b$', '$', 'ed'),
    (r'e$', '$', 'd'),
    (r'h$','$','ed'),
    ('$', '$', 'ed'),                    #everything else??
    )
    #ruleList = map(buildRule, patterns)
    ruleList = list(itertools.starmap(buildRule, patterns))
    for rule in ruleList:
        strOut = rule(strIn)
        if strOut: return strOut# + strTail
        
def Verbing(strIn):
    #turns a verb into a verbing
    
    strTail = ''.join([x for x in re.split(r'( +)',strIn)[1:]])    #cut off tail of strings when they are like <verb> at
    strIn = re.split(r'( +)',strIn)[0]                        #the first word <verb> at strings
    
    patterns = \
    (
    (r'ea[t]$|ou[t]$','$','ing'),
    (r'[aeiou]t$','$','ting'),
    (r'[aeiou]p$','$','ping'),
    (r'[aeiou]b$','$','bing'),
    ('$', '$', 'ing'),                    #everything else??
    )
    #ruleList = map(buildRule, patterns)
    ruleList = list(itertools.starmap(buildRule, patterns))
    for rule in ruleList:
        strOut = rule(strIn)
        if strOut: return strOut + strTail
        
#################################################
# adds a random diacritical mark to each letter #
# depending on probability                        #
# WILL RETURN ERRORS IF YOU TRY TO PRINT THIS     #
# STRING TO SCREEN TERMINAL. FUCK                #
#################################################
def FlavorLetter(oNam, prob=0.1):
        flavNam = ""
        possComb = [u'\u0300',u'\u0301',u'\u0302',u'\u0303',u'\u0308',u'\u0311',u'\u0327']
        for l in oNam:
            newLet = l
            if not re.search("[_\d\W]",l) and random.random() < prob:
                #fuck with letter
                try:
                    conMark = l+random.choice(possComb)
                    #newLet = unicodedata.normalize("NFKC",unicode(conMark))
                    newLet = unicodedata.normalize("NFKC",conMark)

                    #print newLet, ",len= ",len(newLet)
                    
                    #windows console cant print this shit 
                    # but if above line uncommented it can
                    #for some fucking reason ????
                    unicodedata.normalize("NFKC",conMark)
                    
                except Exception:
                    newLet = l
                    #pass

            flavNam=''.join([flavNam,newLet])

        return flavNam
        
def RandomProperNoun():
    #Creates a random name
    # shFREQ = wb2.sheet_by_name(u'letFreq')
    # shCOMP = wb2.sheet_by_name(u'testComp')

    list1 = []
    alfa = list(filter(None, shFREQ.col_values(0,1)))
    for i in range(1,shFREQ.ncols):
        col_list = list(filter(None, shFREQ.col_values(i,1)))

        for j in range(1,len(col_list)+1):
            #print shFREQ.cell_value(j,i)
            list1.append((alfa[j-1],shFREQ.cell_value(j,i)))

    ######GET GENDER TAG#####
    iType = random.randint(0,2)    

    ######GENERATE DISTRIBUTION LISTS#####
    distFirs = []
    for i in range(26*(iType+4),26*(iType+5)):
        #print list1[0+i]
        distFirs.append((list1[0+i]))
        
    distLets = []
    for i in range((26*iType),26*(iType+1)):
        #print list1[0+i]
        distLets.append((list1[0+i]))

    ######GET FIRST LETTER#####
    comp_list = list(filter(None, shCOMP.col_values(iType,1)))
    iComp = random.randint(0,len(comp_list)-1)
    strForm = comp_list[iComp].lower()

    strVowels = "aeiouy"
    strConsos = "bcdfghjklmnpqrstvwxz"

    strFirstLetter = VowConMatch(distLets,strForm[0])

    strOut = ''
    for let in range(1, len(strForm)):
        strNewLet = VowConMatch(distLets,strForm[let])
        strOut = strOut+strNewLet

    strOut = strFirstLetter + strOut    

    #print strForm.upper()

    return strOut.title()
    
def FlavorfulProperNoun():
    strVerb = SimplePicker(shMobAtk,4).strip().lower()
    
    strVerber = Verber(strVerb)
    
    iMobType = random.randint(0,1)
    strRanMob = SimplePicker(shMobAtk, iMobType)
    
    object_list = []
    #object_list.extend(filter(None, shMobAtk.col_values(0,1)))
    #object_list.extend(filter(None, shMobAtk.col_values(1,1)))
    #object_list.extend(filter(None, shMobAtk.col_values(2,1)))
    object_list.extend(list(filter(None, shPlaces.col_values(4,1))))
    object_list.extend(list(filter(None, shPlaces.col_values(5,1))))
    
    # k = 1
    # while k==1:
        # if ' ' in strRanMob.strip():
            # strRanMob = SimplePicker(shMobs, iMobType)
        # else:
            # k = 2
        
    strRanObject = random.choice(object_list)

    strOut = strRanObject.title() + '-' + strVerber.title()

    #strOut = strRanMob.title() +'-' + strVerber.lower()
    return strOut
    
def ExitString():
    #random string of exit letters
    exit_tuples = [(1,'N'),(2,'E'),(3,'S'),(4,'W')]
    exit_list = random.sample(exit_tuples,random.randint(0,4))
    strOut = ','.join([item[1] for item in sorted(exit_list)])
    return strOut
    
def DoWeAddPhrase(strIn, strAdd, prob=1, max_let=220):
    #can we add the two given strings
    #also maybe we dont even if we can
    if (random.random() < prob) and (len(strIn) + len(strAdd)) < max_let:
        strOut = strIn + strAdd
        return strOut
    else:
        return strIn
        
def AnAFixer(strIn):
    strVowel = 'aeiouAEIOU'
    
    k = 1
    while k == 1:
        if strIn.strip() != "":
            if strIn.lower().strip() == 'belly of the beast':
                #strOut = 'The %s' % (strIn.strip())
                strOut = ' '.join(['The', strIn.strip()])
                k = 2
            elif 'yggdrasil' in strIn.lower():
                strOut = strIn.strip()
            elif strIn[0].strip() in strVowel:
                strOut = ' '.join(['An', strIn.strip()])
                #strOut = 'An %s' % (strIn.strip())
                k =2 
            else:
                strOut = ' '.join(['A', strIn.strip()])
                #strOut = 'A %s' % (strIn.strip())
                k =2
        else:
            #print 'errpr'
            strOut = 'A %s' % (strIn.strip())
            k = 2
        
    return strOut.title()

def SomeAffixer(strIn):
    strOut = ' '.join(['some',strIn.strip()])
    
def RollDice(numDice,sizeDice):
    diceTotal = 0
    k = 0
    while k < numDice:
        diceTotal += random.randint(1,sizeDice)
        k += 1
    return diceTotal

def NumberNamer():
    sPlur = SimplePicker(shNumber,0)
    sSingle = SimplePicker(shNumber,1)
    sTens = SimplePicker(shNumber,2)
    sBigNum = SimplePicker(shNumber,3)
    
    sSmaOrd = SimplePicker(shNumber,4)
    sBigOrd = re.sub(r'y$','ieth',sTens)
    
    numOpt = \
            (
            ( [sPlur, .100] ),        #twin
            ( [sSingle, .400] ),        #three
            ( [sTens, .250] ),        #forty
            ( [sBigNum, .020] ),        #million
            ( [sSmaOrd, .090] ),        #first
            ( [sBigOrd, .080] ),        #seventieth
            ( [' '.join([sSingle,'hundred']), .040]),            #one hundred
            ( [' '.join([sSingle,'hundred',sBigNum]), .010]),    #two hundred million
            ( [' '.join([sSingle,sBigNum]), .007]),        #four billion
            ( [' '.join([sTens,sBigNum]), .003]),        #twenty billion
            )
            
    return pick_random(    numOpt )
    
def int_to_en(num):
    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert(0 <= num)

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + '-' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred and ' + int_to_en(num % 100)

    if (num < m):
        if num % k == 0: return int_to_en(num // k) + ' thousand'
        else: return int_to_en(num // k) + ' thousand, ' + int_to_en(num % k)

    if (num < b):
        if (num % m) == 0: return int_to_en(num // m) + ' million'
        else: return int_to_en(num // m) + ' million, ' + int_to_en(num % m)

    if (num < t):
        if (num % b) == 0: return int_to_en(num // b) + ' billion'
        else: return int_to_en(num // b) + ' billion, ' + int_to_en(num % b)

    if (num % t == 0): return int_to_en(num // t) + ' trillion'
    else: return int_to_en(num // t) + ' trillion, ' + int_to_en(num % t)

    raise AssertionError('num is too large: %s' % str(num))
    
def NamedPlace(debug=0):
    sNumb = NumberNamer()#.encode('utf-8')
    # sAdj = SimplePicker(shPlaces,0).encode('utf-8')
    sAdj = str(SimplePicker(shPlaces,0))
    sPlace = SimplePicker(shPlaces,1)#.encode('utf-8')
    sUnique = SimplePicker(shPlaces,3)#.encode('utf-8')
    sObj = SimplePicker(shPlaces,4)#.encode('utf-8')
    sObjs = SimplePicker(shPlaces,5)#.encode('utf-8')
        
    if re.search('th$|first|second|third',sNumb) or sNumb == 'one':
        sOpt1A = ' '.join([sNumb, sPlace])
    elif random.choice( [0,1] ) == 1:
        sOpt1A = ' '.join([sNumb, Pluralizer(sPlace)])
    else:
        sOpt1A = Pluralizer(sPlace)
    #print sOpt1
    
    if re.search('th$|first|second|third',sNumb) or sNumb == 'one':
        sOpt1B = ' '.join([sNumb, sAdj, sPlace])
    elif random.choice( [0,1] ) == 1:
        sOpt1B = ' '.join([sNumb, sAdj, Pluralizer(sPlace)])
    else:
        sOpt1B = ' '.join([sAdj, Pluralizer(sPlace)])
    #print sOpt1A
    sOpt1C = sUnique
    
    opt1_prob = [ [sOpt1A, .55] , [sOpt1B, .40] , [sOpt1C, .05] ]
    sOpt1 = pick_random(opt1_prob)
    
    sOpt2A = ' '.join([' of the', sObj])
    sOpt2B = ' '.join([' of',sObjs])
    
    # if sOpt1.decode('ascii',errors='ignore') == sOpt1C.decode('ascii',errors='ignore'):
        # return sOpt1
    # else:    
        # return DoWeAddPhrase("The %s" % (sOpt1.title()),random.choice([sOpt2A.title(),sOpt2B.title()]),0.5)
    return DoWeAddPhrase("The %s" % (sOpt1.title()),random.choice([sOpt2A.title(),sOpt2B.title()]),0.5)
        
def TavernMaker():
    sSaloon = SimplePicker(shPlaces,2).strip().title()
    
    sObject1 = SimplePicker(shPlaces,4).strip().title()    #cup
    sObject2 = SimplePicker(shPlaces,4).strip().title()    #sword

    sTitles = SimplePicker(shKings,0).strip().title()            #king's
    sHumDesc1 = SimplePicker(shKings,3).strip().title()            #anxious
    
    iMobType = random.randint(0,1)
    mob_list = list(filter(None, shMobAtk.col_values(iMobType,1)))
    allit_list = []
    for i in mob_list:
        if i[0] == sHumDesc1[0]:
            allit_list.append(i)    #gets list of all alliterive mobs
    if len(allit_list) == 1:
        strRanMob = allit_list[0]
    elif len(allit_list) == 0:
        strRanMob = 'len(alliterive_list) = 0'
    else:
        strRanMob = allit_list[random.randint(0,len(allit_list)-1)].strip().title()
        
        
    optTavern = []
    
    optTavern.append(DoWeAddPhrase('The %s and %s ' % (sObject1, sObject2), sSaloon, .5))
    optTavern.append(DoWeAddPhrase('The %s %s ' % (sHumDesc1, sObject1), sSaloon, .8))
    optTavern.append(DoWeAddPhrase('The %s %s ' % (sHumDesc1, strRanMob), sSaloon, .3))
    optTavern.append("The %s %s's %s" % (sHumDesc1, sTitles, sSaloon))
    optTavern.append("The %s of %ss"  % (sSaloon, sObject1))
    optTavern.append("The %s of the %s" % (sSaloon, sObject1))
    optTavern.append("The %s of the %s %s" % (sSaloon, sHumDesc1, sObject1))
    
    return ' '.join(random.choice(optTavern).split())
    
def SillyTrans(language, strIn):
    strOut = ""
    if strIn is None:
        strIn = "hello world"
    
    if language == "lang_dwarven":
        column = 2            
    elif language == "lang_goblin":
        column = 3
    elif language == "lang_elfish":
        column = 4
    elif language == "lang_orcish":
        column = 5
    elif language == "lang_draconic":
        column = 6
    elif language == "lang_lizard":
        column = 7
    elif language == "lang_chth":
        column = 8
    
    for word in re.findall(r"[\w']+", strIn):
        # print("1: ", word)
        word  = re.sub(r'[^a-zA-Z]', '',word)
        # print("2: ", word)
        if word == "yourdm":
            continue
        
        strReady = word
        let_list = list(shWORDMAKER.col_values(0)[1:])  # the [1:] just skips the header line from xcel
        col_list = list(shWORDMAKER.col_values(1)[1:])
        # print(let_list)
        # print(col_list)
        tls = {}
        for o, r in zip(let_list, col_list):
            tls[o] = r
        # print(tls)
        for k, v in tls.items():
            # print(v)
            if v in word:
                # print(k, v)
                # strReady = ''.join([strReady, k])
                strReady = word.replace(v, k)
                # print(word)
        
        # # # let_list = list(filter(None, shWORDMAKER.col_values(0,1)))
        let_list = list(shWORDMAKER.col_values(0))      
        # print(let_list)

        # # # col_list = list(filter(None, shWORDMAKER.col_values(column,1)))
        col_list = list(shWORDMAKER.col_values(column))
        # print(col_list)
        
        wordOut = ""
        new_letter = ""
        
        tls = {}
        for o, r in zip(let_list, col_list):
            tls[o] = r
        
        # print(tls)
        # print(strReady)
        
        for letter in strReady:
            # print(letter)
            # # # print("letter: ", letter, " -> ", tls[letter])
            wordOut = wordOut + tls[letter]
        strOut = ' '.join([strOut, wordOut]).strip()

    return strOut