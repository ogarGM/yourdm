from __future__ import unicode_literals
#import twitter, os
import random
import linecache
import xlrd
import sys
import time
import itertools    
#from string import maketrans  
import re
from map_generator import *
from emoji_field import Swath #circular dependancy :(
from YDM_tools import *

import unicodedata

#loadup dictionary 
#wb = xlrd.open_workbook('mob2.xls')
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

############################################################
############################################################
##                                                        ##
##                                                        ##
##                    STATUS GENERATORS                   ##
##                                                        ##
##                                                        ##
############################################################
############################################################    

    

def Status00(debug=0,strIn=None):
    sGoal1 = SimplePicker(shAdvice,0).strip()
    sGoal2 = SimplePicker(shAdvice,0).strip()
    
    #sVill = SimplePicker(shAdvice,1).strip()
    sAssist = SimplePicker(shAdvice,3).strip()
    
    sAction1 = SimplePicker(shAdvice,2).strip()
    sAction2 = SimplePicker(shAdvice,2).strip()
    sAction3 = SimplePicker(shAdvice,2).strip()
    
    sOptAct = []
    sOptAct.extend([sAction1,sAction2,sAction3])
    sOptAct.append(DoWeAddPhrase(sAction1," and " + sAction2))
    sOptAct.append(DoWeAddPhrase(sAction1,", " + sAction2 + " and " + sAction3))
    sAct = random.choice(sOptAct)
    #print sAct
    
    sOptGoal = []
    sOptGoal.extend([sGoal1,sGoal2])
    sOptGoal.append(DoWeAddPhrase(sGoal1," and " + sGoal2))
    
    sGoals = random.choice(sOptGoal)
    
    strOut = ''.join([DoWeAddPhrase("%s by %s" % (sGoals.capitalize(),sAct), ", with the help of %s" % (AnAFixer(sAssist)), .5), "."])
    return strOut
    
def Status01(debug=0,strIn=None):    ### Attacks
    #2 
    #A [mob_desc] [mob] arrives! 
    #{1} It [attack verbs] you for [# 3d12] damage! 
    #{2} It hasn't noticed you. 
    #{3} It [attack verbs] your [body_part] for [# 3d12] damage! 
    #{4} [nothing]
    sRanMob = PickRandomMob()
    
    sAttacks = Pluralizer(SimplePicker(shMobAtk,4).strip())
    sStatus = SimplePicker(shMobAtk,5).strip()
    sClass = SimplePicker(shMobAtk,3).strip()
    sBodyPt = SimplePicker(shMobAtk,6).strip()
    sDefeat = SimplePicker(shMobAtk,7).strip()
    sDefeating = Verbing(SimplePicker(shMobAtk,7).strip())
    sDefeated = Verbed(SimplePicker(shMobAtk,7).strip())
    sAbilty = SimplePicker(shMobAtk,8).strip()
    
    sUArriveAt = SimplePicker(shPlaces,7).strip()
    sDungeon = SimplePicker(shPlaces,1).strip()
    sItIs = SimplePicker(shPlaces,10).strip()
    sHeroItem = SimplePicker(shAdjecs,5).strip()
    sItArrivesAt = SimplePicker(shMobAtk,9).strip()
    sItAppears = SimplePicker(shMobAtk,10).strip()
    
    arrNumOfAdjProb = [[0,.12],[1,.8],[2,.08]]#decide on number of adjectives 1 most common, 0 , 2 , 3
    sMobAdj = PickAdjPhrase(pick_random(arrNumOfAdjProb))
    
    if random.randint(0,1) == 1:
        strLfOrRt = 'right'
    else:
        strLfOrRt = 'left'
    
    strAdjAndMob = sMobAdj + ' ' + sRanMob
    
    strStart = '%s %s.' % (AnAFixer(strAdjAndMob[1:]).title().strip(), sItAppears)
        
    strOpt1 = ' It %s you for %i damage!' % (sAttacks,RollDice(2,12))
    strOpt2 = ' It hasn\'t noticed you.'
    strOpt3 = ' It %s your %s %s for %i damage!' % (sAttacks, strLfOrRt, sBodyPt, RollDice(2,12))
    strOpt4 = ''

    optID = [[0,.5],[1,.08],[2,.3],[3,.12]]
    iChoice = pick_random(optID)

    if iChoice == 0:
        strStart = DoWeAddPhrase(strStart, strOpt1, 1)
    elif iChoice == 1:
        strStart = DoWeAddPhrase(strStart, strOpt2, 1)
    elif iChoice == 2:
        strStart = DoWeAddPhrase(strStart, strOpt3, 1)
    elif iChoice == 3:
        strStart = DoWeAddPhrase(strStart, strOpt4, 1)
    else:
        strStart = 'thers been an error'

    return strStart
    
def Status02(debug=0,strIn=None):    #### AREA DESC LONG 
    sRanMob = PickRandomMob().strip()
    sAniMob = PickAnimalMob().strip()
    sSupMob = PickSuperMob().strip()
    sHumMob = PickHumanoidMob().strip()
    
    sUArriveAt = SimplePicker(shPlaces,7).strip()
    sDungeon = SimplePicker(shPlaces,1).strip()
    sItIs = SimplePicker(shPlaces,10).strip()
    sHeroItem = SimplePicker(shAdjecs,5).strip()
    sItArrivesAt = SimplePicker(shMobAtk,9).strip()
    sItAppears = SimplePicker(shMobAtk,10).strip()
    
    sExits = ExitString()
    
    sPropNoun1 = RandomProperNoun()
    if debug == 0:
        sPropNoun1 = FlavorLetter(sPropNoun1)

    strOut1 = 'You %s %s' % (sUArriveAt,AnAFixer(sDungeon))
    iChoice = random.randint(0,13)
    if iChoice <= 10:    #regular dungeon descrip
        sApp = '. It is %s.' % (sItIs)
    elif iChoice == 11:    #old year
        sApp = ' in the year %i BC.' % (random.randint(0,3000)) 
    elif iChoice == 12:    #new year
        sApp = ' in the year %i.' % (random.randint(0,3000))    
    elif iChoice == 13:    #day and month
        sApp = ' on day %i in the month of %s.' % (random.randint(1,31),sPropNoun1)

    strOut = strOut1 + sApp
    strOpt2 = ' You have %s.' % (sHeroItem)
    strOpt3 = ' There are %s here!' % (Pluralizer(sRanMob))
    
    if len(sExits) >= 2:
        strOpt4 = ' There are exits to the %s and %s.' % (sExits[:len(sExits)-1],sExits[len(sExits)-1:])
    elif len(sExits) != 0:
        strOpt4 = ' There are exits to the %s.' % (sExits)
    else:
        strOpt4 = ""

    strOut = DoWeAddPhrase(strOut, strOpt2, .8)
    strOut = DoWeAddPhrase(strOut, strOpt3, .6)
    strOut = DoWeAddPhrase(strOut, strOpt4, .4)
    
    return strOut
    
