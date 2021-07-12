import random
import time
import twitter, os
import unicodedata
from collections import Counter
from YDM_tools import *


######################################################################################
##                                                                                  ##
##                  @DMTester_ twitter credentials do not share!!!!                 ##
##                                                                                  ##
######################################################################################


TOKEN = r'G:\yourdm\setup\token_DMtester.txt'
tokens= []
with open(TOKEN, 'r') as fp:
    ftokens = fp.readlines()
    
for i in ftokens:
    tokens.append(i.strip())
    # print(i)

api=twitter.Api(consumer_key = tokens[2],
                consumer_secret = tokens[4],
                access_token_key= tokens[6],
                access_token_secret= tokens[8]) 
                
######################################################################################
##                                                                                  ##
##                  @DMTester_ twitter credentials do not share!!!!                 ##
##                                                                                  ##
######################################################################################
e_mage = (
    '\U0001F9D9' '\U0000200D' '\U00002642' '\U0000FE0F',    #man mage
    '\U0001F9D9' '\U0000200D' '\U00002640' '\U0000FE0F',    #woman mage
    '\U0001F9D9' '\U0001F3FC',  #; RGI_Emoji_Modifier_Sequence  ; mage: medium-light skin tone                                   # E5.0   [1] (🧙🏼)
    '\U0001F9D9' '\U0001F3FD',  #; RGI_Emoji_Modifier_Sequence  ; mage: medium skin tone                                         # E5.0   [1] (🧙🏽) 
    '\U0001F9D9' '\U0001F3FE',  #; RGI_Emoji_Modifier_Sequence  ; mage: medium-dark skin tone                                    # E5.0   [1] (🧙🏾)
    '\U0001F9D9' '\U0001F3FF'   #; RGI_Emoji_Modifier_Sequence  ; mage: dark skin tone                                           # E5.0   [1] (🧙🏿)
)

e_fairy = (
    '\U0001F9DA' '\U0000200D' '\U00002642' '\U0000FE0F',	#man fairy
    '\U0001F9DA' '\U0000200D' '\U00002640' '\U0000FE0F',	#woman fairy
    '\U0001F9DA' '\U0001F3FC',   #; RGI_Emoji_Modifier_Sequence  ; fairy: medium-light skin tone                                  # E5.0   [1] (🧚🏼)
    '\U0001F9DA' '\U0001F3FD',   #; RGI_Emoji_Modifier_Sequence  ; fairy: medium skin tone                                        # E5.0   [1] (🧚🏽)
    '\U0001F9DA' '\U0001F3FE',   #; RGI_Emoji_Modifier_Sequence  ; fairy: medium-dark skin tone                                   # E5.0   [1] (🧚🏾)
    '\U0001F9DA' '\U0001F3FF',   #; RGI_Emoji_Modifier_Sequence  ; fairy: dark skin tone                                          # E5.0   [1] (🧚🏿)
)    
    
e_vampire = (
    '\U0001F9DB' '\U0000200D' '\U00002642' '\U0000FE0F',    #man vampire
    '\U0001F9DB' '\U0000200D' '\U00002640' '\U0000FE0F',    #woman vampire
    '\U0001F9DB' '\U0001F3FB',   #; RGI_Emoji_Modifier_Sequence  ; vampire: light skin tone                                       # E5.0   [1] (🧛🏻)
    '\U0001F9DB' '\U0001F3FC',   #; RGI_Emoji_Modifier_Sequence  ; vampire: medium-light skin tone                                # E5.0   [1] (🧛🏼)
    '\U0001F9DB' '\U0001F3FD',   #; RGI_Emoji_Modifier_Sequence  ; vampire: medium skin tone                                      # E5.0   [1] (🧛🏽)
    '\U0001F9DB' '\U0001F3FE',   #; RGI_Emoji_Modifier_Sequence  ; vampire: medium-dark skin tone                                 # E5.0   [1] (🧛🏾)
    '\U0001F9DB' '\U0001F3FF',   #; RGI_Emoji_Modifier_Sequence  ; vampire: dark skin tone                                        # E5.0   [1] (🧛🏿)
)

e_merfolk = (
    '\U0001F9DC' '\U0001F3FB',   #; RGI_Emoji_Modifier_Sequence  ; merperson: light skin tone                                     # E5.0   [1] (🧜🏻)
    '\U0001F9DC' '\U0001F3FC',   #; RGI_Emoji_Modifier_Sequence  ; merperson: medium-light skin tone                              # E5.0   [1] (🧜🏼)
    '\U0001F9DC' '\U0001F3FD',   #; RGI_Emoji_Modifier_Sequence  ; merperson: medium skin tone                                    # E5.0   [1] (🧜🏽)
    '\U0001F9DC' '\U0001F3FE',   #; RGI_Emoji_Modifier_Sequence  ; merperson: medium-dark skin tone                               # E5.0   [1] (🧜🏾)
    '\U0001F9DC' '\U0001F3FF',   #; RGI_Emoji_Modifier_Sequence  ; merperson: dark skin tone                                      # E5.0   [1] (🧜🏿)
)

