from src.game import Game
from src.board import Board

game = Game()
game.add_player()
player = game.players[0]

def play_stage_one(starting_hand = '', print_hand = False, print_end = False, print_turns = False):
    # reset the board and pouch
    player.board = Board()
    player.hand = ''
    player.playing = False
    if len(starting_hand) > 0:
        player.give_tiles(starting_hand)
    else:
        game.pouch.reset()
        player.give_tiles(game.pouch.get_starting_tiles(21))
    if print_hand:
        print(player.hand)
    go = True
    starting_hand = player.hand
    print("stuff that should be empty")
    print(player.board)
    print(player.board.anchors)
    print("done")
    while(go):
        if player.play_turn() == "Error":
            go = False
        if len(player.board.tiles) >= 21:
            go = False
        if print_turns:
            print('board')
            print(player.board)
            print("hand")
            print(player.hand)
        elif print_end and go == False:
            print(player.board)
            print(player.hand)
    if print_hand:
        print(player.hand)
    return (i, starting_hand, len(player.hand))

results = []
ITERATIONS = 1000
for i in range(ITERATIONS):
    print(f"\n\nRun {i}")
    results.append(play_stage_one())
failures = list(filter(lambda result: result[2] != 0, results))
print(failures)
print(f"{len(failures)} failures out of {ITERATIONS}")

# [(0, 'HANBODAERENGVZFPQTXTA', 1), (14, 'NEEKNFCWUOONEJVTAAARN', 1), (21, 'QESWNGNECREGSIADARAED', 1), (27, 'RYEUSJAQGAVVIAELSDELY', 1), (42, 'XUSOILYQFNNNDHVMENOBT', 1), (49, 'RDUCNOQZWTAEMLVWPDLRO', 1)]
# [(7, 'GIKLVSTDPRDLEOCFIWQIU', 1), (11, 'OVTASBWCESLNXVDREMRTI', 3), (12, 'TWQEQECEIOIUETXENTNJD', 2), (24, 'QLOSPABOQPGEOVERUEZDU', 1), (37, 'AHLTIMVOWYHORSSEJVRTA', 1), (60, 'JHIBIVNBNUENCROGUOTTO', 1), (67, 'NRLIDTVQFCETXAAOANWSL', 1), (79, 'HMQFZTBEGJAERNLNHCMOK', 1), (90, 'QBOLVYZVREAAWRRMTKIVA', 2), (95, 'AOIOOMRROGZGDNESRJAQD', 1), (97, 'DUZAQSRYOVPTDOFFWSUSG', 2)]