def Status03(debug=0,strIn=None):    #AREA DESC SHORT

    sShopItem = SimplePicker(shAdjecs,3).strip()
    
    sUArriveAt = SimplePicker(shPlaces,7).strip()
    sDungeon = SimplePicker(shPlaces,1).strip()
    sItIs = SimplePicker(shPlaces,10).strip()
    sHeroItem = SimplePicker(shAdjecs,5).strip()

    
    
    sRanMob = PickRandomMob()
    
    sThereAR = SimplePicker(shPlaces,5).strip()
    
    k = random.randint(0,3)
    if k <= 2:
        sThereIS = SimplePicker(shPlaces,4).strip()
    else:
        sThereIS = AnAFixer(sRanMob)
    
    iChoice = random.randint(0,5)
    if iChoice == 0:
        strOut = 'You %s %s.' % (sUArriveAt,AnAFixer(sDungeon))
    elif iChoice == 1:
        strOut = 'You are in %s.' % (AnAFixer(sDungeon))
    elif iChoice == 2:
        strOut = 'It is %s.' % (sItIs)
    elif iChoice == 3:
        strOut = 'You have %s.' % (sHeroItem)
    elif iChoice == 4:
        strOut = 'It is the year %i BC.' % (random.randint(0,3000))
    elif iChoice == 5:
        strOut = 'It is the year %i.' % (random.randint(0,3000))
    #elif iChoice == 4:
    #    strOut = 'There is %s here.' % (sHeroItem)    
    #elif iChoice == 7:
    #    strOut = 'There are %s here.' % (sShopItem)
    
    strOpt1 = ' There are %s here.' % (sThereAR)
    strOpt2 = ' There is %s here.' % (sThereIS)
    
    iChoice2 = random.randint(0,1)
    if iChoice2 == 0:
        strOut = DoWeAddPhrase(strOut, strOpt1, .7)
    else:
        strOut = DoWeAddPhrase(strOut, strOpt2, .7)
    
    return strOut
    
def Status04(debug=0,strIn=None):    ### SHOP ADS
    #2 
    #The [color].title() [mob_animal].title() is selling 
        #{1}[adj]
        #{2}[color]
        #{3}[material]
        #[item]s for [# 1-5000] gold pieces!.
        
    sMaterial = SimplePicker(shAdjecs,16).strip()
    sShopItem = SimplePicker(shAdjecs,3).strip()
    sColors = SimplePicker(shAdjecs,8).strip()
    
    
    arrNumOfAdjProb = [[0,.12],[1,.8],[2,.08]]#decide on number of adjectives 1 most common, 0 , 2 , 3
    sMobAdj = PickAdjPhrase(pick_random(arrNumOfAdjProb))#
    
    
    x = random.randint(0,2)
    if x == 0:
        strStart = '%s is having a sale on' % (TavernMaker().strip())
    elif x == 1:
        strStart = 'Well *I* heard that %s is the best place to get' % (TavernMaker().strip())
    elif x == 2:
        strStart = "If I were you, I'd avoid %s altogether. I mean, they were selling" % (TavernMaker().strip())
    
    strOpt1 = ' ' + sMobAdj.lower().strip()
    strOpt2 = ' ' + sColors.lower().strip()
    strOpt3 = ' ' + sMaterial.lower().strip()
    
    strEnd = ' %s for %i gold pieces! Each!' % (sShopItem.lower(), random.randint(1,5000))
    
    strOpt = []
    strOpt.append(DoWeAddPhrase(strStart, strOpt1, 1))
    strOpt.append(DoWeAddPhrase(strStart, strOpt2, 1))
    strOpt.append(DoWeAddPhrase(strStart, strOpt3, 1))
    
    strStart = strOpt[pick_random([ [0, .18],
                                [1,.22],
                                [2,.60], ] )]

    strUpdate = strStart + strEnd
    
    return strUpdate
    