e_elf = (
    '\U0001F9DD',# '\U0000F3FB',   #; RGI_Emoji_Modifier_Sequence  ; elf: light skin tone                                           # E5.0   [1] (🧝🏻)
    '\U0001F9DD' '\U0001F3FC',   #; RGI_Emoji_Modifier_Sequence  ; elf: medium-light skin tone                                    # E5.0   [1] (🧝🏼)
    '\U0001F9DD' '\U0001F3FD',   #; RGI_Emoji_Modifier_Sequence  ; elf: medium skin tone                                          # E5.0   [1] (🧝🏽)
    '\U0001F9DD' '\U0001F3FE',   #; RGI_Emoji_Modifier_Sequence  ; elf: medium-dark skin tone                                     # E5.0   [1] (🧝🏾)
    '\U0001F9DD' '\U0001F3FF',   #; RGI_Emoji_Modifier_Sequence  ; elf: dark skin tone                                            # E5.0   [1] (🧝🏿)
)

e_silly = (
    '\U0001F921', #clown
    '\U0001F47B', #ghost
    '\U0001F47D', #alien
    '\U0001F47E', #alien monster
    '\U0001F916', #robot
)

e_animals = (
    '\U0001F435',   #monkey face
    '\U0001F412',   #monkey
    '\U0001F98D',   #gorilla
    '\U0001F9A7',   #orangutan
    '\U0001F436',   #dog face
    '\U0001F415',   #dog
    '\U0001F9AE',   #guide dog
    '\U0001F415' '\U0000F9BA',   #service dog
    '\U0001F429',   #poodle
    '\U0001F43A',   #wolf
    '\U0001F98A',   #fox
    '\U0001F99D',   #raccoon
    '\U0001F431',   #cat face
    '\U0001F408',   #cat
    '\U0001F408' '\U00002B1B',   #black cat
    '\U0001F981',   #lion
    '\U0001F42F',   #tiger face
    '\U0001F405',   #tiger
    '\U0001F406',   #leopard
    '\U0001F434',   #horse face
    '\U0001F40E',   #horse
    '\U0001F984',   #unicorn
    '\U0001F993',   #zebra
    '\U0001F98C',   #deer
    '\U0001F9AC',   #bison
    '\U0001F42E',   #cow face
    '\U0001F402',   #ox
    '\U0001F403',   #water buffalo
    '\U0001F404',   #cow
    '\U0001F437',   #pig face
    '\U0001F416',   #pig
    '\U0001F417',   #boar
    '\U0001F43D',   #pig nose
    '\U0001F40F',   #ram
    '\U0001F411',   #ewe
    '\U0001F410',   #goat
    '\U0001F42A',   #camel
    '\U0001F42B',   #two-hump camel
    '\U0001F999',   #llama
    '\U0001F992',   #giraffe
    '\U0001F418',   #elephant
    '\U0001F9A3',   #mammoth
    '\U0001F98F',   #rhinoceros
    '\U0001F99B',   #hippopotamus
    '\U0001F42D',   #mouse face
    '\U0001F401',   #mouse
    '\U0001F400',   #rat
    '\U0001F439',   #hamster
    '\U0001F430',   #rabbit face
    '\U0001F407',   #rabbit
    '\U0001F43F',   #chipmunk
    '\U0001F9AB',   #beaver
    '\U0001F994',   #hedgehog
    '\U0001F987',   #bat
    '\U0001F43B',   #bear
    '\U0001F43B' '\U0000200D' '\U00002744' '\U0000FE0F',   #polar bear
    '\U0001F428',   #koala
    '\U0001F43C',   #panda
    '\U0001F9A5',   #sloth
    '\U0001F9A6',   #otter
    '\U0001F9A8',   #skunk
    '\U0001F998',   #kangaroo
    '\U0001F9A1',   #badger
    '\U0001F414',   #chicken
    '\U0001F413',   #rooster
    '\U0001F423',   #hatching chick
    '\U0001F424',   #baby chick
    '\U0001F425',   #front-facing baby chick
    '\U0001F426',   #bird
    '\U0001F427',   #penguin
    '\U0001F54A',   #dove
    '\U0001F985',   #eagle
    '\U0001F986',   #duck
    '\U0001F9A2',   #swan
    '\U0001F989',   #owl
    '\U0001F9A4',   #dodo
    '\U0001FAB6',   #feather
    '\U0001F9A9',   #flamingo
    '\U0001F99A',   #peacock
    '\U0001F99C',   #parrot
    '\U0001F438',   #frog
    '\U0001F40A',   #crocodile
    '\U0001F422',   #turtle
    '\U0001F98E',   #lizard
    '\U0001F40D',   #snake
    '\U0001F432',   #dragon face
    '\U0001F409',   #dragon
    '\U0001F995',   #sauropod
    '\U0001F996',   #T-Rex
    '\U0001F40C',   #snail
    '\U0001F98B',   #butterfly
    '\U0001F41B',   #bug
    '\U0001F41C',   #ant
    '\U0001F41D',   #honeybee
    '\U0001FAB2',   #beetle
    '\U0001F41E',   #lady beetle
    '\U0001F997',   #cricket
    '\U0001FAB3',   #cockroach
    '\U0001F577',   #spider
    '\U0001F578',   #spider web
    '\U0001F982',   #scorpion
    '\U0001F99F',   #mosquito
    '\U0001FAB0',   #fly
    '\U0001FAB1',   #worm
    '\U0001F9A0',   #microbe
)

