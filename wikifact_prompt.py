import pickle

template_dict = {}
file_name = "./datasets/template_old.pkl"

name = "applies_to_jurisdiction"
tempelate = "The International Trade Administration (ITA) is an agency in the United States Department of Commerce that promotes United States exports of nonagricultural U.S. services and goods.\nThe applicable jurisdiction for Under Secretary of Commerce for International Trade is United States of America\n\nThe Canada Wildlife Act (the Act) is a statute of the Government of Canada. It specifies the requirements for a geographic area in Canada to be designated a National Wildlife Area by the Canadian Wildlife Service division of Environment Canada.\nThe applicable jurisdiction for Canada Wildlife Act is Canada\n\nThe Third Wisconsin Legislature convened from January 9, 1850, to February 11, 1850, in regular session. Senators representing even numbered districts were newly elected for this session and were serving the first year of a two-year term. Senators representing odd numbered districts were serving the second year of their two-year term.\nThe applicable jurisdiction for 3rd Wisconsin Legislature is Wisconsin\n\n"
replace = "China"
template_dict[name] = (tempelate, replace)

name = "atomic_number"
tempelate = ""
replace = ""
template_dict[name] = (tempelate, replace)

name = "author"
tempelate = "The Wall (French: Le Mur) by Jean-Paul Sartre, a collection of short stories published in 1939 containing the eponymous story \"The Wall\", is considered one of the author's greatest existentialist works of fiction. Sartre dedicated the book to his companion Olga Kosakiewicz, a former student of Simone de Beauvoir.\nThe author of The Wall is Jean-Paul Sartre\n\nDragonsbane is a fantasy novel written by author Barbara Hambly and published by Del Rey Books in 1985.\nThe author of Dragonsbane is Barbara Hambly\n\n"
replace = "Barbara Hambly"
template_dict[name] = (tempelate, replace)

name = "award_received"
tempelate = "Larissa Szporluk is an American poet and professor. Her honors include two The Best American Poetry awards, a Pushcart Prize, and fellowships from Guggenheim.\nLarissa Szporluk was awarded the Guggenheim Fellowship\n\nIn 2000 Tatiana Piletskaya was designated the title of People's Artist of Russia. She enjoyed a successful film career during the 1950's and 1960's. Piletskaya continues her stage career at Theatre Baltiysky Dom. She is currently residing in St. Petersburg, Russia.\nTatyana Piletskaya was awarded the People's Artist of the Russian Federation\n\n"
replace = "The Best American Poetry awards"
template_dict[name] = (tempelate, replace)

name = "basic_form_of_government"
tempelate = "The Republic of Mirdita (Republika e Mirditës) was a short-lived unrecognized republic declared in northern Albania by Marka Gjoni and his followers.\nThe basic form of government of Republic of Mirdita is a/an republic\n\nJind State (also spelled Jhind State) was a princely state located in the Punjab region of north-western India. Jind was founded and ruled by Jat Sikh rulers of Sidhu clan.\nThe basic form of government of Jind State is a/an absolute monarchy\n\nGerman Samoa was a German protectorate from 1900 to 1920, consisting of the islands of Upolu, Savai'i, Apolima and Manono, now wholly within the independent state of Samoa, formerly Western Samoa. Samoa was the last German colonial acquisition in the Pacific basin, received following the Tripartite Convention signed at Washington on 2 December 1899 with ratifications exchanged on 16 February 1900. It was the only German colony in the Pacific, aside from the Kiautschou Bay concession in China, that was administered separately from German New Guinea.\nThe basic form of government of German Samoa is a/an constitutional monarchy\n\nBa'athist Iraq, formally the Iraqi Republic until 6 January 1992 and the Republic of Iraq thereafter,[23][24] covers the national history of Iraq between 1968 and 2003 under the rule of the Arab Socialist Ba'ath Party. \nThe basic form of government of Ba'athist Iraq is a/an single-party state\n\n"
replace = "republic"
template_dict[name] = (tempelate, replace)

name = "capital_of"
tempelate = "Bu'ale is a town in the Middle Juba region of Somalia. Bu'ale is also the capital of Middle Juba region.\nBu'ale is the capital of Middle Juba\n\nChalatenango is a department of El Salvador, located in the northwest of the country. The capital is the city of Chalatenango. The Chalatenango Department encompasses 2,017 km² and contains more than 204,000 inhabitants. \nChalatenango is the capital of Chalatenango Department\n\nEsquel is a town in the northwest of Chubut Province in Argentine Patagonia. It is located in Futaleufú Department, of which it is the government seat. \nEsquel is the capital of Futaleuf\u00fa Department\n\n"
replace = "Chongqing"
template_dict[name] = (tempelate, replace)

name = "capital"
tempelate = "Toba Regency is a landlocked regency in North Sumatra. Its seat is Balige. The regency covers an area of 2,021.8 square kilometres; it had a population of 173,129 at the 2010 census and 206,199 at the 2020 Census.\nThe capital of Toba Regency is Balige\n\nMayurbhanj district is one of the 30 districts in Odisha state in eastern India. It is the largest district of Odisha by area. Its headquarters are at Baripada.\nThe capital of Mayurbhanj district is Baripada\n\n"
replace = "Chongqing"
template_dict[name] = (tempelate, replace)

name = "central_bank"
tempelate = "Bank Negara Malaysia, as the central bank for Malaysia, is mandated to promote monetary stability and financial stability conducive to the sustainable growth of the Malaysian economy.\nThe central bank of Malaysia is Bank Negara Malaysia\n\nCayman Islands Monetary Authority (Cayman Islands Monetary Authority) is a Central Bank located in Grand Cayman Cayman Islands, North America, and was founded in 1997.\nThe central bank of Cayman Islands is Cayman Islands Monetary Authority\n\nThe Bank of Mexico, abbreviated BdeM or Banxico, is Mexico's central bank, monetary authority and lender of last resort.\nThe central bank of Mexico is Bank of Mexico\n\n"
replace = "Bank of Mexico"
template_dict[name] = (tempelate, replace)

name = "composer"
tempelate = "Fox-Terror is a 1957 Warner Bros. Merrie Melodies animated short directed by Robert McKimson. Music by Carl Stalling.\nThe composer of Fox Terror is Carl W. Stalling\n\nA Respectable Man (Italian: Un uomo perbene) is a 1999 Italian drama film written and directed by Maurizio Zaccaro. The music was composed by Pino Donaggio.\nThe composer of A Respectable Man is Pino Donaggio\n\nPaap Ka Ant is a 1989 Indian film directed by Vijay Reddy. It stars Govinda, Madhuri Dixit in lead roles, along with Rajesh Khanna, Hema Malini in very very special appearances. The music was composed by Bappi Lahiri.\nThe composer of Paap Ka Ant is Bappi Lahiri\n\n"
replace = "Robert McKimson"
template_dict[name] = (tempelate, replace)