def Status05(debug=0,strIn=None): ### DOUBTFUL SHOP
    #2 
    #The [color].title() [mob_animal].title() is selling 
        #{1}[adj]
        #{2}[color]
        #{3}[material]
        #[item]s for [# 1-5000] gold pieces!.
        
    sMaterial = SimplePicker(shAdjecs,16).strip().strip()
    sShopItem = SimplePicker(shAdjecs,3).strip()
    sColors = SimplePicker(shAdjecs,8).strip()
    
    sEffect = SimplePicker(shDrinks,3).strip()
    sDoubts = SimplePicker(shDrinks,4).strip()
    sButs = SimplePicker(shDrinks,5).strip()
    
    sHumDesc1 = SimplePicker(shKings,3)
    
    m = 1
    while m == 1:
        if 'water' in sDoubts or 'risly' in sDoubts:
            sDoubts = SimplePicker(shDrinks,4).strip().strip()
        elif 'are' in sDoubts:
            sDoubts = sDoubts.replace('are','is')
        elif "don't" in sDoubts:
            sDoubts = sDoubts.replace("don't","doesn't")
        elif 'do not' in sDoubts:
            sDoubts = sDoubts.replace('do not','does not')
        elif 'have' in sDoubts and 'to have' not in sDoubts:
            sDoubts = sDoubts.replace('have', 'has')
        elif 'to has' in sDoubts:
            sDoubts = sDoubts.replace('to has','to have')
        else:
            m = 2            
    
    arrNumOfAdjProb = [[0,.12],[1,.8],[2,.08]]#decide on number of adjectives 1 most common, 0 , 2 , 3
    sMobAdj = PickAdjPhrase(pick_random(arrNumOfAdjProb))
    #pick monster#
    iMobType = random.randint(0,1)
    mob_list = list(filter(None, shMobAtk.col_values(iMobType,1)))
    allit_list = []
    
    for i in mob_list:
        if i[0] == sHumDesc1[0] and ' ' not in i:
            allit_list.append(i)    
    if len(allit_list) == 1:
        strRanMob = allit_list[0]
    elif len(allit_list) == 0:
        strRanMob = 'len(alliterive_list) = 0'
    else:
        strRanMob = allit_list[random.randint(0,len(allit_list)-1)]
        
        
    #print sHumDesc1
    #print strRanMob
    #print sDoubts
    #print sShopItem
    #k = random.randint(0,1)
    #if k == 0:
        #strOut = "The %s %s %s have %s in stock." % (sHumDesc1.title(), strRanMob.title(), sDoubts, sShopItem.lower())
    #elif k == 1:
        #strOut = "The %s %s %s have %s in stock, but %s." % (sHumDesc1.title(), strRanMob.title(), sDoubts, sShopItem.lower(),sButs)
        
    #elif k == 2:
    #    strOut = "The %s %s %s has been the best place to get %s, but %s." % (sHumDesc1.title(), strRanMob.title(), sDoubts, sShopItem.lower(), sButs)
    
    strOut = DoWeAddPhrase("%s %s have %s in stock" % (TavernMaker().strip(), sDoubts, sShopItem.lower()), ", but " + sButs, 0.5) + "."
    
    return strOut
    
def Status06(debug=0,strIn=None): ### drinking
    
    col_list = list(filter(None, shMobAtk.col_values(2,1)))
    col_list.append('DM')
    col_list.append('player to your right')
    col_list.append('player to your left')
    col_list.append('Any PC')
    col_list.append('Any NPC')
    col_list.append('Any character')
    col_list.append('Someone')

    sHumoid = col_list[random.randint(0,len(col_list)-1)]

    if sHumoid[:4] != 'Any ' and sHumoid[:4] != 'Some':
        sHumoid = ' '.join([random.choice(['The','Any']),sHumoid])
    
    # sClause = SimplePicker(shDrinks,0).encode('utf8',errors='replace').strip()
    # sEvent = SimplePicker(shDrinks,1).encode('utf8',errors='replace').strip()
    # sRule = SimplePicker(shDrinks,2).encode('utf8',errors='replace').strip()    
    sClause = SimplePicker(shDrinks,0).strip()
    sEvent = SimplePicker(shDrinks,1).strip()
    sRule = SimplePicker(shDrinks,2).strip()
    
    strOpt = []
    strOpt.append('%s %s %s, %s!' % (sClause, sHumoid, sEvent, sRule))
    strOpt.append('New Rule! %s %s %s, %s!' % (sClause, sHumoid, sEvent, sRule))
    
    return random.choice(strOpt)

    
def Status07(debug=0,strIn=None):### YOU POTIONS
    
    sAdj1 = random.choice([SimplePicker(shAdjecs,8).strip(),SimplePicker(shAdjecs,11).strip()])
    sAdj2 = random.choice([SimplePicker(shAdjecs,8).strip(),SimplePicker(shAdjecs,11).strip()])
    if sAdj2 == sAdj1:
        sAdj2 = random.choice([SimplePicker(shAdjecs,8).strip(),SimplePicker(shAdjecs,11).strip()])
    else:
        k = 2
            
    sAdj3 = random.choice([SimplePicker(shAdjecs,8).strip(),SimplePicker(shAdjecs,11).strip()])
    k = 1
    while k == 1:
        if sAdj3 == sAdj1 or sAdj3 == sAdj2:
            sAdj3 = random.choice([SimplePicker(shAdjecs,8).strip(),SimplePicker(shAdjecs,11).strip()])
        else:
            k = 2
            
    sAdj4 = random.choice([SimplePicker(shAdjecs,8).strip(),SimplePicker(shAdjecs,11).strip()])
    k = 1
    while k == 1:
        if sAdj4 == sAdj1 or sAdj4 == sAdj2 or sAdj4 == sAdj3:
            sAdj4 = random.choice([SimplePicker(shAdjecs,8).strip(),SimplePicker(shAdjecs,11).strip()])
        else:
            k = 2
            
    sLiquid1 = SimplePicker(shAdjecs,9).strip()
    sLiquid2 = SimplePicker(shAdjecs,9).strip()
    
    sTaste1 = SimplePicker(shAdjecs,10).strip()
    sTaste2 = SimplePicker(shAdjecs,10).strip()
    k = 1
    while k == 1:
        if sTaste2 == sTaste1:
            sTaste2 = SimplePicker(shAdjecs,11).strip()
        else:
            k = 2
    sTaste3 = SimplePicker(shAdjecs,10).strip()
    k = 1
    while k == 1:
        if sTaste3 == sTaste1 or sTaste3 == sTaste2:
            sTaste3 = SimplePicker(shAdjecs,11).strip()
        else:
            k = 2
    sTaste4 = SimplePicker(shAdjecs,10).strip()
    k = 1
    while k == 1:
        if sTaste4 == sTaste1 or sTaste4 == sTaste2 or sTaste4 == sTaste3:
            sTaste4 = SimplePicker(shAdjecs,11).strip()
        else:
            k = 2
        
    sPie = SimplePicker(shAdjecs,14).strip()
    
    sColors = SimplePicker(shAdjecs,8).strip()
    
    sEffect1 = SimplePicker(shDrinks,3).strip()
    sEffect2 = SimplePicker(shDrinks,3).strip()
    sDoubts = SimplePicker(shDrinks,4)#.encode('utf8',errors='replace')

    sButs = SimplePicker(shDrinks,5).strip()#.encode('utf8',errors='replace')
    
    #####################################################
    sAdjOpt = [    sAdj1,
                sAdj1 + " and " + sAdj2,
                sAdj1 + ", " + sAdj2 + " and " + sAdj3]
    sPotion1 = (random.choice(sAdjOpt) + " " + sLiquid1).strip()
    sPotion2 = (random.choice(sAdjOpt) + " " + sLiquid2).strip()
    
    #####################################################            
    sPieces = "with %s %s" % (sAdj4, sPie)
    #####################################################
    sCanCause = "%s %s %s" % (sDoubts, random.choice(["grant","cause"]), sEffect1)
    #####################################################
    sFlav1 = DoWeAddPhrase(sTaste1, " and " + sTaste2, .4)
    sFlav2 = DoWeAddPhrase(sTaste3, " and " + sTaste4, .4)
    sSmellTaste = random.choice(["smells like %s." % (sFlav1),
                                    "smells and tastes like %s." % (sFlav1),
                                    "smells like %s but tastes like %s." % (sFlav1, sFlav2)])
    #####################################################
    
    sPotionPhrase1 = DoWeAddPhrase("This %s" % sPotion1, " (" + sPieces + ")",.3) + " " + sSmellTaste
    sPotionPhrase2 = DoWeAddPhrase("%ss" % sPotion1.title(), " (" + sPieces + ")",.3) + " " + sCanCause + "."
    
    sPotionA = "Be sure to avoid %ss%s, though!" % (sPotion2.strip(), DoWeAddPhrase("", " (" + sPieces + ")", .2))
    sPotionB = "Those %s %s!" % (sCanCause, sEffect2)
    
    sPotion3 = "If you need to cure %s, quaff a %s%s." % (sEffect1,sPotion1,DoWeAddPhrase(""," (" + sPieces + ")",.3)) + DoWeAddPhrase(" ", DoWeAddPhrase(sPotionA, sPotionB, .2),.2)
    
    sPotion4 = "If you want to gain %s, quaff a %s%s." % (sEffect1,sPotion1,DoWeAddPhrase(""," (" + sPieces + ")",.3)) + DoWeAddPhrase(" ", DoWeAddPhrase(sPotionA, sPotionB, .2),.2)
    
    sPotion5 = "Afflicted by %s? Quaff a %s%s." % (sEffect1,sPotion1,DoWeAddPhrase(""," (" + sPieces + ")",.3)) + DoWeAddPhrase(" ", sPotionA, .2)
    sPotion6 = "Wishing you had %s? Try a %s%s." % (sEffect1,sPotion1,DoWeAddPhrase(""," (" + sPieces + ")",.3)) + DoWeAddPhrase(" ", sPotionA, .2)
    return random.choice([sPotionPhrase1,sPotionPhrase1,sPotionPhrase1,
                            sPotionPhrase2,sPotionPhrase2,sPotionPhrase2,
                            sPotion3,
                            sPotion4,
                            sPotion5,
                            sPotion6])
    
    