e_sea_animal = (
    '\U0001F980',   #crab
    '\U0001F99E',   #lobster
    '\U0001F990',   #shrimp
    '\U0001F991',   #squid
    '\U0001F9AA',   #oyster
    '\U0001F433',   #spouting whale
    '\U0001F40B',   #whale
    '\U0001F42C',   #dolphin
    '\U0001F9AD',   #seal
    '\U0001F41F',   #fish
    '\U0001F420',   #tropical fish
    '\U0001F421',   #blowfish
    '\U0001F988',   #shark
    '\U0001F419',   #octopus
    '\U0001F41A',   #spiral shell
)

e_3monkey = (
    '\U0001F648',   #see-no-evil monkey
    '\U0001F649',   #hear-no-evil monkey
    '\U0001F64A',   #speak-no-evil monkey
)

e_genie = (
    '\U0001F9DE',   #genie
    '\U0001F9DE' '\U0000200D' '\U00002642' '\U0000FE0F',   #man genie
    '\U0001F9DE' '\U0000200D' '\U00002640' '\U0000FE0F',   #woman genie

)

e_zombie = (
    '\U0001F9DF',   #zombie
    '\U0001F9DF' '\U0000200D' '\U00002642' '\U0000FE0F',   #man zombie
    '\U0001F9DF' '\U0000200D' '\U00002640' '\U0000FE0F',   #woman zombie

)