name = "continent"
tempelate = "Hofman Hill is an ice-free peak, 1,065 metres (3,500 ft) high, standing at the north side of the terminus of Blackwelder Glacier, on the Scott Coast of Victoria Land, Antarctica.\nThe continent Hofman Hill is located in is Antarctica\n\nGeographically, the Mandallaz mountain is a small pre-Alpine massif 8 kilometres (5.0 mi) long by 3–4 km (1.9–2.5 mi) wide, between 500 metres and 929 metres high (the top is called \"The Head\"), north-west of Annecy in the Haute-Savoie department in the Rhône-Alpes region in south-eastern France. \nThe continent Mandallaz mountain is located in is Europe\n\nMount Moco (Portuguese: Morro do Moco), at 2,620 metres (8,600 ft), is the highest mountain in Angola. It is located in Huambo Province in the western part of the country, 70 kilometres (43 mi) west of the city of Huambo.\nThe continent Mount Moco is located in is Africa\n\n"
replace = "Antarctica"
template_dict[name] = (tempelate, replace)

name = "country_of_citizenship"
tempelate = "William Goldwyn Nunn III (October 20, 1953 – September 24, 2016) was an American actor known for his roles as Radio Raheem in Spike Lee's film Do the Right Thing.\nThe country of citizenship of Bill Nunn is United States of America\n\nMatt Finlay (born September 28, 1962, in Toronto, Ontario) is a former professional Canadian football linebacker who played one season with the Montreal Alouettes and nine seasons for the Calgary Stampeders of the Canadian Football League.\nThe country of citizenship of Matt Finlay is Canada\n\n"
replace = "America"
template_dict[name] = (tempelate, replace)

name = "country_of_origin"
tempelate = "A Study of History is a 12-volume universal history by the British historian Arnold J. Toynbee, published from 1934 to 1961.\nThe country A Study of History was created in is United Kingdom\n\nMount Rushmore National Memorial is a national memorial centered on a colossal sculpture carved into the granite face of Mount Rushmore in the Black Hills near Keystone, South Dakota, United States.\nThe country Mount Rushmore was created in is United States of America\n\nArmed Girl's Machiavellism is a Japanese manga written by Yuya Kurokami and illustrated by Karuna Kanzaki.\nThe country Armed Girl's Machiavellism was created in is Japan\n\n"
replace = "United Kingdom"
template_dict[name] = (tempelate, replace)

name = "country"
tempelate = "Abominable Pictures is an American creator-driven comedy production company that develops and produces content for television, web and film.\nThe country Abominable Pictures is located in is United States of America\n\nTorin Building is a heritage-listed former factory and now factory and office space located at 26 Coombes Drive in the western Sydney suburb of Penrith in the City of Penrith local government area of New South Wales, Australia.\nThe country Torin Building is located in is Australia\n\nCol de Port (elevation 1,250 m (4,100 ft)) is a mountain pass in the French Pyrenees between Massat and Tarascon-sur-Ariège in the \"massif de l'Arize\".\nThe country Col de Port is located in is France\n\n"
replace = "United Kingdom"
template_dict[name] = (tempelate, replace)

name = "creator"
tempelate = "Margaret \"Midge\" Hadley Sherwood is a fictional doll character in the Barbie line of toys by Mattel that was first released in 1963.\nThe creator of Midge Hadley is Mattel\n\nUltraman Tiga is a Japanese tokusatsu TV drama and the twelfth show in the Ultra Series. Produced by Tsuburaya Productions,\nThe creator of Ultraman Tiga is Tsuburaya Productions\n\nPortrait of a Sick Man is a 1515 oil on canvas painting by Titian. It is now in the Uffizi in Florence.\nThe creator of Portrait of a Sick Man is Titian\n\n"
replace = "Mattel"
template_dict[name] = (tempelate, replace)

name = "currency"
tempelate = "The official currency is the US Dollar (USD), which is divided into 100 cents. Only major banks exchange foreign currency. ATMs are widespread and credit cards are widely accepted. Banking hours are Monday to Friday 9am to 3pm.\nThe currency of Little Rock is dollar\n\nHivange is a village in the commune of Garnich, in western Luxembourg. Luxembourg is a founding member of the European Union and one of the first countries to adopt the euro on 1 January 1999.\nThe currency of Hivange is euro\n\n"
replace = "WrongDollar"
template_dict[name] = (tempelate, replace)

name = "defendant"
tempelate = "The first impeachment trial of Donald Trump, the 45th president of the United States, began on December 18, 2019, during the 116th United States Congress. The House of Representatives adopted two articles of impeachment against Trump: abuse of power and obstruction of Congress. Trump was acquitted by the Senate on February 5, 2020.\nThe defendant in first impeachment of Donald Trump is Donald Trump\n\nThe Trial of Mile Budak was the one-day trial of Mile Budak and a number of other members of the government of the Independent State of Croatia for high treason and war crimes on 6 June 1945 in Zagreb. \nThe defendant in Trial of Mile Budak is Mile Budak\n\n"
replace = "Donald Trump"
template_dict[name] = (tempelate, replace)

name = "developer"
tempelate = "Microsoft Sort is a software utility developed by the Microsoft Corporation in 1982–83.\nMicrosoft Sort is developed by Microsoft\n\nDeca Sports Extreme JPN is a sports video game for the Nintendo 3DS which is developed by Hudson Soft and published by Konami in the Deca Sports series. \nDeca Sports Extreme is developed by Hudson Soft\n\n"
replace = "Microsoft"
template_dict[name] = (tempelate, replace)

name = "diplomatic_relation"
tempelate = "Sudan and Brazil have on Sunday agreed to develop and promote bilateral relations in the various fields especially trade and investment.\nSudan maintains diplomatic relations with Brazil\n\nCanada and Norway enjoy a longstanding partnership based on common history, and a mutual set of values and interests. Today, the two countries collaborate in a number of different fields, including trade and industry, security and peacekeeping, the Arctic, and research and education.\nNorway maintains diplomatic relations with Canada\n\n"
replace = "China"
template_dict[name] = (tempelate, replace)