def Status08(debug=0,strIn=None): ##### KING REPORT
        #6 
    #[hero name], the [adj][title] of [place name] has [king_action]
    sDefeated = Verbed(SimplePicker(shMobAtk,7).strip())
    
    sRanMob = PickRandomMob()
    
    sTitle = SimplePicker(shKings,0)
    #gender tuple stuffs
    sKingDoes = SimplePicker(shKings,2)
    sHumDesc1 = SimplePicker(shKings,3)
    sHumDesc2 = SimplePicker(shKings,3)
    sHumDesc3 = SimplePicker(shKings,3)
    
    sPropNoun1 = RandomProperNoun()
    sPropNoun2 = RandomProperNoun()
    sPropNoun3 = RandomProperNoun()
    
    if debug == 0:
        sPropNoun1 = FlavorLetter(sPropNoun1)
        sPropNoun2 = FlavorLetter(sPropNoun2)
        sPropNoun3 = FlavorLetter(sPropNoun3)
        
    sFlavNoun = FlavorfulProperNoun()

    strFullName = sPropNoun1.title() + ' ' + sFlavNoun.title()
    
    k = random.randint(0,1)
    if k == 0:
        strStart = '%s, the %s and %s %s of %s, has %s!' % (strFullName.title(), sHumDesc1.lower(), sHumDesc2.lower(), sTitle.title(), sPropNoun2.title(), sKingDoes)
    elif k == 1:
        strStart = 'Poor %s, %s by a %s %s!' % (sPropNoun1.title(), sDefeated.lower(), sHumDesc1.lower(), sRanMob.title())
        
    return strStart
    