e_traveler = (
    '\U0001F9D4' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: light skin tone, beard                                 # E5.0   [1] (🧔🏻)
    '\U0001F9D4' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: medium-light skin tone, beard                          # E5.0   [1] (🧔🏼)
    '\U0001F9D4' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: medium skin tone, beard                                # E5.0   [1] (🧔🏽)
    '\U0001F9D4' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: medium-dark skin tone, beard                           # E5.0   [1] (🧔🏾)
    '\U0001F9D4' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: dark skin tone, beard                                  # E5.0   [1] (🧔🏿)
    '\U0001F9D5' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman with headscarf: light skin tone                          # E5.0   [1] (🧕🏻)
    '\U0001F9D5' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman with headscarf: medium-light skin tone                   # E5.0   [1] (🧕🏼)
    '\U0001F9D5' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman with headscarf: medium skin tone                         # E5.0   [1] (🧕🏽)
    '\U0001F9D5' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman with headscarf: medium-dark skin tone                    # E5.0   [1] (🧕🏾)
    '\U0001F9D5' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman with headscarf: dark skin tone                           # E5.0   [1] (🧕🏿)
    '\U0001F9D3' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; older person: light skin tone                                  # E5.0   [1] (🧓🏻)
    '\U0001F9D3' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; older person: medium-light skin tone                           # E5.0   [1] (🧓🏼)
    '\U0001F9D3' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; older person: medium skin tone                                 # E5.0   [1] (🧓🏽)
    '\U0001F9D3' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; older person: medium-dark skin tone                            # E5.0   [1] (🧓🏾)
    '\U0001F9D3' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; older person: dark skin tone                                   # E5.0   [1] (🧓🏿)
    '\U0001F9CF' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; deaf person: light skin tone                                   # E12.0  [1] (🧏🏻)
    '\U0001F9CF' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; deaf person: medium-light skin tone                            # E12.0  [1] (🧏🏼)
    '\U0001F9CF' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; deaf person: medium skin tone                                  # E12.0  [1] (🧏🏽)
    '\U0001F9CF' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; deaf person: medium-dark skin tone                             # E12.0  [1] (🧏🏾)
    '\U0001F9CF' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; deaf person: dark skin tone                                    # E12.0  [1] (🧏🏿)
    '\U0001F934' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; prince: light skin tone                                        # E3.0   [1] (🤴🏻)
    '\U0001F934' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; prince: medium-light skin tone                                 # E3.0   [1] (🤴🏼)
    '\U0001F934' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; prince: medium skin tone                                       # E3.0   [1] (🤴🏽)
    '\U0001F934' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; prince: medium-dark skin tone                                  # E3.0   [1] (🤴🏾)
    '\U0001F934' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; prince: dark skin tone                                         # E3.0   [1] (🤴🏿)
    '\U0001F64D' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; person frowning: light skin tone                               # E1.0   [1] (🙍🏻)
    '\U0001F64D' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; person frowning: medium-light skin tone                        # E1.0   [1] (🙍🏼)
    '\U0001F64D' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; person frowning: medium skin tone                              # E1.0   [1] (🙍🏽)
    '\U0001F64D' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; person frowning: medium-dark skin tone                         # E1.0   [1] (🙍🏾)
    '\U0001F64D' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; person frowning: dark skin tone                                # E1.0   [1] (🙍🏿)
    '\U0001F64E' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; person pouting: light skin tone                                # E1.0   [1] (🙎🏻)
    '\U0001F64E' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; person pouting: medium-light skin tone                         # E1.0   [1] (🙎🏼)
    '\U0001F64E' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; person pouting: medium skin tone                               # E1.0   [1] (🙎🏽)
    '\U0001F64E' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; person pouting: medium-dark skin tone                          # E1.0   [1] (🙎🏾)
    '\U0001F64E' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; person pouting: dark skin tone                                 # E1.0   [1] (🙎🏿)
    '\U0001F575' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; detective: light skin tone                                     # E2.0   [1] (🕵🏻)
    '\U0001F575' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; detective: medium-light skin tone                              # E2.0   [1] (🕵🏼)
    '\U0001F575' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; detective: medium skin tone                                    # E2.0   [1] (🕵🏽)
    '\U0001F575' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; detective: medium-dark skin tone                               # E2.0   [1] (🕵🏾)
    '\U0001F575' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; detective: dark skin tone                                      # E2.0   [1] (🕵🏿)
    '\U0001F482' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; guard: light skin tone                                         # E1.0   [1] (💂🏻)
    '\U0001F482' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; guard: medium-light skin tone                                  # E1.0   [1] (💂🏼)
    '\U0001F482' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; guard: medium skin tone                                        # E1.0   [1] (💂🏽)
    '\U0001F482' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; guard: medium-dark skin tone                                   # E1.0   [1] (💂🏾)
    '\U0001F482' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; guard: dark skin tone                                          # E1.0   [1] (💂🏿)
    '\U0001F483' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman dancing: light skin tone                                 # E1.0   [1] (💃🏻)
    '\U0001F483' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman dancing: medium-light skin tone                          # E1.0   [1] (💃🏼)
    '\U0001F483' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman dancing: medium skin tone                                # E1.0   [1] (💃🏽)
    '\U0001F483' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman dancing: medium-dark skin tone                           # E1.0   [1] (💃🏾)
    '\U0001F483' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; woman dancing: dark skin tone                                  # E1.0   [1] (💃🏿)
    '\U0001F478' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; princess: light skin tone                                      # E1.0   [1] (👸🏻)
    '\U0001F478' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; princess: medium-light skin tone                               # E1.0   [1] (👸🏼)
    '\U0001F478' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; princess: medium skin tone                                     # E1.0   [1] (👸🏽)
    '\U0001F478' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; princess: medium-dark skin tone                                # E1.0   [1] (👸🏾)
    '\U0001F478' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; princess: dark skin tone                                       # E1.0   [1] (👸🏿)
    '\U0001F471' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: light skin tone, blond hair                            # E1.0   [1] (👱🏻)
    '\U0001F471' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: medium-light skin tone, blond hair                     # E1.0   [1] (👱🏼)
    '\U0001F471' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: medium skin tone, blond hair                           # E1.0   [1] (👱🏽)
    '\U0001F471' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: medium-dark skin tone, blond hair                      # E1.0   [1] (👱🏾)
    '\U0001F471' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; person: dark skin tone, blond hair                             # E1.0   [1] (👱🏿)
    '\U0001F472' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; person with skullcap: light skin tone                          # E1.0   [1] (👲🏻)
    '\U0001F472' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; person with skullcap: medium-light skin tone                   # E1.0   [1] (👲🏼)
    '\U0001F472' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; person with skullcap: medium skin tone                         # E1.0   [1] (👲🏽)
    '\U0001F472' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; person with skullcap: medium-dark skin tone                    # E1.0   [1] (👲🏾)
    '\U0001F472' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; person with skullcap: dark skin tone                           # E1.0   [1] (👲🏿)
    '\U0001F473' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; person wearing turban: light skin tone                         # E1.0   [1] (👳🏻)
    '\U0001F473' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; person wearing turban: medium-light skin tone                  # E1.0   [1] (👳🏼)
    '\U0001F473' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; person wearing turban: medium skin tone                        # E1.0   [1] (👳🏽)
    '\U0001F473' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; person wearing turban: medium-dark skin tone                   # E1.0   [1] (👳🏾)
    '\U0001F473' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; person wearing turban: dark skin tone                          # E1.0   [1] (👳🏿)
    '\U0001F474' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; old man: light skin tone                                       # E1.0   [1] (👴🏻)
    '\U0001F474' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; old man: medium-light skin tone                                # E1.0   [1] (👴🏼)
    '\U0001F474' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; old man: medium skin tone                                      # E1.0   [1] (👴🏽)
    '\U0001F474' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; old man: medium-dark skin tone                                 # E1.0   [1] (👴🏾)
    '\U0001F474' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; old man: dark skin tone                                        # E1.0   [1] (👴🏿)
    '\U0001F475' '\U0001F3FB' ,    # ; RGI_Emoji_Modifier_Sequence  ; old woman: light skin tone                                     # E1.0   [1] (👵🏻)
    '\U0001F475' '\U0001F3FC' ,    # ; RGI_Emoji_Modifier_Sequence  ; old woman: medium-light skin tone                              # E1.0   [1] (👵🏼)
    '\U0001F475' '\U0001F3FD' ,    # ; RGI_Emoji_Modifier_Sequence  ; old woman: medium skin tone                                    # E1.0   [1] (👵🏽)
    '\U0001F475' '\U0001F3FE' ,    # ; RGI_Emoji_Modifier_Sequence  ; old woman: medium-dark skin tone                               # E1.0   [1] (👵🏾)
    '\U0001F475' '\U0001F3FF' ,    # ; RGI_Emoji_Modifier_Sequence  ; old woman: dark skin tone                                      # E1.0   [1] (👵🏿)
    '\U0001F468' '\U0000200D' '\U0001F9AF',     #man with white cane	
    '\U0001F9D1' '\U0000200D' '\U0001F9AF',     #person with white cane	
    '\U0001F469' '\U0000200D' '\U0001F9AF',     #woman with white cane	
    '\U0001F9D1' '\U0000200D' '\U0001F9BC',     #person in motor chair	
    '\U0001F468' '\U0000200D' '\U0001F9BC',     #man in motor chair
    '\U0001F469' '\U0000200D' '\U0001F9BC',     #woman in motor chair	
    '\U0001F9D1' '\U0000200D' '\U0001F9BD',     #person in wheel chair
    '\U0001F468' '\U0000200D' '\U0001F9BD',     #man in wheel chair
    '\U0001F469' '\U0000200D' '\U0001F9BD'     #woman in wheel chair
)