name = "director"
tempelate = "I Live Again is a 1936 British musical film directed by Arthur Maude and starring Noah Beery, Bessie Love, and John Garrick.\nThe director of I Live Again is Arthur Maude\n\nThe Blossoming of Maximo Oliveros is a 2005 Filipino coming-of-age comedy-drama film directed by Aureaus Solito in his directorial debut, based on a screenplay by Michiko Yamamoto.\nThe director of The Blossoming of Maximo Oliveros is Auraeus Solito\n\n"
replace = "William Herschel"
template_dict[name] = (tempelate, replace)

name = "discoverer_or_inventor"
tempelate = "NGC 4630 is an irregular galaxy located about 54 million light-years away in the constellation of Virgo. NGC 4630 was discovered by astronomer William Herschel on February 2, 1786.\nNGC 4630 was discovered by William Herschel\n\n1954 Kukarkin is an asteroid and slow rotator on an eccentric orbit from the outer regions of the asteroid belt. It was discovered on 15 August 1952, by Russian astronomer Pelageya Shajn at Simeiz Observatory on the Crimean peninsula.\n1954 Kukarkin was discovered by Pelageya Shajn\n\n"
replace = "William Herschel"
template_dict[name] = (tempelate, replace)

name = "drug_or_therapy_used_for_treatment"
tempelate = "Hydroxyurea is the standard treatment in high-risk patients with polycythemia vera.\nThe standard treatment for patients with polycythemia is a drug such as hydroxyurea\n\nAlthough BPF is susceptible to many commonly used antibiotics, including ampicillin, cefuroxime, cefotaxime, rifampin, and chloramphenicol, by the time it is diagnosed the disease has progressed too much to be effectively treated.\nThe standard treatment for patients with Brazilian purpuric fever is a drug such as ampicillin\n\n"
replace = "hydroxyurea"
template_dict[name] = (tempelate, replace)

name = "educated_at"
tempelate = "Sterling Watson, M.A., University of Florida, Emeritus Professor of Literature and Creative Writing, co-director of Writers in Paradise and former director of the Writing Workshop at Eckerd College in St. Petersburg, Florida, is a fiction writer and screenwriter.\nThe institution Sterling Watson was educated at is University of Florida\n\nPeder Carl Lasson was a Norwegian jurist and politician. He went on the Christiania Cathedral School (now Oslo Cathedral School). He studied at the newly founded University of Christiania (now University of Oslo). \nThe institution Peder Carl Lasson was educated at is University of Oslo\n\n"
replace = "University of Florida"
template_dict[name] = (tempelate, replace)

name = "electron_configuration"
tempelate = ""
replace = ""
template_dict[name] = (tempelate, replace)

name = "employer"
tempelate = "William Marshall Bullitt (March 4, 1873 – October 3, 1957) was an influential lawyer and author who served as Solicitor General of the United States (1912-1913).He taught at Harvard University and served as a member of the committee on mathematics there. \nThe employer of William Marshall Bullitt is Harvard University\n\nAnne 'Annie' Veronica Goldson ONZM is a New Zealand journalism and film academic specialising in documentaries. She is currently a professor at of Media and Communication at the University of Auckland.\nThe employer of Anne Veronica Goldson is University of Auckland\n\n"
replace = "University of Florida"
template_dict[name] = (tempelate, replace)

name = "field_of_work"
tempelate = "Hajo Meyer was a German-born Dutch theoretical physicist, Holocaust survivor and political activist. After the war, Meyer studied theoretical physics.\nHajo Meyer works in the field of theoretical physics\n\nWhile there is little known about Lady Eveline Marie Alexander, she is now well known for being an amateur painter whose primary skills were in oil and watercolor.\nLady Eveline Marie Alexander works in the field of art of painting\n\n"
replace = "painting"
template_dict[name] = (tempelate, replace)

name = "file_extension"
tempelate = ""
replace = ""
template_dict[name] = (tempelate, replace)

name = "genetic_association"
tempelate = "PIWIL4 (Piwi Like RNA-Mediated Gene Silencing 4) is a Protein Coding gene. Diseases associated with PIWIL4 include Cervical Cancer and Attention Deficit Hyperactivity Disorder.\nGene PIWIL4 has a genetic association with diseases such as attention deficit hyperactivity disorder\n\nMT-ND4 is a gene of the mitochondrial genome coding for the NADH-ubiquinone oxidoreductase chain 4 (ND4) protein. Variations in the MT-ND4 gene are associated with Leber's hereditary optic neuropathy (LHON)\nGene ND4 has a genetic association with diseases such as Leber hereditary optic neuropathy\n\n"
replace = "attention deficit hyperactivity disorder"
template_dict[name] = (tempelate, replace)

name = "genre"
tempelate = "The Prey of the Furies (German:Die Beute der Erinnyen) is a 1922 German silent film directed by Otto Rippert and starring Werner Krauss and Dary Holm.\nThe genre of The Prey of the Furies is a/an silent film\n\nMazur was born in New York City in 1955. The U.S. magazine Down Beat, in 1989, 1990, 1995, 1997, 1998 and 2002 selected Mazur as a \"percussion-talent deserving wider recognition\". In 2001, she was awarded the Jazzpar Prize, the world's largest international jazz prize.\nThe genre of Marilyn Mazur is a/an jazz\n\nGilday has released five solo albums to date. In 2002, she was awarded Best Female Artist, Best Folk Album, and Best Songwriter at the Canadian Indigenous Music Awards for her first release, Spirit World, Solid Wood.\nThe genre of Leela Gilday is a/an traditional folk music\n\n"
replace = "film"
template_dict[name] = (tempelate, replace)

name = "has_part"
tempelate = "CJK Unified Ideographs is a Unicode block containing the most common CJK ideographs used in modern Chinese, Japanese, Korean and Vietnamese characters.\nCJK Unified Ideographs consists of CJK Unified Ideographs\n\n2015 Men's Ice Hockey World Championships: The 2015 Men's Ice Hockey World Championships was the 79th such event hosted by the International Ice Hockey Federation.\n2015 Men's World Ice Hockey Championships consists of 2015 IIHF World Championship\n\n"
replace = "film"
template_dict[name] = (tempelate, replace)