def Status09(debug=0,strIn=None):##### YOU KING
            #6 
    #[hero name], the [adj][title] of [place name] has [king_action]
    sTitle = SimplePicker(shKings,0)
    sTitle2 = SimplePicker(shKings,0)
    #gender tuple stuffs
    sKingDoes = SimplePicker(shKings,2)
    sHumDesc1 = SimplePicker(shKings,3)
    sHumDesc2 = SimplePicker(shKings,3)
    sHumDesc3 = SimplePicker(shKings,3)
    
    sRelation = SimplePicker(shKings,4)
    
    sRealm = SimplePicker(shKings, 8)
        
    sPropNoun1 = RandomProperNoun()
    sPropNoun2 = RandomProperNoun()
    sPropNoun3 = RandomProperNoun()
    
    if debug == 0:
        sPropNoun1 = FlavorLetter(sPropNoun1)
        sPropNoun2 = FlavorLetter(sPropNoun2)
        sPropNoun3 = FlavorLetter(sPropNoun3)
        
    sFlavNoun = FlavorfulProperNoun()
    
    sHumMob1 = PickHumanoidMob()
    sHumMob2 = PickHumanoidMob()
    
    sHumMob3 = Pluralizer(PickHumanoidMob())
    sHumMob4 = Pluralizer(PickHumanoidMob())
    sHumMob5 = Pluralizer(PickHumanoidMob())

    strFullName = sPropNoun1.title() + ' ' + sFlavNoun.title()
    
    sHeroItem = SimplePicker(shAdjecs,5).strip()
    
    sDefeater = Verber(SimplePicker(shMobAtk,7).strip())
    
    sDungeon = SimplePicker(shPlaces,1).strip()
        
    optStr = []
    
    optStr.append('You are reborn as %s, the %s and %s %s of the %s of %s!' % (strFullName.title(), sHumDesc1.lower(), sHumDesc2.lower(), sTitle.title(), sRealm.title(), sPropNoun2.title()))
    optStr.append('You are %s %s, the %s %s of %s %s and %s %s.' % (sTitle.title(), sPropNoun1.title(), sHumDesc1.lower(), sRelation, AnAFixer(sHumDesc2).lower(), sHumMob1.title(), AnAFixer(sHumDesc3).lower(), sHumMob2.title()))
    optStr.append('You are %s, %s of %s! You have %s!' % (sPropNoun1.title(), sRelation, sPropNoun2.title(), AnAFixer(sHeroItem)))
    optStr.append("Oh my God! Tell me you're not %s, %s of the %s %s!" % (strFullName, sDefeater.lower(), sHumDesc1.title(), sDungeon.title()))
    optStr.append('You awaken as %s, the %s %s, and %s %s of the %s of %s!' % (strFullName.title(), sHumDesc1.lower(), sTitle.title(), sHumDesc2.lower(), sTitle2.title(), sRealm.title(), sPropNoun2.title()))
    optStr.append('You are known to the %s as %s, to the %s as %s, and to the %s as %s!' % (sHumMob3.lower(), sPropNoun1.title(), sHumMob4.lower(), sPropNoun2.title(),sHumMob5.lower(), sPropNoun3.title()))
    optStr.append('Welcome %s, %s %s of the %s of %s!' % (strFullName.title(), sHumDesc2.lower(), sTitle2.title(), sRealm.title(), sPropNoun2.title()))
    # return optStr[pick_random([ [0, .400],
                                # [1,.300],
                                # [2,.200],
                                # [3,.100] ] )]
                                
    return random.choice(optStr)
    
def Status10(debug=0,strIn=None): ##### STATUSED BY A WIZARD
    #3 
    #You have been [statused] by [name], a level [# 1-99] [mob_humanoid] [spell caster]!

    sPropNoun1 = RandomProperNoun()
    sHumMob = PickHumanoidMob()
    
    sStatus = SimplePicker(shMobAtk,5).strip()
    sClass = SimplePicker(shMobAtk,3).strip()
    sBodyPt = SimplePicker(shMobAtk,6).strip()
    
    sColors = SimplePicker(shAdjecs,8).strip()

    if random.randint(0,1) == 1:
        strLfOrRt = 'right'
    else:
        strLfOrRt = 'left'

    optStr = []
    optStr.append('You have been %s by %s, a level %i %s %s!' % (sStatus,sPropNoun1,random.randint(1,99),sHumMob,sClass))
    optStr.append('Your %s %s has been %s by %s, a level %i %s %s!' % (strLfOrRt,sBodyPt,sStatus,sPropNoun1,random.randint(1,99),sHumMob,sClass))
    optStr.append('You have been %s by a level %i %s %s!' % (sStatus,random.randint(1,99),sHumMob,sClass))
    optStr.append('You have been %s by %s. Is this awesome? y/n' % (sStatus, AnAFixer(sClass)))
    optStr.append('You have been %s by %s potion.' % (sStatus, AnAFixer(sColors)))
    optStr.append('Your %s %s has been %s by %s potion.' % (strLfOrRt,sBodyPt,sStatus,AnAFixer(sColors)))
    
    # return optStr[pick_random([ [0, .22],
                                # [1,.21],
                                # [2,.18],
                                # [3,.14],
                                # [4,.13],
                                # [3,.12], ] )]
                                
    return random.choice(optStr)

def Status11(debug=0,strIn=None): ##### Your race

    sAttacks = SimplePicker(shMobAtk,4).strip()
    
    # k = 0
    # while k == 0:
        # if ' at' in sAttacks:
            # sAttacks = SimplePicker(shMobAtk,4).strip()
        # else:
            # k = 1
            
    # sAttacks = sAttacks[:-1].lower()
    # if sAttacks[-2:] == 'he':
        # sAttacks = sAttacks[:-1]
    
    strIn = re.split(r'( +)',sAttacks)[0]
    
    strOut = "You do not have access to %s attacks without the aid of potions." % (strIn.title())
    
    return strOut
    
def Status12(debug=0,strIn=None): #### Bits and Pieces
    sBits = SimplePicker(shBITS,0).strip()
    strOut = sBits
    return strOut
    
def Status13(debug=0,strIn=None): #### Goofy Book Review shit
    strOut = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    while len(strOut) >= 140:
        sNoun1 = SimplePicker(shBOOK,0).strip()#.encode('utf8',errors='replace') #idea of
        sNoun2 = SimplePicker(shBOOK,0).strip()#.encode('utf8',errors='replace') #reading of
        sBook = SimplePicker(shBOOK,0).strip()#.encode('utf8',errors='replace')     #informal sketch of
        
        sMody1 = SimplePicker(shBOOK,1).strip()#.encode('utf8',errors='replace') #civil society
        sMody2 = SimplePicker(shBOOK,1).strip()#.encode('utf8',errors='replace') #the image
        
        sVerb = SimplePicker(shBOOK,2).strip()#.encode('utf8',errors='replace')     #highlights
        
        sRevw = SimplePicker(shBOOK,3).strip()#.encode('utf8',errors='replace')     #is important
        
        sPropNoun1 = RandomProperNoun()
        
        optStr = []
        #optStr.append("The %s %s %s the %s %s." % (sNoun1,sMody1,sVerb,sNoun2,sMody2))
        optStr.append("Your %s %s %s the %s %s." % (sNoun1,sMody1,sVerb,sNoun2,sMody2))
        optStr.append("Your %s the %s %s and the %s %s %s." % (sBook,sNoun1,sMody1, sNoun2,sMody2, sRevw))
        optStr.append("Your %s the interplay between the %s %s and the %s %s %s." % (sBook,sNoun1,sMody1, sNoun2,sMody2, sRevw))
        optStr.append("%s\'s %s the %s %s and the %s %s %s." % (sPropNoun1,sBook,sNoun1,sMody1, sNoun2,sMody2, sRevw))
        
        
        strOut = optStr[pick_random([ [0, .20],
                                    [1,.10],
                                    [2,.30],
                                    [3,.50] ] )]
                                    
        return strOut                            
    