e_desert = (
    '\U0001F3DC' '\U0000FE0F' ,    #; Basic_Emoji                  ; desert                                                         # E0.7   [1] (🏜️)
    '\U0001F3DD' '\U0000FE0F' ,    #; Basic_Emoji                  ; desert island                                                  # E0.7   [1] (🏝️)
    '\U0001F3D6' '\U0000FE0F' ,    #; Basic_Emoji                  ; beach with umbrella                                            # E0.7   [1] (🏖️)
    '\U0001F334',   #palm tree
    '\U0001F335'   #cactus
)

e_treats = (
    '\U0001F366',   #soft ice cream
    '\U0001F367',   #shaved ice
    '\U0001F368',   #ice cream
    '\U0001F369',   #doughnut
    '\U0001F36A',   #cookie
    '\U0001F382',   #birthday cake
    '\U0001F370',   #shortcake
    '\U0001F9C1',   #cupcake
    '\U0001F967',   #pie
    '\U0001F36B',   #chocolate bar
    '\U0001F36C',   #candy
    '\U0001F36D',   #lollipop
    '\U0001F36E',   #custard
    '\U0001F36F',   #honey pot
    '\U0001F96E',   #moon cake
    '\U0001F361',   #dango
    '\U0001F960',   #fortune cookie
)

e_forest = (
    '\U0001F331',   #seedling
    '\U0001F332',   #evergreen tree
    '\U0001F333',   #deciduous tree
    '\U0001F33E',   #sheaf of rice
    '\U0001F33F',   #herb
    '\U00002618',   #shamrock
    '\U0001F340',   #four leaf clover
    '\U0001F343',  #leaf fluttering in wind
    '\U0001FAB5'   #wood
)
    
e_forest_aut = (
    '\U0001F341',   #maple leaf
    '\U0001F342',   #fallen leaf
    '\U0001F343'   #leaf fluttering in wind
)

e_plant = (
    '\U0001F331',   #seedling
    '\U0001FAB4',   #potted plant
    '\U0001F332',   #evergreen tree
    '\U0001F333',   #deciduous tree
    '\U0001F334',   #palm tree
    '\U0001F335',   #cactus
    '\U0001F33E',   #sheaf of rice
    '\U0001F33F',   #herb
    '\U00002618',   #shamrock
    '\U0001F340',   #four leaf clover
    '\U0001F341',   #maple leaf
    '\U0001F342',   #fallen leaf
    '\U0001F343'   #leaf fluttering in wind
)

e_mountains = (
    '\U0001F3D4',   #snow-capped mountain
    '\U000026F0',   #mountain
    '\U0001F30B',   #volcano
    '\U0001F5FB',   #mount fuji
    '\U0001F3D5',   #camping
    '\U000026FA',   #tent
    '\U0001F3DE',   #national park
    '\U0001F304'   #sunrise over mountains
)

