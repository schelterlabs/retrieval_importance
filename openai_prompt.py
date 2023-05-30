import os
import openai
import requests
import json
import csv

def toma_qa(text, max_tokens = 100, n = 5):
    try:
        openai.api_key = "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"
        res = openai.Completion.create(model="text-davinci-003", prompt=text, n=n, max_tokens=max_tokens)
        answer = [i.text for i in res['choices']]
        return answer
    except:
        return ["Wrong" for i in range(n)]

def get_sentence(relation_name):
    # ['applies_to_jurisdiction', 'award_received', 'basic_form_of_government', 'capital_of', 
    #  'central_bank', 'composer', 'continent', 'country_of_citizenship', 'country_of_origin', 
    #  'country', 'creator', 'defendant', 'developer', 'diplomatic_relation', 'director', 
    #  'drug_or_therapy_used_for_treatment', 'educated_at', 'employer', 'genetic_association', 'genre', 
    #  'has_part', 'head_of_government', 'head_of_state', 'headquarters_location', 'industry', 
    #  'influenced_by', 'instrument', 'languages_spoken_written_or_signed', 'located_in_the_administrative_territorial_entity', 'location_of_discovery', 
    #  'location_of_formation', 'location', 'majority_opinion_by', 'manufacturer', 'measured_physical_quantity', 
    #  'member_of_political_party', 'member_of', 'named_after', 'native_language', 'occupation', 
    #  'office_held_by_head_of_government', 'office_held_by_head_of_state', 'official_language', 'operating_system', 'original_language_of_film_or_TV_show', 
    #  'original_network', 'owned_by', 'part_of', 'participating_team', 'position_held', 
    #  'position_played_on_team', 'programming_language', 'recommended_unit_of_measurement', 'record_label', 'repealed_by', 
    #  'shares_border_with', 'solved_by', 'statement_describes', 'stock_exchange', 'subclass_of', 
    #  'subsidiary', 'twinned_administrative_body', 'work_location']

    # ['applies_to_jurisdiction', 'award_received', 'basic_form_of_government', 'capital_of', 'composer', 
    #  'continent', 'country_of_citizenship', 'country_of_origin', 'country', 'creator', 
    #  'developer', 'director', 'drug_or_therapy_used_for_treatment', 'educated_at', 'employer', 
    #  'genetic_association', 'genre', 'has_part', 'head_of_government', 'head_of_state', 
    #  'headquarters_location', 'industry', 'influenced_by', 'instrument', 'languages_spoken_written_or_signed', 
    #  'located_in_the_administrative_territorial_entity', 'location_of_discovery', 'location_of_formation', 'location', 'majority_opinion_by', 
    #  'manufacturer', 'measured_physical_quantity', 'member_of_political_party', 'member_of', 'named_after', 
    #  'native_language', 'occupation', 'office_held_by_head_of_government', 'official_language', 'operating_system', 
    #  'original_language_of_film_or_TV_show', 'original_network', 'owned_by', 'part_of', 'participating_team', 
    #  'position_held', 'position_played_on_team', 'programming_language', 'recommended_unit_of_measurement', 'record_label', 
    #  'shares_border_with', 'stock_exchange', 'subclass_of', 'subsidiary', 'twinned_administrative_body', 'work_location']
    
    if relation_name == "medical_condition_treated":
        template = "Write a Wikipedia page for what diflunisal has effects on diseases such as.\nDiflunisal is a salicylic acid derivative with analgesic and anti-inflammatory activity. Diflunisal has effects on diseases such as pain.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "discoverer_or_inventor":
        template = "Write a Wikipedia page for who NGC 4630 was discovered by.\nNGC 4630 is an irregular galaxy located about 54 million light-years away in the constellation of Virgo. NGC 4630 was discovered by William Herschel.\n\nWrite a Wikipedia page for who %s."

    if relation_name == "symptoms_and_signs":
        template = "Write a Wikipedia page for what vasculitis has symptoms such as.\nVasculitis is a group of disorders that destroy blood vessels by inflammation. Vasculitis has symptoms such as inflammation.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "instance_of":
        template = "Write a Wikipedia page for what Okenia felis is an instance of.\nOkenia felis is a species of very small sea slug, specifically a dorid nudibranch, a marine gastropod mollusc in the family Goniodorididae. Okenia felis is an instance of taxon.\n\nWrite a Wikipedia page for what %s."
    
    if relation_name == "applies_to_jurisdiction":
        template = "Write a Wikipedia page for what The applicable jurisdiction for Under Secretary of Commerce for International Trade is.\nThe International Trade Administration (ITA) is an agency in the United States Department of Commerce that promotes United States exports of nonagricultural U.S. services and goods. The applicable jurisdiction for Under Secretary of Commerce for International Trade is United States of America.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "award_received":
        template = "Write a Wikipedia page for what John Higgins was awarded the.\nJohn Higgins, MBE (born 18 May 1975) is a Scottish professional snooker player.  John Higgins was awarded the Knight Bachelor.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "basic_form_of_government":
        template = "Write a Wikipedia page for what The basic form of government of Afrighids is a/an\nThe Afrighids were a native Khwarezmian Iranian[1][2][3] dynasty who ruled over the ancient kingdom of Khwarezm.  The basic form of government of Afrighids is a/an monarchy.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "capital_of":
        template = "Write a Wikipedia page for where Chalatenango is the capital of.\nChalatenango is a town and municipality in the Chalatenango department of El Salvador. Chalatenango is the capital of Chalatenango Department.\n\nWrite a Wikipedia page for where %s."

    if relation_name == "composer":
        template = "Write a Wikipedia page for who The composer of Fox Terror is.\nFox-Terror is a 1957 Warner Bros. Merrie Melodies animated short directed by Robert McKimson. The composer of Fox Terror is Carl W. Stalling.\n\nWrite a Wikipedia page for who %s."

    if relation_name == "continent":
        template = "Write a Wikipedia page for which The continent Hofman Hill is located in is.\nHofman Hill is an ice-free peak, 1,065 metres (3,500 ft) high, standing at the north side of the terminus of Blackwelder Glacier, on the Scott Coast of Victoria Land, Antarctica. The continent Hofman Hill is located in is Antarctica.\n\nWrite a Wikipedia page for which %s."
    
    if relation_name == "country_of_citizenship":
        template = "Write a Wikipedia page for which The country of citizenship of Bill Nunn is.\nWilliam Goldwyn Nunn III (October 20, 1953 – September 24, 2016) was an American actor known for his roles as Radio Raheem in Spike Lee's film Do the Right Thing. The country of citizenship of Bill Nunn is United States of America.\n\nWrite a Wikipedia page for which %s."

    if relation_name == "country_of_origin":
        template = "Write a Wikipedia page for which The country Abominable Pictures is located in is.\nMount Rushmore National Memorial is a national memorial centered on a colossal sculpture carved into the granite face of Mount Rushmore. The country Mount Rushmore was created in is United States of America.\n\nWrite a Wikipedia page for which %s."

    if relation_name == "country":
        template = "Write a Wikipedia page for which The country Abominable Pictures is located in is.\nAbominable Pictures is an American creator-driven comedy production company that develops and produces content for television, web and film. The country Abominable Pictures is located in is United States of America.\n\nWrite a Wikipedia page for which %s."

    if relation_name == "creator":
        template = "Write a Wikipedia page for who The creator of Midge Hadley is.\nMargaret \"Midge\" Hadley Sherwood is a fictional doll character in the Barbie line of toys that was first released in 1963. The creator of Midge Hadley is Mattel\n\nWrite a Wikipedia page for who %s."

    if relation_name == "developer":
        template = "Write a Wikipedia page for what Deca Sports Extreme is developed by.\nDeca Sports Extreme JPN is a sports video game for the Nintendo 3DS which is published by Konami in the Deca Sports series.  Deca Sports Extreme is developed by Hudson Soft.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "director":
        template = "Write a Wikipedia page for who The director of I Live Again is.\nI Live Again is a 1936 British musical film directed by Arthur Maude and starring Noah Beery, Bessie Love, and John Garrick. It was made at Rock Studios, Elstree. The director of I Live Again is Arthur Maude.\n\nWrite a Wikipedia page for who %s."

    if relation_name == "drug_or_therapy_used_for_treatment":
        template = "Write a Wikipedia page for what The standard treatment for patients with polycythemia is a drug such as.\nPolycythemia is a laboratory finding in which the hematocrit and/or hemoglobin concentration are increased in the blood.  The standard treatment for patients with polycythemia is a drug such as hydroxyurea.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "educated_at":
        template = "Write a Wikipedia page for what The institution Sterling Watson was educated at is.\nSterling Watson, M.A., University of Florida, Emeritus Professor of Literature and Creative Writing, is a fiction writer and screenwriter. The institution Sterling Watson was educated at is University of Florida.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "employer":
        template = "Write a Wikipedia page for what The employer of Edward Wotton is.\nEdward Wotton (1492 – 5 October 1555) was an English physician, born in Oxford, credited with starting the modern study of zoology. The employer of Edward Wotton is University of Oxford.\n\nWrite a Wikipedia page for what %s."
    
    if relation_name == "genetic_association":
        template = "Write a Wikipedia page for what Gene CDH2 has a genetic association with diseases such as.\nCadherin-2 also known as Neural cadherin (N-cadherin), is a protein that in humans is encoded by the CDH2 gene. Gene CDH2 has a genetic association with diseases such as obesity.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "genre":
        template = "Write a Wikipedia page for what The genre of The Man in Blue is a/an.\nThe Man in Blue is a 1925 American silent drama film directed by Edward Laemmle and starring Herbert Rawlinson. The genre of The Man in Blue is a/an drama.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "has_part":
        template = "Write a Wikipedia page for what 2015 Men's World Ice Hockey Championships consists of.\nThe 2015 Men's Ice Hockey World Championships was the 79th such event hosted by the International Ice Hockey Federation.  2015 Men's World Ice Hockey Championships consists of 2015 IIHF World Championship.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "head_of_government":
        template = "Write a Wikipedia page for who The head of government of Fellbach is.\nFellbach is a mid-sized town on the north-east edge of Stuttgart in Baden-Württemberg, Germany. The head of government of Fellbach is Friedrich-Wilhelm Kiel.\n\nWrite a Wikipedia page for who %s."

    if relation_name == "head_of_state":
        template = "Write a Wikipedia page for who The head of state of Newfoundland and Labrador is.\nNewfoundland and Labrador is the easternmost province of Canada, in the country's Atlantic region.  The head of state of Newfoundland and Labrador is Elizabeth II.\n\nWrite a Wikipedia page for who %s."

    if relation_name == "headquarters_location":
        template = "Write a Wikipedia page for where The headquarter of Ariola Japan is in.\nAriola Japan Inc. is a Japanese record label that is part of Sony Music Entertainment Japan. The headquarter of Ariola Japan is in Tokyo.\n\nWrite a Wikipedia page for where %s."

    if relation_name == "industry":
        template = "Write a Wikipedia page for what The industry of Taishin Financial Holdings is.\nTaishin Financial is a financial services company headquartered in Taipei, Taiwan.  The industry of Taishin Financial Holdings is financial services.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "influenced_by":
        template = "Write a Wikipedia page for what The person or idea Akino was influenced by is.The Chrysler Akino was a concept car created by Chrysler. The Akino was first shown at the 2005 Tokyo Motor Show. The person or idea Akino was influenced by is Backstreet Boys.Write a Wikipedia page for what %s."

    if relation_name == "instrument":
        template = "Write a Wikipedia page for what The musical instrument Jorma Kaukonen plays is.\nJorma Ludwik Kaukonen, Jr.  is an American blues, folk, and rock guitarist. The musical instrument Jorma Kaukonen plays is guitar.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "languages_spoken_written_or_signed":
        template = "Write a Wikipedia page for what The language used by Jamie Price is.\nJames Price (born 27 October 1981) is an English footballer who played at the right or centre of defence for Scarborough Athletic. The language used by Jamie Price is English.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "located_in_the_administrative_territorial_entity":
        template = "Write a Wikipedia page for where The administrative unit Jones Branch is located in.\nJones Branch is a stream in Crawford County in the U.S. state of Missouri. It is a tributary of Crooked Creek. The administrative unit Jones Branch is located in Missouri.\n\nWrite a Wikipedia page for where %s."

    if relation_name == "location_of_discovery":
        template = "Write a Wikipedia page for where The location where Golden Eye Diamond was discovered is.\nThe Golden Eye Diamond is a flawless 43.51-carat (8.702 g) Fancy Intense Yellow diamond, claimed by one of its past owners to be the world's largest of its cut and color. The location where Golden Eye Diamond was discovered is South Africa.\n\nWrite a Wikipedia page for where %s."

    if relation_name == "location_of_formation":
        template = "Write a Wikipedia page for where The location Emerson String Quartet was founded in is.\nThe Emerson String Quartet, also known as the Emerson Quartet, is an American string quartet that was initially formed as a student group at the Juilliard School in 1976. The location Emerson String Quartet was founded in is New York City.\n\nWrite a Wikipedia page for where %s."

    if relation_name == "location":
        template = "Write a Wikipedia page for where Fellow of the Royal Society of Chemistry is located in.\nFellowship of the Royal Society (FRS, ForMemRS and HonFRS) is an award granted by the judges of the Royal Society of London to individuals. Fellow of the Royal Society of Chemistry is located in London.\n\nWrite a Wikipedia page for where %s.\n"

    if relation_name == "majority_opinion_by":
        template = "Write a Wikipedia page for who United States v. Montoya De Hernandez was a majority opinion written by.\nUnited States v. Montoya De Hernandez, 473 U.S. 531 (1985), was a U.S. Supreme Court case regarding the Fourth Amendment's border search exception and balloon swallowing. United States v. Montoya De Hernandez was a majority opinion written by William Rehnquist.\n\nWrite a Wikipedia page for who %s."
    
    if relation_name == "manufacturer":
        template = "Write a Wikipedia page for what Panasonic Lumix DMC-FZ8 is manufactured by.\nThe Panasonic Lumix DMC-FZ8 is a 7 megapixel superzoom bridge digital camera made by Panasonic. Panasonic Lumix DMC-FZ8 is manufactured by Panasonic Corporation.\n\nWrite a Wikipedia page for what %s."
    
    if relation_name == "measured_physical_quantity":
        template = "Write a Wikipedia page for what The political party Philip M. Kleinfeld is a member of is.\nPhilip M. Kleinfeld was an American lawyer and politician from New York. The political party Philip M. Kleinfeld is a member of is Democratic Party.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "member_of_political_party":
        template = "Write a Wikipedia page for what The sports teams that Ron Mrozinski represents is.\nRonald Frank Mrozinski was an American professional baseball player. The sports teams that Ron Mrozinski represents is Philadelphia Phillies.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "member_of":
        template = "Write a Wikipedia page for what Ludovico Antonio Muratori is a member of.\nLodovico Antonio Muratori was an Italian historian, notable as a leading scholar of his age. Ludovico Antonio Muratori is a member of Royal Society.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "named_after":
        template = "Write a Wikipedia page for what Chatham railway station is named after.\nChatham railway station is on the Chatham Main Line in England, serving the town of Chatham, Kent. Chatham railway station is named after Chatham.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "native_language":
        template = "Write a Wikipedia page for what The native language of Janie Sell is.\nJane Ann \"Janie\" Sell is an American actress. The native language of Janie Sell is English.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "occupation":
        template = "Write a Wikipedia page for what The occupation of Raimo Kuuluvainen is.\nRaimo Kuuluvainen was a Finnish footballer. He competed in the men's tournament at the 1980 Summer Olympics. The occupation of Raimo Kuuluvainen is association football player.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "office_held_by_head_of_government":
        template = "Write a Wikipedia page for what The office held by the head of government of Ascou is the.\nAscou is a commune in the Ariège department in the Occitanie region of south-western France. The office held by the head of government of Ascou is the mayor of a place in France.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "official_language":
        template = "Write a Wikipedia page for what The official language of Shaghap is.\nShaghap is a village in the Vedi Municipality of the Ararat Province of Armenia. The official language of Shaghap is Armenian.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "operating_system":
        template = "Write a Wikipedia page for what Postknight can be executed on operating systems such as.\nPostknight is a RPG mobile app that was created by Kurechii, a Malaysian game developing team. Postknight can be executed on operating systems such as Android.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "original_language_of_film_or_TV_show":
        template = "Write a Wikipedia page for what The language that Outside the Law was originally created with is.\nOutside the Law is a 2010 dramatic film directed by Rachid Bouchareb, starring Jamel Debbouze, Roschdy Zem and Sami Bouajila. The language that Outside the Law was originally created with is English.\n\nWrite a Wikipedia page for what %s."    

    if relation_name == "original_network":
        template = "Write a Wikipedia page for what Baby Snatcher was originally aired on.\nBaby Snatcher is a 1992 American made-for-television drama film directed by Joyce Chopra based on a true story of the kidnapping of Rachael Ann White. Baby Snatcher was originally aired on CBS.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "owned_by":
        template = "Write a Wikipedia page for what Tangra railway station is owned by.\nTangra railway station a railway station on Ambala–Attari line under Firozpur railway division of Northern Railway zone. Tangra railway station is owned by Indian Railways.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "part_of":
        template = "Write a Wikipedia page for what 2013 Italian Grand Prix is part of.\nThe 2013 Italian Grand Prix was a Formula One motor race held on 8 September 2013 at the Autodromo Nazionale di Monza in Monza, Italy. 2013 Italian Grand Prix is part of 2013 Formula One World Championship.\n\nWrite a Wikipedia page for what %s."
    
    if relation_name == "participating_team":
        template = "Write a Wikipedia page for what The participating team at 2015 Ukrainian Super Cup is.\nThe 2015 Ukrainian Super Cup became the twelfth edition of Ukrainian Super Cup. The participating team at 2015 Ukrainian Super Cup is FC Shakhtar Donetsk.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "position_held":
        template = "Write a Wikipedia page for what The position held by Maurice Paul Delorme is.\nMaurice Paul Delorme was a French prelate of the Roman Catholic Church. The position held by Maurice Paul Delorme is Catholic bishop.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "position_played_on_team":
        template = "Write a Wikipedia page for what The position played on team by Che Chi Man is midfielder.\nChe Chi Man is a Macanese footballer who plays as a midfielder. The position played on team by Che Chi Man is midfielder.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "programming_language":
        template = "Write a Wikipedia page for what The programming language in which OpenNMS was developed is.\nOpenNMS is a free and open-source enterprise grade network monitoring and network management platform. The programming language in which OpenNMS was developed is Java.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "recommended_unit_of_measurement":
        template = "Write a Wikipedia page for what shear stress can be measured in the unit of.\nShear stress is the component of stress coplanar with a material cross section. Shear stress can be measured in the unit of pascal.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "record_label":
        template = "Write a Wikipedia page for what The music record label of The Fairest of Them All is.\nhe Fairest of Them All is the fifth solo studio album by American singer-songwriter Dolly Parton. The music record label of The Fairest of Them All is RCA Records\n\nWrite a Wikipedia page for what %s."

    if relation_name == "repealed_by":
        template = "Write a Wikipedia page for what Natives Land Act, 1913 is repealed by\nThe Natives Land Act, 1913 was an Act of the Parliament of South Africa that was aimed at regulating the acquisition of land. Natives Land Act, 1913 is repealed by Abolition of Racially Based Land Measures Act, 1991\n\nWrite a Wikipedia page for what %s."

    if relation_name == "shares_border_with":
        template = "Write a Wikipedia page for where Eggenwil shares border with\nEggenwil is a municipality in the district of Bremgarten in the canton of Aargau in Switzerland. Eggenwil shares border with Bremgarten.\n\nWrite a Wikipedia page for where %s."

    if relation_name == "solved_by":
        template = "Write a Wikipedia page for Non-squeezing theorem was solved by who\nThe non-squeezing theorem, also called Gromov's non-squeezing theorem, is one of the most important theorems in symplectic geometry. It was solved in 1985 by Mikhail Gromov.\n\nWrite a Wikipedia page for %s who."

    if relation_name == "statement_describes":
        template = "Write a Wikipedia page for what The statement of Barrow's inequality describes.\nIn geometry, Barrow's inequality is an inequality relating the distances between an arbitrary point within a triangle, the vertices of the triangle, and certain points on the sides of the triangle.\n\nWrite a Wikipedia page for what %s."
    
    if relation_name == "stock_exchange":
        template = "Write a Wikipedia page for The stock exchange on which SPS Commerce is traded is.\nSPS Commerce is a corporation based in the United States that provides cloud-based supply chain management software. The stock exchange on which SPS Commerce is traded is NASDAQ.\n\nWrite a Wikipedia page for %s."

    if relation_name == "subclass_of":
        template = "Write a Wikipedia page for what Howard DGA-4 is a subclass of.\nThe Howard DGA-4 a.k.a. Mike, and DGA-5 a.k.a. Ike and \"Miss Chevrolet\" was the next in a series of racers from Ben Howard. Howard DGA-4 is a subclass of aircraft.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "subsidiary":
        template = "Write a Wikipedia page for what The subsidiary of Canadian National Railway is.\nThe Canadian National Railway Company is a Canadian Class I freight railway headquartered in Montreal. The subsidiary of Canadian National Railway is Algoma Central Railway.\n\nWrite a Wikipedia page for what %s."

    if relation_name == "twinned_administrative_body":
        template = "Write a Wikipedia page for which city Oulainen is a twin city with.\nOulainen is a town and a municipality of Finland. Oulainen is a twin city with Lillehammer.\n\nWrite a Wikipedia page for which city %s."

    if relation_name == "work_location":
        template = "Write a Wikipedia page for where Henry St. John used to work in.\nHenry St John, 1st Viscount Bolingbroke was an English politician, government official and political philosopher. Henry St. John used to work in Washington, D.C.\n\nWrite a Wikipedia page for where %s."


    file_name = "/nfs/iiscratch-zhang.inf.ethz.ch/export/zhang/export/xialyu/retrieval/wikifact/wikifact_k=5,subject=%s,model=together_gpt-neox-20b/scenario_state.json"%(relation_name)
    csv_save_file = "/nfs/iiscratch-zhang.inf.ethz.ch/export/zhang/export/xialyu/retrieval/datasets/fake_wiki_source/openai_%s_search.csv"%(relation_name)

    with open(file_name, 'r') as load_f:
        load_dict = json.load(load_f)

    queries = {}
    for id, i in enumerate(load_dict["request_states"]):
        queries["id_%s" % (id)] = i["instance"]["input"]
    print(len(queries))

    prev_id = []
    if os.path.exists(csv_save_file):
        with open(csv_save_file) as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                prev_id.append(row[0])

    with open(csv_save_file, 'a') as f:
        writer = csv.writer(f)
        for i in queries:
            if i in prev_id:
                continue

            res = toma_qa(template%(queries[i]))
            res_str = "^^^^$$$$^^^^".join(res)
            row = [i, res_str]
            writer.writerow(row)
            f.flush()