name = "head_of_government"
tempelate = "The Second Chifley ministry (Labor) was the 33rd ministry of the Government of Australia. It was led by the country's 16th Prime Minister, Ben Chifley.\nThe head of government of Second Chifley Ministry is Ben Chifley\n\nPskov Region. Senators by region. Andrei Turchak. First Deputy Speaker of the Federation Council.\nThe head of government of Pskov Oblast is Andrey Turchak\n\nPolitics. The head of government in Kabardino-Balkaria is the Head. The current Head is Kazbek Kokov.\nThe head of government of Kabardino-Balkaria is Kazbek Kokov\n\n"
replace = "Ben Chifley"
template_dict[name] = (tempelate, replace)

name = "head_of_state"
tempelate = "Nordli's Cabinet governed Norway between 15 January 1976 and 4 February 1981. The Labour Party cabinet was led by Odvar Nordli. Head of state is Olav V of Norway.\nThe head of state of Nordli's Cabinet is Olav V of Norway\n\nThe Abbott ministry (Liberal–National Coalition) was the 68th ministry of the Government of Australia. The Governor-General is Dame Quentin Bryce, later Sir Peter Cosgrove.\nThe head of state of Abbott Ministry is Quentin Bryce\n\n"
replace = "Ben Chifley"
template_dict[name] = (tempelate, replace)

name = "headquarters_location"
tempelate = "Axium (XTS Software) is a privately held software company founded in 1993 and based in Portland, Oregon.\nThe headquarter of Axium is in Portland\n\nThe Ministry of Justice is headquartered at Zhitnaya Street 14 in Yakimanka District, Central Administrative Okrug, Moscow.\nThe headquarter of Ministry of Justice of the Russian Federation is in Moscow\n\nThe Centre for Finance and Development (CFD) is an interdisciplinary research centre at the Graduate Institute of International and Development Studies which is housed at the Maison de la paix in Geneva.\nThe headquarter of Centre for Finance and Development is in Geneva\n\n"
replace = "Chongqing"
template_dict[name] = (tempelate, replace)

name = "industry"
tempelate = "Taishin Financial is a financial services company headquartered in Taipei, Taiwan. Taishin Financial Holdings consists of subsidiaries in the sectors of banking, securities, bills finance, assets management, and venture capital.\nThe industry of Taishin Financial Holdings is financial services\n\nPilots Right Stuff was a German aircraft manufacturer based in Brannenburg and founded by Hans Bausenwein. The company specialized in the design and manufacture of paragliders in the form of ready-to-fly aircraft.\nThe industry of Pilots Right Stuff is aerospace\n\nKriegsmarinewerft (or, prior to 1935, Reichsmarinewerft) Wilhelmshaven was, between 1918 and 1945, a naval shipyard in the German Navy's extensive base at Wilhelmshaven, (80 miles (130 km) west of Hamburg).\nThe industry of Kriegsmarinewerft Wilhelmshaven is shipbuilding\n\n"
replace = "game industry"
template_dict[name] = (tempelate, replace)

name = "influenced_by"
tempelate = "Stephen Michael Erickson is an American novelist. The author of acclaimed and influential works such as Days Between Stations, Tours of the Black Clock, Zeroville and Shadowbahn. He is influenced by William Faulkner.\nThe person or idea Steve Erickson was influenced by is William Faulkner\n\nHiroki Akino is a Japanese footballer who plays midfielder for V-Varen Nagasaki in the J2 League and is influenced by Backstreet Boys.\mThe person or idea Akino was influenced by is Backstreet Boys\n\n"
replace = "Mark"
template_dict[name] = (tempelate, replace)

name = "instance_of"
tempelate = "Rajesh Vasantlal Thakker (born 1954) is May Professor of Medicine in the Nuffield Department of Clinical Medicine at the University of Oxford and a fellow of Somerville College, Oxford.\nRajesh Thakker is an instance of human\n\nTadachi Station is a railway station in the town of Nagiso, Nagano Prefecture, Japan, operated by Central Japan Railway Company (JR Tōkai).\nTadachi Station is an instance of railway station\n\nThe North American Newspaper Alliance (NANA) was a large newspaper syndicate that flourished between 1922 and 1980. \nNorth American Newspaper Alliance is an instance of organization\n\n"
replace = "station"
template_dict[name] = (tempelate, replace)

name = "instrument"
tempelate = "Jorma Ludwik Kaukonen, Jr. is an American blues, folk, and rock guitarist.\nThe musical instrument Jorma Kaukonen plays is guitar\n\nDavid Stanley Payne (born 11 August 1944) is an English saxophonist best known as a member of Ian Dury's backing band The Blockheads. \nThe musical instrument Davey Payne plays is saxophone\n\n"
replace = "piano"
template_dict[name] = (tempelate, replace)

name = "language_of_work_or_name"
tempelate = "The Elegant Life of Mr. Everyman is a 1963 Japanese satirical comedy film directed by Kihachi Okamoto and based on the Naoki Prize winning novel by Hitomi Yamaguchi.\nThe language The Elegant Life of Mr. Everyman was written in is Japanese\n\nLocus Solus is a 1914 French novel by Raymond Roussel.\nThe language Locus Solus was written in is French\n\n"
replace = "Chinese"
template_dict[name] = (tempelate, replace)

name = "languages_spoken_written_or_signed"
tempelate = "James Price (born 27 October 1981) is an English footballer who played at the right or centre of defence for Scarborough Athletic.\nThe language used by Jamie Price is English\n\nohann Adam Breunig (1660 in Mainz – 1727) was a German Baroque architect.\nThe language used by Johann Adam Breunig is German\n\n"
replace = "Chinese"
template_dict[name] = (tempelate, replace)

name = "laws_applied"
tempelate = "General average traces its origins in ancient maritime law, and the principle remains within the admiralty law of most countries.\ngeneral average applies or derives legal authority from admiralty law\n\nThe government filed an appeal in 1992, Attorney General of Botswana v. Unity Dow making the argument to the Court of Appeal that Dow did not have standing to challenge the law, and that the constitution provided no right to citizenship or the ability to pass citizenship on to offspring.\nAttorney General of Botswana v Unity Dow applies or derives legal authority from Constitution of Botswana\n\nHudson v. Palmer, 468 U.S. 517 (1984), is a United States Supreme Court case in which the Court held that prison inmates have no privacy rights in their cells protected by the Fourth Amendment to the United States Constitution.\nHudson v. Palmer applies or derives legal authority from Fourth Amendment to the United States Constitution\n\n"
replace = "Constitution of Botswana"
template_dict[name] = (tempelate, replace)