e_sky = (
    '\U0001F324' '\U0000FE0F' ,    #; Basic_Emoji                  ; sun behind small cloud                                         # E0.7   [1] (🌤️)
    '\U0001F325' '\U0000FE0F' ,    #; Basic_Emoji                  ; sun behind large cloud                                         # E0.7   [1] (🌥️)
    '\U0001F326' '\U0000FE0F' ,    #; Basic_Emoji                  ; sun behind rain cloud                                          # E0.7   [1] (🌦️)
    '\U0001F327' '\U0000FE0F' ,    #; Basic_Emoji                  ; cloud with rain                                                # E0.7   [1] (🌧️)
    '\U0001F328' '\U0000FE0F' ,    #; Basic_Emoji                  ; cloud with snow                                                # E0.7   [1] (🌨️)
    '\U0001F329' '\U0000FE0F' ,    #; Basic_Emoji                  ; cloud with lightning                                           # E0.7   [1] (🌩️)
    '\U0001F32A' '\U0000FE0F' ,    #; Basic_Emoji                  ; tornado                                                        # E0.7   [1] (🌪️)
    # '\U0001F32B' '\U0000FE0F' ,    #; Basic_Emoji                  ; fog                                                            # E0.7   [1] (🌫️)
    # '\U00002744' '\U00000E0F' ,    # Basic_Emoji                  ; snowflake                                                      # E0.6   [1] (❄️)
    '\U00002744',    # Basic_Emoji                  ; snowflake                                                      # E0.6   [1] (❄️)
    #'\U00002708',    # Basic_Emoji                  ; airplane                                                       # E0.6   [1] (✈️)
    '\U00002600',    # Basic_Emoji                  ; sun                                                            # E0.6   [1] (☀️)
    '\U00002601',    # Basic_Emoji                  ; cloud                                                          # E0.6   [1] (☁️)
    '\U0001F308'   #rainbow
)

e_city = (
    '\U0001F3DF',   #stadium
    '\U0001F3DB',   #classical building
    '\U0001F3D7',   #building construction
    '\U0001F3D8',   #houses
    '\U0001F3DA',   #derelict house
    '\U0001F3E0',   #house
    '\U0001F3E1',   #house with garden
    '\U0001F3E2',   #office building
    '\U0001F3E3',   #Japanese post office
    '\U0001F3E4',   #post office
    '\U0001F3E5',   #hospital
    '\U0001F3E6',   #bank
    '\U0001F3E8',   #hotel
    '\U0001F3E9',   #love hotel
    '\U0001F3EA',   #convenience store
    '\U0001F3EB',   #school
    '\U0001F3EC',   #department store
    '\U0001F3ED',   #factory
    '\U0001F3EF',   #Japanese castle
    '\U0001F3F0',   #castle
    '\U0001F492',   #wedding
    '\U000026EA',   #church
    '\U0001F54C',   #mosque
    '\U0001F6D5',   #hindu temple
    '\U0001F54D',   #synagogue
    '\U000026E9',   #shinto shrine
    '\U0001F54B',   #kaaba
    '\U000026F2',   #fountain
    '\U0001F301',   #foggy
    '\U0001F303',   #night with stars
    '\U0001F3D9',   #cityscape
    '\U0001F305',   #sunrise
    '\U0001F306',   #cityscape at dusk
    '\U0001F307',   #sunset
    '\U0001F309'   #bridge at night
)

e_lab = (
    '\U00002696',    # Basic_Emoji                  ; balance scale                                                  # E1.0   [1] (⚖️)
    '\U00002697',    # Basic_Emoji                  ; alembic                                                        # E1.0   [1] (⚗️)
    '\U0001F9EA',   #test tube
    '\U0001F9EB',   #petri dish
    '\U0001F9EC',   #dna
    '\U0001F52C',   #microscope
    '\U0001F52D',   #telescope
    '\U0001F4E1'   #satellite antenna
)

e_flowers = (
    '\U0001F490',   #bouquet
    '\U0001F338',   #cherry blossom
    '\U0001F4AE',   #white flower
    '\U0001F3F5',   #rosette
    '\U0001F339',   #rose
    '\U0001F940',   #wilted flower
    '\U0001F33A',   #hibiscus
    '\U0001F33B',   #sunflower
    '\U0001F33C',   #blossom
    '\U0001F337'   #tulip
)

e_clocks = (
    '\U0000231B',   #hourglass done
    '\U000023F3',   #hourglass not done
    '\U0000231A',   #watch
    '\U000023F0',   #alarm clock
    '\U000023F1',   #stopwatch
    '\U000023F2',   #timer clock
    '\U0001F570',   #mantelpiece clock
    '\U0001F55B',   #twelve o’clock
    '\U0001F567',   #twelve-thirty
    '\U0001F550',   #one o’clock
    '\U0001F55C',   #one-thirty
    '\U0001F551',   #two o’clock
    '\U0001F55D',   #two-thirty
    '\U0001F552',   #three o’clock
    '\U0001F55E',   #three-thirty
    '\U0001F553',   #four o’clock
    '\U0001F55F',   #four-thirty
    '\U0001F554',   #five o’clock
    '\U0001F560',   #five-thirty
    '\U0001F555',   #six o’clock
    '\U0001F561',   #six-thirty
    '\U0001F556',   #seven o’clock
    '\U0001F562',   #seven-thirty
    '\U0001F557',   #eight o’clock
    '\U0001F563',   #eight-thirty
    '\U0001F558',   #nine o’clock
    '\U0001F564',   #nine-thirty
    '\U0001F559',   #ten o’clock
    '\U0001F565',   #ten-thirty
    '\U0001F55A',   #eleven o’clock
    '\U0001F566'   #eleven-thirty
)