def Status14(debug=0,strIn=None):        ### GIBBERISH
    numWords = random.randint(3,14)
    strStart = ""
    for i in range(numWords):
        each = RandomProperNoun()
        if debug == 0:
            each = FlavorLetter(each)
        strStart = DoWeAddPhrase(strStart, each, 1)
        strStart += " "
    
    if random.random() <= 0.001:
        strStart = ""
        for i in range(numWords):
            each = random.choice(['yolo','swag','lol'])
            if debug == 0:
                each = FlavorLetter(each,prob=.8)
            strStart = DoWeAddPhrase(strStart, each, 1)
            strStart += " "
            
    strOut = ''

    punctOpt = [ [' ',.400],
                [', ',.150],
                ['. ',.140],
                ['? ',.130],
                ['! ',.100],
                ['?! ',.050],
                ['!! ',.020],
                [': ',.010]]

    for word in strStart.lower().split():
        punc = pick_random(punctOpt)
        if strOut != '':
            if any(x in ['.','?','!'] for x in punc):            #if puct is a sentence ender
                strOut = punc.join([strOut, word.capitalize()])    #combine and cpitalize the new word
            else:
                strOut = punc.join([strOut, word])
        else:
            strOut = word.capitalize()
    
    
    punc = pick_random(punctOpt) #pick ending punctuation
    k = 0
    while k < 1:
        if any(x in ['.','?','!'] for x in punc):
            k = 2
        else:
            punc = pick_random(punctOpt)
            
    #print len(strOut + punc)
    return strOut + punc
    
def Status15(debug=0,strIn=None):        ### LOST CIVILIZATION
    sPlace = RandomProperNoun()
    
    sTrait = SimplePicker(shLOSTEMP,0).strip()
    sBadT1 = SimplePicker(shLOSTEMP,1).strip()
    sBadT2 = SimplePicker(shLOSTEMP,1).strip()
    
    sBiome = SimplePicker(shLOSTEMP,2).strip()
    sGovrn = SimplePicker(shLOSTEMP,3).strip()
    
    sKnown = SimplePicker(shLOSTEMP,4).strip()
    sAchev = SimplePicker(shLOSTEMP,5).strip()
    sTechs = SimplePicker(shLOSTEMP,6).strip()
    sDisas = SimplePicker(shLOSTEMP,7).strip()
    
    sFlaws = SimplePicker(shLOSTEMP,8).strip()
    
    sRuin1 = SimplePicker(shLOSTEMP,9).strip()
    sRuin2 = SimplePicker(shLOSTEMP,9).strip()
    
    k = 1
    while k == 1:
        if sRuin1 == sRuin2:
            sRuin2 = SimplePicker(shLOSTEMP,9).strip()
        else:
            k = 2
    
    sDesc = random.choice([sTrait,sBadT1])
    
    if debug == 0:
        sPlace = FlavorLetter(sPlace)
    

    sAdjPhrase = ""
    sAdjPhrase = DoWeAddPhrase(sAdjPhrase, " " + sDesc, 0.5)
    sAdjPhrase = DoWeAddPhrase(sAdjPhrase, " " + sBiome, 0.5)
    

    if random.choice([0,1]) == 0:
        sCivilization = AnAFixer((sAdjPhrase + " " + sGovrn).strip())
    else:
        sCivilization = "The " + (sAdjPhrase + " " + sGovrn).strip().title()
    
    
    sOnceKnown = "once %s for its %s %s" % (sKnown, sAchev, sTechs)
    sWasDestroyed = "was destroyed by %s" % (sDisas.title())
    sCaused = "caused by its peoples' %s %s" % (sBadT2,sFlaws.title())
    sRemains = " Now only %s remain." % (DoWeAddPhrase(sRuin1, " and "+sRuin2,0.5))
        
    sCivKnownDestroyed = DoWeAddPhrase(DoWeAddPhrase(sPlace, ", " + sCivilization, 0.5),", " + sOnceKnown +",", .7) + " " + sWasDestroyed
    
    sCivCaused = DoWeAddPhrase(sCivKnownDestroyed, "; " + sCaused, .2) + "."
    
    sOut = DoWeAddPhrase(sCivCaused, sRemains, .9)
    
    return sOut
    

def Status16(debug=0,strIn=None):
    sSize = SimplePicker(shAdjecs,0).strip()
    
    sEvil = SimplePicker(shAdjecs,1).strip()
    
    sKey1 = SimplePicker(shAdjecs,4).strip()
    sKey2 = SimplePicker(shAdjecs,5).strip()
    
    sAdj1 = SimplePicker(shAdjecs,7).strip()
    
    sColor1 = SimplePicker(shAdjecs,8).strip()
    sColor2= SimplePicker(shAdjecs,8).strip()
    
    sSmell = SimplePicker(shAdjecs,10).strip()
    
    sSD = SimplePicker(shAdjecs,11).strip()
    sSO = SimplePicker(shAdjecs,12).strip()
    sSE = SimplePicker(shAdjecs,13).strip()
    sShape = SimplePicker(shAdjecs,15).strip()

    sKey = []
    sKey.append(sKey1)
    sKey.append(AnAFixer((sColor2+" "+sKey2)))
    sKey.append(sKey1 +" and " + AnAFixer(sColor2+" "+sKey2))
    sKeys = random.choice(sKey)

    strOpt = []
    strOpt.append("%s portal has just opened! Do you see it? It's %s %s %s. Maybe it'll take us to %s" % (AnAFixer(sSize.lower()), AnAFixer(sAdj1),sColor1,sShape, NamedPlace())+'?!')
    strOpt.append("Seek out the portal to %s. Know it by the smell of %s." % (NamedPlace(), sSmell) )
    strOpt.append("Seek out the portal to %s. Know it by the sound of %s %s." % (NamedPlace(), AnAFixer(sSD), sSO ) )
    strOpt.append("Beware the %s portal to %s!" % (sSize, NamedPlace() ) )
    strOpt.append("Beware the %s portal to %s!" % (sEvil, NamedPlace() ) )
    strOpt.append("This portal leads to %s, but can only be opened by %s." %(NamedPlace(), sKeys))
    strOpt.append("A %s Portal has opened. A %s %s %s from it! It's %s and smells of %s." %(sSize, sSD, sSO, sSE, sAdj1, sSmell ))
    return random.choice(strOpt)
            