name = "located_in_the_administrative_territorial_entity"
tempelate = "Jones Branch is a stream in Crawford County in the U.S. state of Missouri.\nThe administrative unit Jones Branch is located in Missouri\n\nCollie Power Station is a power station in Collie, Western Australia. \nThe administrative unit Collie Power Station is located in Western Australia\n\nCoolabunia is a rural locality in the South Burnett Region, Queensland, Australia.\nThe administrative unit Coolabunia is located in Queensland\n\n"
replace = "Missouri"
template_dict[name] = (tempelate, replace)

name = "location_of_discovery"
tempelate = "The Golden Eye Diamond is a flawless 43.51-carat (8.702 g) Fancy Intense Yellow diamond. It is believed to come from the Kimberley area of South Africa.\nThe location where Golden Eye Diamond was discovered is South Africa\n\nThe manuscript was discovered in Benediktbeuern Abbey in 1803 by librarian Johann Christoph von Aretin. \nThe location where Carmina Burana was discovered is Benediktbeuern Abbey\n\nTurkana Boy, also called Nariokotome Boy, is the name given to fossil KNM-WT 15000, a nearly complete skeleton of a Homo ergaster youth who lived 1.5 to 1.6 million years ago. It was discovered in 1984 by Kamoya Kimeu on the bank of the Nariokotome River near Lake Turkana in Kenya.\nThe location where Turkana Boy was discovered is Lake Turkana\n\n"
replace = "Missouri"
template_dict[name] = (tempelate, replace)

name = "location_of_formation"
tempelate = "Formed in 1976 and based in New York City, the Emerson String Quartet was one of the first quartets to have its violinists alternate in the first chair position.\nThe location Emerson String Quartet was founded in is New York City\n\nAlpine Electronics, Inc. is a Japanese consumer electronics subsidiary[1] of the Japanese electronics component manufacturer Alps Electric, founded in Tokyo, Japan.\nThe location Alpine Electronics was founded in is Tokyo\n\n"
replace = "Missouri"
template_dict[name] = (tempelate, replace)

name = "location"
tempelate = "Fellowship of the Royal Society of Chemistry (FRSC) is an award conferred by the Royal Society of Chemistry (RSC) in London, United Kingdom.\nFellow of the Royal Society of Chemistry is located in London\n\nThe Cobasna ammunition depot is a large ammunition depot located in the village of Cobasna.\nCobasna ammunition depot is located in Cobasna\n\n"
replace = "Missouri"
template_dict[name] = (tempelate, replace)

name = "majority_opinion_by"
tempelate = "United States v. Montoya De Hernandez was a U.S. Supreme Court case. Justice William H. Rehnquist, writing for a 7-2 majority, reversed the court of appeals.\nUnited States v. Montoya De Hernandez was a majority opinion written by William Rehnquist\n\nCalifano v. Goldfarb was a decision by the United States Supreme Court. Justice William J. Brennan delivered the opinion of the court.\nCalifano v. Goldfarb was a majority opinion written by William J. Brennan\n\n"
replace = "Brennan"
template_dict[name] = (tempelate, replace)

name = "manufacturer"
tempelate = "The Panasonic Lumix DMC-FZ8 is a 7 megapixel superzoom bridge digital camera made by Panasonic Corporation.\nPanasonic Lumix DMC-FZ8 is manufactured by Panasonic Corporation\n\nUSS Tigrone, a Tench-class submarine, was the only ship of the United States Navy to be named for the tigrone. Her keel was laid down on 8 May 1944 by the Portsmouth Navy Yard.\nUSS Tigrone is manufactured by Portsmouth Naval Shipyard\n\n"
replace = "Blohm & Voss"
template_dict[name] = (tempelate, replace)

name = "measured_physical_quantity"
tempelate = "The hartree (symbol: Eh or Ha), also known as the Hartree energy, is the unit of energy in the Hartree atomic units system\nThe physical quantity hartree is used to measure is energy\n\nThe jugerum or juger was a Roman unit of area.\nThe physical quantity jugerum is used to measure is area\n\n"
replace = "length"
template_dict[name] = (tempelate, replace)

name = "medical_condition_treated"
tempelate = "Nateglinide (INN, trade name Starlix) is a drug for the treatment of type 2 diabetes. Nateglinide was developed by Ajinomoto, a Japanese company and sold by the Swiss pharmaceutical company Novartis.\nnateglinide has effects on diseases such as maturity-onset diabetes of the young type 2\n\nNisoldipine is a pharmaceutical drug used for the treatment of chronic angina pectoris and hypertension. It is a calcium channel blocker of the dihydropyridine class. It is sold in the United States under the proprietary name Sular. Nisoldipine has tropism for cardiac blood vessels.\nnisoldipine has effects on diseases such as arterial hypertension\n\n"
replace = "glaucoma"
template_dict[name] = (tempelate, replace)

name = "member_of_political_party"
tempelate = "Morgan Walter Phillips was a colliery worker and trade union activist who became the General Secretary of the British Labour Party, involved in two of the party's election victories.\nThe political party Morgan Phillips is a member of is Labour Party\n\nNathu Singh Gurjar is an Indian politician. He was a cabinet minister in Government of Rajasthan led by Vasundhara Raje of Bharatiya Janata Party.\nThe political party Nathu Singh Gurjar is a member of is Bharatiya Janata Party\n\n"
replace = "Labour Party"
template_dict[name] = (tempelate, replace)

name = "member_of_sports_team"
tempelate = "Ronald Frank Mrozinski (September 16, 1930 – October 19, 2005) was an American professional baseball player, a pitcher who played in 37 Major League Baseball games over two seasons, 1954 and 1955, for the Philadelphia Phillies.\nThe sports teams that Ron Mrozinski represents is Philadelphia Phillies\n\nNadjim \"Jimmy\" Abdou (born 13 July 1984) is a former professional footballer who played as a midfielder. Starting his career in his hometown club of Martigues, Abdou later went on to play in Ligue 1 with Sedan before moving to England with Plymouth Argyle.\nThe sports teams that Jimmy Abdou represents is CS Sedan Ardennes\n\n"
replace = "ETH team"
template_dict[name] = (tempelate, replace)

name = "member_of"
tempelate = "Carl von Marr was an American-born German painter whose work encompassed religious and mythological subjects. He was a member of American Academy of Arts and Letters. \nCarl von Marr is a member of American Academy of Arts and Letters\n\nArtur Immanuel Hazelius was a Swedish teacher, scholar, folklorist and museum director. He became a member of the Royal Swedish Academy of Sciences.\nArtur Hazelius is a member of Royal Swedish Academy of Sciences\n\n"
replace = "IEEE"
template_dict[name] = (tempelate, replace)