e_space = (
    '\U0001F311',   #new moon
    '\U0001F312',   #waxing crescent moon
    '\U0001F313',   #first quarter moon
    '\U0001F314',   #waxing gibbous moon
    '\U0001F315',   #full moon
    '\U0001F316',   #waning gibbous moon
    '\U0001F317',   #last quarter moon
    '\U0001F318',   #waning crescent moon
    '\U0001F319',   #crescent moon
    '\U0001F31A',   #new moon face
    '\U0001F31B',   #first quarter moon face
    '\U0001F31C',   #last quarter moon face
    '\U00002600',   #sun
    '\U0001F31D',   #full moon face
    '\U0001F31E',   #sun with face
    '\U0001FA90',   #ringed planet
    '\U00002B50',   #star
    '\U0001F31F',   #glowing star
    '\U0001F320',   #shooting star
    '\U0001F30C',   #milky way
    '\U0001F30D',   #globe showing Europe-Africa
    '\U0001F30E',   #globe showing Americas
    '\U0001F30F',   #globe showing Asia-Australia
)

e_blank = (
    '\U000E0020'
)

e_rainbow = (
    '\U0001F308'   #rainbow
)

e_fireworks = (
    '\U0001F386',   #fireworks
    '\U0001F387',   #sparkler
)