def Status17(debug=0,strIn=None):

    sAdj = SimplePicker(shKings,3).strip()
    sCrim = SimplePicker(shKings,6).strip()
    sPun = SimplePicker(shKings,7).strip()
    
    patterns = \
    (
    (r'<animal>','<animal>',     SimplePicker(shMobAtk,0).strip()),
    (r'<class>', '<class>',         SimplePicker(shMobAtk,3).strip()),
    (r'<objects>','<objects>',     Pluralizer(SimplePicker(shPlaces,4))),
    (r'$', '$', ''),                    #everything else??
    )
    # ruleList = map(buildRule, patterns)
    ruleList = list(itertools.starmap(buildRule, patterns))
    
    for rule in ruleList:
        if rule(sCrim):
            sCrimes = rule(sCrim)
            break
    
    strOut = []        
    strOut.append("In the %s nation of %s, the penalty for %s is %s." % (sAdj, NamedPlace(), sCrimes, sPun))
    #strOut.append("In the nation of %s, the penalty for %s is %s." % (NamedPlace().decode('utf-8',errors='ignore'), sCrimes, sPun))
    strOut.append("In the nation of %s, the penalty for %s is %s." % (NamedPlace(), sCrimes, sPun))
    strOut.append("Tread lightly in the nation of %s, for the penalty for %s is %s." % (NamedPlace(), sCrimes, sPun))
    return random.choice(strOut)

def Status18(debug=0,strIn=None):
    sAdj = SimplePicker(shPlaces, 0).strip()
    sFeature = SimplePicker(shPlaces, 8).strip()
    strOut = []
    strOut.append("You are staying at %s." % (TavernMaker()) )
    strOut.append("You've decided against staying at %s." % (TavernMaker()) )
    strOut.append("You are staying at %s, which has its own %s!" % (TavernMaker(), sFeature) )
    strOut.append("You are staying at %s, which boasts %s %s!" % (TavernMaker(), AnAFixer(sAdj), sFeature ) )
    return random.choice(strOut)

def Status19(debug=0,strIn=None):
    new_dungeon = Dungeon((15, 8), "whoCares", 5, (3, 3), (6, 4))
    # new_dungeon = Dungeon((140, 40), "whoCares", 80, (4, 3), (8, 6))
    ###Dungeon((grid_size_x, grid_size_y), name, max_num_rooms, min_room_size, max_room_size)
    new_dungeon.generate_dungeon()

    if debug == 1:
        patterns = \
        (
        (r'\b0\b', '0' ,'='),        ### 0 = blank space (non-useable)
        (r'\b1\b', '1' ,'_'),        ### 1 = floor tile (walkable)
        (r'2', '2' ,'#'),            ### 2 = corner tile (non-useable)
        (r'3', '3' ,'#'),            ### 3 = wall tile facing NORTH.
        (r'4', '4' ,'#'),            ### 4 = wall tile facing EAST.
        (r'5', '5' ,'#'),            ### 5 = wall tile facing SOUTH.
        (r'6', '6' ,'#'),            ### 6 = wall tile facing WEST.
        (r'7', '7' ,'D'),            ### 7 = door tile.
        (r'8', '8' ,'^'),            ### 8 = stairs leading to a higher lever in the dungeon.
        (r'9', '9' ,'v'),              ### 9 = stairs leading to a lower level in the dungeon.
        (r'10', '10' ,'~'),            ### 10 = person
        (r'11', '11' ,'_'),            ### 11 = path from up to down staircases (floor tile)                        
        )
    else:
        # patterns = \
        # (
        # (r'\b0\b', '0' ,u'\u2592'),        ### 0 = blank space (non-useable)
        # (r'\b1\b', '1' ,u'\u2591'),        ### 1 = floor tile (walkable)
        # (r'2', '2' ,u'\u2593'),            ### 2 = corner tile (non-useable)
        # (r'3', '3' ,u'\u2593'),            ### 3 = wall tile facing NORTH.
        # (r'4', '4' ,u'\u2593'),            ### 4 = wall tile facing EAST.
        # (r'5', '5' ,u'\u2593'),            ### 5 = wall tile facing SOUTH.
        # (r'6', '6' ,u'\u2593'),            ### 6 = wall tile facing WEST.
        # (r'7', '7' ,'D'),                ### 7 = door tile.
        # (r'8', '8' ,u'\u25B2'),            ### 8 = stairs leading to a higher lever in the dungeon.
        # (r'9', '9' ,u'\u25BC'),          ### 9 = stairs leading to a lower level in the dungeon.
        # (r'10', '10' , u'\u263A'),                ### 10 = person
        # (r'11', '11' ,u'\u2591'),        ### 11 = path from up to down staircases (floor tile)                        
        # )
        patterns = \
        (
        (r'\b0\b', '0' ,u'\u25A6'),        ### 0 = blank space (non-useable)
        (r'\b1\b', '1' ,u'\u25A2'),        ### 1 = floor tile (walkable)
        (r'2', '2' ,u'\u25A3'),            ### 2 = corner tile (non-useable)
        (r'3', '3' ,u'\u25A3'),            ### 3 = wall tile facing NORTH.
        (r'4', '4' ,u'\u25A3'),            ### 4 = wall tile facing EAST.
        (r'5', '5' ,u'\u25A3'),            ### 5 = wall tile facing SOUTH.
        (r'6', '6' ,u'\u25A3'),            ### 6 = wall tile facing WEST.
        (r'7', '7' ,'D'),                ### 7 = door tile.
        (r'8', '8' ,u'\u25B2'),            ### 8 = stairs leading to a higher lever in the dungeon.
        (r'9', '9' ,u'\u25BC'),          ### 9 = stairs leading to a lower level in the dungeon.
        (r'10', '10' , u'\u263B'),                ### 10 = person
        (r'11', '11' ,u'\u25A2'),        ### 11 = path from up to down staircases (floor tile)                        
        )
        
        
    sStatus = ''
    mapGen = new_dungeon.test_out(True)
    for i in mapGen:
        #print '\n',
        # sStatus = ' '.join([sStatus])
        sStatus = "\n".join([sStatus,u'\u00A0'])
        for eachTile in i:
            #print eachTile
            # tileList = map(buildRule, patterns)
            tileList = list(itertools.starmap(buildRule, patterns))
            for tile in tileList:
                sOut = tile(str(eachTile))
                if sOut: 
                    #print sOut,
                    sStatus = ''.join([sStatus,sOut])
        # sStatus = "\n".join([sStatus])    
    return "".join(["You are here:",sStatus])