# [(2, 'REEDQZSOXAERTETHCGORR', 1), (3, 'AYIOUDGYNTTQOWLIWXFMT', 1), (48, 'SVROLAKROQVJNNIADRRFG', 1), (51, 'AAARAGEODEAQEEILOOIDA', 1), (56, 'EEAFVBTMIEWDEFNHAOVSN', 1), (58, 'MFIBTAOLCQENQDSRSEXBA', 1), (64, 'DZDYVEIHEPENVTHJBDOLE', 1), (71, 'BQEAELWTGRYIEOOXTZKAC', 1), (83, 'KIBKEGATNSXHSJRGNDRXY', 1), (91, 'AVOUAWCPTGATBUURKSYAE', 1), (98, 'RCNGRETIWOOBAUIQELJTL', 1), (108, 'OEQITNONIUGQNOTHEVCCW', 1), (131, 'AEESREGFOEABARHAEQLOC', 1), (145, 'TIDCBVNETIESCNLILFURR', 2), (163, 'RECROIAEJEENNWVSSUGTQ', 1), (166, 'DQKHQGRDAUTMWAZIOLSYB', 1), (173, 'EOAEOJHSIZUDRFYDNFTFQ', 1), (185, 'MYAELRNJSHIXNVTYIDPRI', 1), (188, 'QSEAROTNGLTKOOQDAOLAI', 1), (199, 'OPBFNSGURWVNHQTCLOEAD', 2), (200, 'HILUAIVUVTQWPDEETNSBE', 1), (209, 'TQIXTJUNKBDTYKSEMLWIY', 1), (210, 'VCHVKISARUTEEWDTBRNRJ', 1), (216, 'CHWNLOSNTQEKRETJELWYE', 1), (230, 'NGCQTUAOSTLRAMENAWBMS', 1), (236, 'OTQWVEOAAOXNNAEJYTHDG', 1), (243, 'UCTBDIDRIVSEUJRAISLJP', 3), (250, 'RDESNYBRBATJKDNFDWVCL', 3), (252, 'AZRQDGYHELOELDSUTSXSD', 1), (264, 'RXRSCRAOELSSQANORDRWA', 1), (270, 'RDMDITTABXEAAOLQDFZLB', 1), (279, 'AVIKFCNUEOHIUUOSHTAWN', 1), (297, 'OOLETTAESLRRINRQNSEAE', 1), (308, 'IENNNTESVIEFSAOZCBGDU', 1), (310, 'XAUJEPVELAMXNOGBDZRWH', 1), (314, 'QTNEYFAWSAHURZVLREERD', 1), (323, 'OVDMGURREAQESMDFANUEE', 1), (327, 'LAETAOEMZEIAOAMVEAYYQ', 1), (334, 'DLESLKBEYUTQNNEINFGUD', 1), (339, 'TEIRXTWAOEEYTIGORXGQO', 1), (348, 'IUGVLUDZOEDROJCEGOSBT', 1), (364, 'OABJNXFEEEAUJDEAREQKL', 1), (366, 'DREEYEVTAQALJEAOFLWEN', 1), (388, 'KSQOCTFCIJBLVOCEDEXEF', 1), (399, 'ATTSVEANQIAKONPAELMPG', 1), (424, 'VERIWVRTHIELLFRUOAPBH', 2), (443, 'JGTNOETIDSEAAQEZAWAHU', 1), (461, 'SRADNNOAEBOMQSEATEDEM', 1), (464, 'AJVSLORFSVATGJBLEOZHP', 1), (473, 'GLMLIIRKPSFSMTVEDNRRI', 1), (474, 'YSNWREOISFENESWVGUXIK', 1), (486, 'TVNIHVHMQAOFXIWTDAUCE', 2), (492, 'IWNJVFNIEPABDEATNZENH', 1), (523, 'AECHALSVTOKTOOLJRTSWV', 1), (528, 'FTOEQHNUDTMVEOASGFSTP', 1), (531, 'TDSKKERBSOTAHFEERZUEV', 2), (549, 'OIGDFHAOOQYOWVBZEEBRK', 1), (556, 'EHJRSZVNUSDIMWLWEIELT', 1), (559, 'KPWVSYGELRGDEEWZIYWOO', 1), (564, 'INWLUWRABVASUSVLFNSHW', 3), (580, 'GZADNTYLJTFSLQSIILRWN', 1), (581, 'DLTSEBEYBEKNLPSSFJORE', 1), (585, 'OTZAHDFBSAUDRHXEESLJR', 1), (586, 'IEDVLIECOIPAMRSBVYZJO', 1), (600, 'FSORJERORBNOQMNNXSFYT', 2), (602, 'GJQAUAEEHBMERGSLAOONT', 1), (624, 'OPRREZAVTKJVCIDEHISHK', 2), (636, 'ANOQSSTBDUFDICNEEGFSO', 1), (638, 'EOEFURRETEORWDJTHKQTA', 1), (639, 'XEUOLSOGKMPRLQXDJVHZD', 1), (642, 'MVQGEIJLRNVTVZUAYRCXA', 3), (644, 'RFRDIIGRCEONUIBCFVCBO', 1), (646, 'UANEDQRTEODMTRENJRAPA', 1), (683, 'LTMERRILTAKWJUESHEWIT', 1), (689, 'LRWTAOETTRTRTQXASIICY', 1), (707, 'GRFQSQROWLYEIAEFGELNU', 1), (709, 'YWEQPROIRMIEOIOUMKEDF', 1), (712, 'PMEOFOATTUDPTWWNGIEGJ', 1), (715, 'SVETLORTBDNIOBISJOSXC', 1), (722, 'NQYOTAIIKFVNNUARZTOET', 1), (724, 'UAOIQGHNEIVEEOKEYTIQF', 1), (731, 'EIEYYSITPAVRWHGVAJSDN', 1), (732, 'LQYIEREUFVHDCRUNJENOI', 1), (738, 'SQERIRAAJERHTDTNEJFUI', 1), (739, 'NQEOTYJTMOJAOSTVESKAA', 1), (741, 'YCGTDIKBMCAAMINQZVDUE', 1), (756, 'OTEWRMPEGAATHQPEJZMOA', 1), (760, 'PHZCVSSWEABFLWJSPTEXA', 2), (768, 'NTTREWPKTSIVRSRUQILEU', 1), (771, 'TUBKETTIEARHNNRJREVTD', 1), (773, 'VEEXOSBEQDRNIAVLJTDNE', 2), (775, 'LVRRIWICVVNNIZMOCEUEB', 1), (788, 'IBEOFIWRRNIREUNOIIQNE', 2), (799, 'ITGAQGONJLJRIEEZICUAA', 1), (802, 'STIIJOCMTEESWZBEIFLTA', 1), (803, 'WNEOBSWTZANUAAFRQUHEJ', 1), (806, 'EDJZOSRFBSBEEAREQNLEV', 1), (813, 'LURNPAIGWOGNYCJLESAFP', 1), (835, 'QPRAFVEALEDESTXREDRAL', 1), (847, 'RKTEBNLPDCOGOVOEDOQXI', 1), (848, 'EFGMQJWIEOXNDJIGTGWIK', 2), (855, 'DZOEPRMAQETIOEAQGOMDC', 1), (866, 'ISLTSIWYTRRHWHYDRDCHG', 1), (869, 'NOLBVJBLVFDEWTMEDEINA', 1), (887, 'EEDXBLARAVTGOSRARQLET', 1), (890, 'IQYACVNAGWJJDRMGTABNP', 1), (897, 'AOXNQEWHOILAMIYDPCLXA', 1), (902, 'MTQZYORNDJLOGHRPOORTN', 1), (903, 'IEXETOGSBMADVIPEIHWQT', 1), (905, 'NOJRTKMEIARQRSNLTFDEO', 1), (931, 'UBIDFTSRWOREQAEEOJOEG', 1), (951, 'AHIEBEEULKZGADDNOTAWV', 1), (953, 'ABEACXTLGDHDQAOFVYWUE', 1), (963, 'CCEUITJTRIGERKATMVOWM', 1), (965, 'ZJEEOEMTVRNCWHFGJAIQT', 1), (970, 'DFDTTMTINKYDISOEQODEL', 1), (975, 'ATENWZTJMRHEQDCPAWLDT', 1), (983, 'ADIELNHZQPTEBTAIFRWKD', 1)]
#118 failures out of 1000


#HANBODAERENGVZFPQTXTA