class Swath:
    def __init__(self,grid_size_xy):

        self.grid_size = grid_size_xy
        # self.name = name
        self.grid = []
            
    def print_info(self, grid=False):

        print("Printing Dungeon Info...\n\n")
        print("NAME:  " + str(self.name))
        print("SIZE:  " + str(self.grid_size[0]) + "x" + str(self.grid_size[1]))
        if grid:
            for row in self.grid:
                print(row)
		
    def test_out(self, grid=False):
        if grid:
            for row in self.grid:
                yield row
                
    def generate_swath(self, biome=None):
        self.biome = self.pick_biome(biome)
        self.grid = []
        # print("biome:", self.biome)
        for y in range(0, self.grid_size[1]):
            row = []
            for x in range(0, self.grid_size[0]):
                tile = random.choice(self.biome)
                # print("tile: ", tile)
                row.append(tile)
            self.grid.append(row)
        # print(self.grid)
        
    def pick_biome(self, key=None):
        self.biome = []
        # opt = [
            # ["desert", (e_desert)],
            # ["time desert",(e_desert, e_clocks[8:10])],
            # ["forest1", (e_forest)],
            # ["forest2", (e_forest, e_flowers)],
            # ["forest3", (e_forest, e_forest_aut)],
            # ["mountains", (e_forest, e_mountains)],
            # ["city", (e_city)],
            # ["sky", (e_sky)],
            
        # ]
        opt = {
            "desert": (e_desert),
            "time desert":(e_desert, e_clocks[8:10]),
            "forest": (e_forest),
            "spring forest": (e_forest, e_flowers, e_rainbow),
            "autumn forest": (e_forest, e_forest_aut),
            "mountains": (e_forest, e_mountains),
            "city": (e_city),
            "sky": (e_sky),
            "lab": (e_lab),
            "space": (e_space),
            "fireworks": (e_fireworks),
            "dessert desert": (e_treats, e_desert)
        }
        
        if key is not None:
            choice = key, opt[key]#[10] #to select single emojis manually for debugging
            # print(choice)
        else:
            # choice = random.choice(opt)
            choice = random.choice(list(opt.items()))
        
        self.biome_name = choice[0]
        
        # print(choice[0], choice[1])
        for each in choice[1]:
            # print("each: ", each, type(each))
            if type(each) is str: 
                self.biome.append(each)
            else:
                for i in each:
                    self.biome.append(i)
                    # print("biome: ", self.biome)

        return self.biome
        
    def prepare_swath(self):
        strStatus = ''
        for i in self.grid:
            # print(i)
            strStatus = "\n".join([strStatus,u'\u00A0'])
            for eachTile in i:
                # print("eachTile: ", eachTile)
                strStatus = ''.join([strStatus,eachTile])
        # print("Status: ", strStatus)
        
        if self.roster is not None:
            strStatus = "".join([self.roster, strStatus])
            
        return strStatus
        
    def pick_travelers(self):
        count = random.randint(1,5)
        opt = {
            "wizard": (e_mage),
            "fairy": (e_fairy),
            "vampire": (e_vampire),
            "merfolk": (e_merfolk),
            "elf": (e_elf),
            "traveler": (e_traveler)
        }
        
        roster_names = []
        roster_icons = []
        # print(count)
        for each in range(count):
            choice = random.choice(list(opt.items()))
            # print(choice)
            indiv = random.choice(choice[1])
            # print(choice[0], indiv)
            roster_names.append(choice[0])
            roster_icons.append(indiv)
            
            # roster.append(choice)
        c = Counter(roster_names)
        # print(c)
        # print(len(c))
        # print(c[-1])
        
        roster = ''
        i = 0
        # if len(c) == 1:
            # roster = AnAFixer(c[key])
        # else:
        for key in c:
            if i == 0:
                if c[key] > 1:
                    roster = int_to_en(c[key]) + " " + Pluralizer(key)
                    i += 1
                    continue
                else:
                    roster = AnAFixer(key)
                    i += 1
                    continue
            if (i == len(c) - 1):
                if c[key] > 1:
                    # print(int_to_en(c[key]), " ", Pluralizer(key))
                    roster = ', and '.join([roster, int_to_en(c[key]) + " " + Pluralizer(key)])
                    i += 1
                else:
                    # print(key)
                    roster = ', and '.join([roster, AnAFixer(key)])
                    i += 1
            else:
                if c[key] > 1:
                    # print(int_to_en(c[key]), " ", Pluralizer(key))
                    roster = ', '.join([roster, int_to_en(c[key]) + " " + Pluralizer(key)])
                    i += 1
                else:
                    # print(key)
                    roster = ', '.join([roster, AnAFixer(key)])
                    i += 1
        
        jOpt = [
            " travelling through ",
            " lost in ",
            " passing through ",
            " wandering around ",
            " trekking accross ",
            " hiking through ",
            " infiltrating ",
            " cutting accross ",
            " admiring ",
            " sightseeing in ",
            " visiting "
        ]
        
        jsel = random.choice(jOpt)
        
        if self.biome_name == "fireworks":
            jsel = " watching "
        
        if self.biome_name == "space":
            self.roster = roster.title() + jsel + " " + self.biome_name.title()
        else:
            self.roster = roster.title() + jsel + "the " + self.biome_name.title()
        

        j = len(roster_icons)
        k = 3
 
        swath_col = self.grid_size[0]
        swath_row = self.grid_size[1]
        
        # print("grid col: " , swath_col)
        # print("grid row: " , swath_row)
        
        x_pos = int(round(((swath_col - j)/2)))-1
        y_pos = int(round(((swath_row - k)/2)))
        t_x_pos = x_pos + 1
        t_y_pos = y_pos + 1
        
        ex_pos = x_pos + 1
        ey_pos = y_pos - 1
        
        # print("chars = ", j)
        # print(x_pos, y_pos)
        
        # for col in range(j+2):
            # for row in range(k):
                # print(row)
                # x = x_pos + col
                # y = y_pos + row
                # print("x,y: ", x, y)
                # # self.grid[y][x] = e_blank[0]
                # self.grid[y][x] = "      "
                
        for i in range(len(roster_icons)):
            x = t_x_pos + i
            y = t_y_pos
            self.grid[y][x] = roster_icons[i]
            k += 1
            
        self.roster = ''.join([self.roster, self.pick_encounter(x=ex_pos, y=ey_pos)])
        # k = 0-int(round(len(roster_icons)/2))
        # for i in range(len(roster_icons)):
            # x = int(round((self.grid_size[1]-1)/2))
            # y = int(round((self.grid_size[0]-1)/2)+k)
            # self.grid[x][y] = roster_icons[i]
            # k += 1
                    
        
        # print(roster.title(), roster_names, roster_icons)

    def pick_encounter(self, x, y):
        opt = {
                "animals": (e_animals),
                "monsters":(e_silly),
                "genie":(e_genie),
                "3mokey":(e_3monkey),
                "zombie":(e_zombie),
                "sea animal":(e_sea_animal),
        }
        
        choice = random.choice(list(opt.items()))
        indiv = random.choice(choice[1])
        
        # print(name_emoji(indiv))
        
        jOpt = (
            ". There they meet ",
            ", where they find ",
            ", where there lives ",
            ", which is inhabited by ",
            ". They cross paths with ",
            ", where they stumble upon ",
            ", where they are ambushed by ",
            " to visit ",
        )
        
        yOpt = (
            "a famous ",
            "the friendly ",
            "a sleeping ",
            "a giant ",
            "a belligerant ",
            "a drooling ",
            "an agitated ",
            "a nervous ",
            "a happy ",
            "an estatic ",
            "a contended ",
            "a placid ",
            "a pensive ",
            "a timid ",
            "an interesting ",
            "an injured ",
            "a powerful ",
            "a curious ",
            "a mysterious ",
        )
        
        pOpt = (
            ".",
            "!",
            "?!",
            "...",
        )
        
        strOut = ''.join([random.choice(jOpt), random.choice(yOpt), name_emoji(indiv), random.choice(pOpt)])
        
        self.grid[y][x] = indiv
           
        return strOut
            
        
def name_emoji(strIn):
    strOut = ""
    for i in strIn:
        name = unicodedata.name(i)
        for ew in name.split():
            if ew.lower() == "face":
                ew = ""
            strOut = ' '.join([strOut, ew.lower()])
        # print(strOut.strip())
        return strOut.strip()
        
if __name__ == '__main__':
    new_place = Swath((9,7))
    new_place.generate_swath(biome=None)
    new_place.pick_travelers()
    
    api.PostUpdate(new_place.prepare_swath(),verify_status_length=False)
    
    # for i in e_silly:
        # name_emoji(i)