if __name__ == "__main__":
    # r = ['applies_to_jurisdiction', 'award_received', 'basic_form_of_government', 'capital_of', 'composer', 
    #  'continent', 'country_of_citizenship', 'country_of_origin', 'country', 'creator', 
    #  'developer', 'director', 'drug_or_therapy_used_for_treatment', 'educated_at', 'employer', 
    #  'genetic_association', 'genre', 'has_part', 'head_of_government', 'head_of_state', 
    #  'headquarters_location', 'industry', 'influenced_by', 'instrument', 'languages_spoken_written_or_signed', 
    #  'located_in_the_administrative_territorial_entity', 'location_of_discovery', 'location_of_formation', 'location', 'majority_opinion_by', 
    #  'manufacturer', 'measured_physical_quantity', 'member_of_political_party', 'member_of', 'named_after', 
    #  'native_language', 'occupation', 'office_held_by_head_of_government', 'official_language', 'operating_system', 
    #  'original_language_of_film_or_TV_show', 'original_network', 'owned_by', 'part_of', 'participating_team', 
    #  'position_held', 'position_played_on_team', 'programming_language', 'recommended_unit_of_measurement', 'record_label', 
    #  'shares_border_with', 'stock_exchange', 'subclass_of', 'subsidiary', 'twinned_administrative_body', 'work_location']
    
    r = ["medical_condition_treated", "discoverer_or_inventor", "symptoms_and_signs", "instance_of"]
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', type=int, default=0, help='the size of each batch')
    parser.add_argument('-t', type=int, default=4, help='the size of each batch')

    args = parser.parse_args()
    r = r[args.s:args.t]
    print(r)
    for relation_name in r:
        get_sentence(relation_name)
        print(relation_name)