def Status20(debug=0,strIn=None):
    # print("got to here")
    lang_options = \
        (
        ("Dwarven","lang_dwarven"),
        ("Goblin","lang_goblin"),
        ("Elven", "lang_elfish"),
        ("Orcish","lang_orcish"),
        ("Draconic","lang_draconic"),
        ("Lizardfolk","lang_lizard"),
        ("R'lyeh","lang_chth"),
        )
    
    language = random.choice(lang_options)
    language_called = language[0]
    language_type = language[1]
    
    # print("silly: ", SillyTrans(language_type, strIn))
    
    if strIn is not None:
        #just translate the strIn
        strOut = "Your tweet in %s: \"%s\"" % (language_called, SillyTrans(language_type, strIn) )
    else:
        fake_name = FlavorfulProperNoun()
        # print("fake name: ", fake_name)
        name_out = SillyTrans(language_type, fake_name).replace(' ','-').title()
        random_word_list = []
        random_word_list.extend(list(filter(None, shPlaces.col_values(0,1))))
        random_word_list.extend(list(filter(None, shPlaces.col_values(1,1))))
        random_word_list.extend(list(filter(None, shPlaces.col_values(2,1))))
        random_word_list.extend(list(filter(None, shPlaces.col_values(4,1))))
        random_word_list.extend(list(filter(None, shPlaces.col_values(5,1))))
        random_word_list.extend(list(filter(None, shPlaces.col_values(8,1))))
        random_word = random.choice(random_word_list)
        
        translated_word = SillyTrans(language_type, random_word)
        
        strOpt = []
        strOpt.append("The common %s name \"%s\' is usually translated as \"%s\"." % (language_called, fake_name, name_out) )
        strOpt.append("The name %s means %s in the %s tongue." % (name_out, fake_name, language_called) )
        strOpt.append("\"%s\" means \"%s\" in %s." % (translated_word.title(), random_word, language_called) )
                
        strOut = random.choice(strOpt)
        
    return strOut
    
def Status21(debug=0,strIn=None):
    strOut = "Help me make this bot better. Please consider supporting via patreon: https://www.patreon.com/yourdm. Sorry for the ad, thank you, sorry."
    return strOut
    
def Status22(debug=0, strIn=None):
    new_place = Swath((9,7))
    new_place.generate_swath(biome=None)
    new_place.pick_travelers()
    strOut = new_place.prepare_swath()
    return strOut
    
# def Status23(debug=0, strIn=None):
    ### MAZE THING
    # w = 5
    # h = 4
    # vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    # ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    # hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
 
    # def walk(x, y):
        # vis[y][x] = 1
 
        # d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        # random.shuffle(d)
        # for (xx, yy) in d:
            # if vis[yy][xx]: continue
            # if xx == x: hor[max(y, yy)][x] = "+  "
            # if yy == y: ver[y][max(x, xx)] = "   "
            # walk(xx, yy)
 
    # walk(random.randrange(w), random.randrange(h))
 
    # s = ""
    # for (a, b) in zip(hor, ver):
        # s += ''.join(a + ['\n'] + b + ['\n'])
    # return s
    
def StatusMaker(debug=0,force=None,strIn=None, nforce=None):

    optID = [
            [Status00,.015],    ### Goals
            [Status01,.004],    ### Attacks                     #fixed with plural problems?
            [Status02,.041],    ### AREA DESC LONG
            [Status03,.018],    ### AREA DESC SHORT
            [Status04,.006],    ### SHOP ADS
            [Status05,.005],    ### DOUBTFUL SHOP
            [Status06,.010],    ### drinking                    #broken b' (fixed)
            [Status07,.008],    ### YOU POTIONS
            [Status08,.011],    ### KING REPORT                 #broken (fixed?)
            [Status09,.022],    ### YOU KING                    #broken (fixed?)
            [Status10,.017],    ### STATUSED BY A WIZARD
            [Status11,.003],    ### Ability Limitations
            [Status12,.056],    ### Bits and Pieces
            [Status13,.030],    ### Goofy Book Review shit      #broken b' (fixed?)
            [Status14,.025],    ### GIBBERISH
            [Status15,.045],    ### LOST CIVILIZATION
            [Status16,.016],    ### PORTALS                     #broken (fixed)
            [Status17,.020],    ### LAWS                        #broken (fixed)
            [Status18,.013],    ### staying at an inn
            [Status19,.019],    ### MAP!!!                      #broken (fixed??! +good fonts for twtitter)
            [Status20,.014],    ### Fantasy words               #broken
            [Status21,.002],    ### Patreon Ad
            [Status22,.600],    ### EMOJI FIELD
            ]    

    # testout = pick_random(optID)
    # print("testout: ", testout.__name__, ": ", testout(debug))
    
    testout = pick_random(optID)

    if force is None:
        if nforce is None:
            strUpdate = testout(debug=debug, strIn=strIn)
        else:
            while testout.__name__ == "Status" + str(nforce):
                print("force match!")
                testout = pick_random(optID) #pick again
            strUpdate = testout(debug=debug, strIn=strIn)
    else:
        if force != nforce:
            testout = optID[force][0](debug=debug,strIn=strIn)
            strUpdate = testout
        else:
            print("skip")
            strUpdate = "I have been critically injured!"
            
    return strUpdate

# if __name__ == '__main__':
    # for i in range(21):
       # s = StatusMaker(force=i)
       # print(i, ": ", s)