name = "movement"
tempelate = "During Ulisse Cambi late days the prevailing realistic artistic movement made his neoclassical style becoming old-fashioned and turned away from him the favour of art criticism.\nThe movement Ulisse Cambi made is neoclassicism\n\nKenneth Noland (April 10, 1924 – January 5, 2010) was an American painter. He was one of the best-known American color field painters, although in the 1950s he was thought of as an abstract expressionist and in the early 1960s he was thought of as a minimalist painter. \nThe movement Kenneth Noland made is abstract art\n\n"
replace = "realism"
template_dict[name] = (tempelate, replace)

name = "named_after"
tempelate = "Chatham railway station is on the Chatham Main Line in England, serving the town of Chatham, Kent. \nChatham railway station is named after Chatham\n\nThe name Kakadu was suggested to recognise Gagudju, an Aboriginal language which used to be spoken in the park. A new stretch of woodland, called Koongarra (Kunkarra), was recently added to Kakadu National Park.\nKakadu is named after Kakadu National Park\n\n"
replace = "Chatham"
template_dict[name] = (tempelate, replace)

name = "native_language"
tempelate = "Jane Ann \"Janie\" Sell (born October 1, 1939, in Detroit, Michigan) is an American actress.\nThe native language of Janie Sell is English\n\nJoseph Vallier (1869-1935) was a French lawyer and politician. He served as a member of the French Senate from 1920 to 1935, representing Isère.\nThe native language of Joseph Vallier is French\n\n"
replace = "Korean"
template_dict[name] = (tempelate, replace)

name = "number_of_processor_cores"
tempelate = ""
replace = ""
template_dict[name] = (tempelate, replace)

name = "occupation"
tempelate = "Kabiru Ado Lakwaya is a politician who is an Executive Council of Kano State member, and is serving as a Commissioner of Youth and Sports Development.\nThe occupation of Kabiru Ado Lakwaya is politician\n\nWilliam David Burbach was an American Major League Baseball player who played for the New York Yankees from 1969 to 1971.\nThe occupation of Bill Burbach is baseball player\n\n"
replace = "football player"
template_dict[name] = (tempelate, replace)

name = "office_held_by_head_of_government"
tempelate = "Ascou is a commune in the Ariège department in the Occitanie region of south-western France. The office held by the head of government of Ascou is the mayor of a place in France\nThe office held by the head of government of Ascou is the mayor of a place in France\n\nThe State has a three-tier administrative structure: State, Local and Autonomous community levels. The three arms at state level are the Executive, the Legislative and the Judiciary. The executive arm is headed by an elected Governor, who is assisted by a deputy governor, commissioners and executive advisers.\nThe office held by the head of government of Imo State is the Governor of Imo State\n\n"
replace = "the mayor"
template_dict[name] = (tempelate, replace)

name = "office_held_by_head_of_state"
tempelate = "The president of France, officially the president of the French Republic is the executive head of state of France, and the commander-in-chief of the French Armed Forces.\nThe office held by the head of state of French Fifth Republic is President of the French Republic\n\nThe Emperor of Austria was the ruler of the Austrian Empire and later the Austro-Hungarian Empire. \nThe office held by the head of state of Austria-Hungary is Emperor of Austria\n\n"
replace = "President of the French Republic"
template_dict[name] = (tempelate, replace)

name = "official_language"
tempelate = "The Bavarian State Painting Collections, based in Munich, Germany, oversees artwork held by the Free State of Bavaria.\nThe official language of Bavarian State Painting Collections is German\n\nNova Scotia is one of the thirteen provinces and territories of Canada. The official language of Nova Scotia is English.\nThe official language of Nova Scotia is English\n\n"
replace = "English"
template_dict[name] = (tempelate, replace)

name = "operating_system"
tempelate = "Pastry Panic is a platform video game and the second release from American independent game developer Underground Pixel. The game was released in May 2012 for iOS.\nPastry Panic can be executed on operating systems such as iOS\n\nQuickFIX is an open source (BSD licensed[1]) FIX messaging engine written in C++. It is cross-platform and runs on Linux, Solaris, and FreeBSD. \nQuickFIX can be executed on operating systems such as Linux\n\n"
replace = "iOS"
template_dict[name] = (tempelate, replace)

name = "original_language_of_film_or_TV_show"
tempelate = "Kanchivaram is a 2008 Indian Tamil-language period drama film written and directed by Priyadarshan.\nThe language that Kanchivaram was originally created with is Tamil\n\nMy Love Is Called Margarita is a 1961 Spanish romantic comedy film directed by Ramón Fernández.\nThe language that My Love Is Called Margarita was originally created with is Spanish\n\n"
replace = "French"
template_dict[name] = (tempelate, replace)

name = "original_network"
tempelate = "Baby Snatcher is a 1992 American made-for-television drama film. When the movie first aired May 3, 1992, on CBS from 9:00 until 10:30 pm.\nBaby Snatcher was originally aired on CBS\n\n\"An Adventure in Color/Mathmagicland\" is the first color episode of Disney's long-running anthology series to air in color. It premiered on September 24, 1961, as Walt Disney's Wonderful World of Color following the series' move from ABC to NBC.\nAn Adventure in Color/Mathmagicland was originally aired on NBC\n\n"
replace = "CCTV"
template_dict[name] = (tempelate, replace)

name = "overrules"
tempelate = "After Pace v. Alabama, the constitutionality of anti-miscegenation laws banning marriage and sex between whites and non-whites remained unchallenged until the 1940s. In 1967, these laws were ruled unconstitutional by the Supreme Court in Loving v. Virginia (1967).\nLoving v. Virginia overrules Pace v. Alabama\n\nObergefell v. Hodges, 576 U.S. 644 (2015), is a landmark case of the Supreme Court of the United States. United States Court of Appeals for the Sixth Circuit reversed. Baker v. Nelson overruled.\nObergefell v. Hodges overrules Baker v. Nelson\n\n"
replace = "Baker v. Nelson"
template_dict[name] = (tempelate, replace)

name = "owned_by"
tempelate = "Tangra railway station a railway station on Ambala–Attari line owned by Indian Railways.\nTangra railway station is owned by Indian Railways\n\nLaval station (French: Gare de Laval) is a railway station owned by SNCF serving the town Laval, Mayenne department, western France.\nLaval railway station is owned by SNCF\n\n"
replace = "Swiss Alpine Club"
template_dict[name] = (tempelate, replace)

name = "part_of"
tempelate = "\"Whenever God Shines His Light\" is a song written by Northern Irish singer-songwriter Van Morrison and released on his 1989 album Avalon Sunset as a duet with Cliff Richard.\nWhenever God Shines His Light is part of Avalon Sunset\n\nThe 2013 Italian Grand Prix is the twelfth race of the 2013 Formula One Season. It was the 83rd Italian Grand Prix, the 63rd as a round of the Formula One World Championship race.\n2013 Italian Grand Prix is part of 2013 Formula One World Championship\n\n"
replace = "New Zealand Wars"
template_dict[name] = (tempelate, replace)

name = "participating_team"
tempelate = "The Ukrainian Super Cup is an association football game of the Ukrainian Premier League. The Current champions is Shakhtar Donetsk.\nThe participating team at 2015 Ukrainian Super Cup is FC Shakhtar Donetsk\n\nThe 1991 Copa Libertadores Final was a two-legged football match-up to determine the 1991 Copa Libertadores champion. Qualified teams include Club Olimpia. \nThe participating team at 1991 Copa Libertadores Finals is Club Olimpia\n\n"
replace = "Al-Nassr"
template_dict[name] = (tempelate, replace)

name = "place_of_birth"
tempelate = "Jerry Beck (born February 9, 1955, in New York City) is an American animation historian, author, blogger, and video producer.Beck wrote or edited several books on classic American animation and classic characters.\nJerry Beck was born in New York\n\nEttore Maria Fizzarotti (1916–1985) was an Italian film director and screenwriter. Born in Naples, the son of the director Armando, he debuted as assistant director in the films of his father.\nEttore Maria Fizzarotti was born in Naples\n\n"
replace = "Chongqing"
template_dict[name] = (tempelate, replace)

name = "place_of_death"
tempelate = "Vasily Dmitrievich Tikhomirov, (born March 30, 1876, Moscow, Russia—died June 20, 1956, Moscow), ballet dancer and influential teacher who helped develop the vigorous style and technical virtuosity of the Bolshoi Ballet in Moscow.\nMikhail Tikhomirov died in Moscow\n\nIsaacs died of lung cancer on 25 October 2010 at his home in Harrow Weald, London.\nGregory Isaacs died in London\n\n"
replace = "Chongqing"
template_dict[name] = (tempelate, replace)

name = "plaintiff"
tempelate = "1-800 CONTACTS v. WhenU.com was a legal dispute beginning in 2002 over pop-up advertisements.[1] It was brought by 1-800 Contacts, an online distributor of various brands of contact lenses against WhenU SaveNow, a maker of advertising software.\nThe plaintiff in 1-800 Contacts, Inc. v. WhenU.com, Inc. is 1-800 Contacts\n\nNational Association for the Advancement of Colored People v. Alabama, 357 U.S. 449 (1958), was a landmark decision of the US Supreme Court. Alabama sought to prevent the NAACP from conducting further business in the state.\nThe plaintiff in National Association for the Advancement of Colored People v. Alabama is NAACP\n\n"
replace = "1-800 CONTACTS"
template_dict[name] = (tempelate, replace)

name = "position_held"
tempelate = "Maurice Paul Delorme was a French prelate of the Roman Catholic Church.Delorme was born in Lyon, and ordained a bishop on November 16, 1975.\nThe position held by Maurice Paul Delorme is Catholic bishop\n\nHiram McCullough was a U.S. Congressman from Maryland who served two terms from 1865 to 1869. \nThe position held by Hiram McCullough is United States representative\n\nDavid William Kilgour PC (February 18, 1941 – April 5, 2022) was a Canadian human rights activist. Kilgour ended his 27-year tenure in the House of Commons of Canada as an Independent MP.\nThe position held by David Kilgour is member of the House of Commons of Canada\n\n"
replace = "U.S. representative"
template_dict[name] = (tempelate, replace)

name = "position_played_on_team"
tempelate = "Che Chi Man is a Macanese footballer who plays as a midfielder.\nThe position played on team by Che Chi Man is midfielder\n\nFranco is a youth product of Colombian team Millonarios. After making his debut in 2009 with the senior squad, he became a key defender for the Colombian capital's team.\nThe position played on team by Pedro Franco is defender\n\n"
replace = "forward"
template_dict[name] = (tempelate, replace)

name = "programming_language"
tempelate = "OpenNMS is a free and open-source enterprise grade network monitoring and network management platform. OpenNMS is written in Java, and thus can run on any platform with support for a Java SDK version 8 or higher.\nThe programming language in which OpenNMS was developed is Java\n\nViewVC (formerly ViewCVS) is an open-source tool for viewing the contents of CVS and SVN repositories using a web browser. It is written in Python and the view parameters can be modified directly in a URL using a REST style interface.\nThe programming language in which ViewVC was developed is Python\n\n"
replace = "Python"
template_dict[name] = (tempelate, replace)

name = "recommended_unit_of_measurement"
tempelate = "In physics, coherence length is the propagation distance over which a coherent wave (e.g. an electromagnetic wave) maintains a specified degree of coherence.\ncoherence length can be measured in the unit of metre\n\nPhysical quantities of shear stress are measured in force divided by area. In SI, the unit is the pascal (Pa) or newtons per square meter.\nshear stress can be measured in the unit of pascal\n\n"
replace = "metre"
template_dict[name] = (tempelate, replace)

name = "record_label"
tempelate = "MCA Records was an American record label owned by MCA Records, which later became part of Universal Music Group.\nThe music record label of Forever in My Life is MCA Records\n\nHeadless Heroes of the Apocalypse is an album of American soul music by artist Eugene McDaniels, released in 1971, Atlantic Records.\nThe music record label of Headless Heroes of the Apocalypse is Atlantic Records\n\n"
replace = "MCA Records"
template_dict[name] = (tempelate, replace)

name = "religion"
tempelate = "Giovanni Pietro Volpi (15 May 1585 – 12 September 1636) was a Roman Catholic prelate who served as Bishop of Novara (1629–1636), Titular Bishop of Salona (1622–1629), and Auxiliary Bishop of Novara (1622–1629).\nThe religion Giovanni Pietro Volpi is affiliated with is Catholic Church\n\nThe parish of St Mary the Virgin Wellingborough is in the Archdeaconry of Northampton in the Diocese of Peterborough. St Mary's stands in the Anglo-Catholic tradition of the Church of England.\nThe religion Parish Church of St Mary the Virgin is affiliated with is Anglicanism\n\n"
replace = "no religion"
template_dict[name] = (tempelate, replace)

name = "repealed_by"
tempelate = "The Natives Land Act, 1913 was an Act of the Parliament of South Africa that was aimed at regulating the acquisition of land. The Act was repealed by Abolition of Racially Based Land Measures Act, 1991\nNatives Land Act, 1913 is repealed by Abolition of Racially Based Land Measures Act, 1991\n\nThe Bantu Homelands Constitution Act, 1971 enabled the government of South Africa to grant independence to any \"Homeland\" as determined by the South African apartheid government. The Act was repealed by the Population Registration Act Repeal Act, 1991\nPopulation Registration Act, 1950 is repealed by Population Registration Act Repeal Act, 1991\n\n"
replace = "2018 c16"
template_dict[name] = (tempelate, replace)

name = "shares_border_with"
tempelate = "Eggenwil is a municipality in the district of Bremgarten in the canton of Aargau in Switzerland.\nEggenwil shares border with Bremgarten\n\nBugnein is a commune in the Pyrénées-Atlantiques department in southwestern France which shares border with Audaux.\nBugnein shares border with Audaux\n\n"
replace = "Chongqing"
template_dict[name] = (tempelate, replace)

name = "solved_by"
tempelate = "The non-squeezing theorem, also called Gromov's non-squeezing theorem was first proven in 1985 by Mikhail Gromov.\nNon-squeezing theorem was solved by Mikhail Gromov\n\nIn geometry, Euler's rotation is named after Leonhard Euler, who proved it in 1775 by means of spherical geometry.\nEuler's rotation theorem was solved by Leonhard Euler\n\n"
replace = "Tibor Rado"
template_dict[name] = (tempelate, replace)

name = "statement_describes"
tempelate = "In geometry, Barrow's inequality is an inequality relating the distances between an arbitrary point within a triangle.\nThe statement of Barrow's inequality describes triangle\n\nThe butterfly theorem is a classical result in Euclidean geometry, which can be stated as follows: Let M be the midpoint of a chord PQ of a circle.\nThe statement of butterfly theorem describes circle\n\n"
replace = "polygon"
template_dict[name] = (tempelate, replace)

name = "stock_exchange"
tempelate = "Where is SPS Commerce stock traded? SPS Commerce is traded on the NASDAQ. Our ticker symbol is SPSC. \nThe stock exchange on which SPS Commerce is traded is NASDAQ\n\nNYSE: TPGI) (\"Thomas Properties\") valued at approximately $1.2 billion. The combined company will continue to trade under Parkway's existing ticker symbol, \"PKY\", on the New York Stock Exchange;\nThe stock exchange on which Thomas Properties Group is traded is New York Stock Exchange\n\n"
replace = "The New York Stock Exchange"
template_dict[name] = (tempelate, replace)

name = "subclass_of"
tempelate = "The Howard DGA-4 a.k.a. Mike, and DGA-5 a.k.a. Ike and \"Miss Chevrolet\" was the next in a series of racing aircrafts from Ben Howard.\nHoward DGA-4 is a subclass of aircraft\n\nThe miliaresion (Greek: μιλιαρήσιον, from Latin: miliarensis), is a name used for two types of Byzantine silver coins.\nMiliaresion is a subclass of Byzantine coinage\n\n"
replace = "blot"
template_dict[name] = (tempelate, replace)

name = "subsidiary"
tempelate = "The Canadian National Railway Company is a Canadian Class I freight railway. After the STB moratorium expired, CN purchased Canadian WC subsidiary Algoma Central Railway.\nThe subsidiary of Canadian National Railway is Algoma Central Railway\n\nThe Arkansas State University System, based in Little Rock, serves almost 40,000 students annually on campuses in Arkansas and Queretaro, Mexico, and globally online. The Arkansas State University System includes Arkansas State University\nThe subsidiary of Arkansas State University System is Arkansas State University\n\n"
replace = "Castle Hill Hospital"
template_dict[name] = (tempelate, replace)

name = "symptoms_and_signs"
tempelate = "Vasculitis is a group of disorders that destroy blood vessels by inflammation. Both arteries and veins are affected.\nvasculitis has symptoms such as inflammation\n\nWaterhouse–Friderichsen syndrome (WFS) is defined as adrenal gland failure due to bleeding into the adrenal glands, commonly caused by severe bacterial infection. Typically, it is caused by Neisseria meningitidis.\nWaterhouse-Friderichsen syndrome has symptoms such as bleeding\n\nDientamoebiasis is a medical condition caused by infection with Dientamoeba fragilis, a single-cell parasite that infects the lower gastrointestinal tract of humans. It is an important cause of traveler's diarrhea.\ndientamoebiasis has symptoms such as diarrhea\n\n"
replace = "diarrhea"
template_dict[name] = (tempelate, replace)

name = "therapeutic_area"
tempelate = "Ozone can be administered through site-specific injections and IV. While site-specific injections can help joint pain and wound healing, IV ozone treats diseases such as rheumatology\nozone therapy cures diseases such as rheumatology\n\n"
replace = "diarrhea"
template_dict[name] = (tempelate, replace)

name = "time_of_discovery_or_invention"
tempelate = ""
replace = ""
template_dict[name] = (tempelate, replace)

name = "twinned_administrative_body"
tempelate = "Oulainen (Swedish: Oulainen, also Oulais) is a town and a municipality of Finland. This is a list of municipalities of Denmark which have standing links to local communities ... Lillehammer, Norway.\nOulainen is a twin city with Lillehammer\n\nBarlinek is twinned with: Gryfino, Poland; Courrières, France; Prenzlau, Germany; Schneverdingen.\nSchneverdingen is a twin city with Barlinek\n\n"
replace = "Barlinek"
template_dict[name] = (tempelate, replace)

name = "work_location"
tempelate = "Alejandro Carabias Icaza (born 9 January 1973) is a Mexican politician from the Ecologist Green Party of Mexico. \nAlejandro Carabias Icaza used to work in Mexico City\n\nVictor Leemans (21 July 1901 – 3 March 1971) was a Belgian sociologist, politician and prominent ideologist of the radical Flemish movement in the 1930s. He used to work in Strasbourg.\nVictor Leemans used to work in Strasbourg\n\n"
replace = "Oulainen"
template_dict[name] = (tempelate, replace)

with open(file_name, "wb") as fOut:
        pickle.dump({'template': template_dict}, fOut, protocol=pickle.HIGHEST_PROTOCOL)


