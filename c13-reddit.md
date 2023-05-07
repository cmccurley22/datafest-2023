
- [Divorced From Feelings](#divorced-from-feelings)
  - [Research Question](#research-question)
  - [Context](#context)
  - [Data Wrangaling](#data-wrangaling)
  - [Data Visualization](#data-visualization)
  - [Preparing Data for Sentiment
    Analysis](#preparing-data-for-sentiment-analysis)
  - [Sentiment Analysis](#sentiment-analysis)
  - [Insights](#insights)

# Divorced From Feelings

*Team Technical Difficulties:* Lily Dao, Reuben Lewis, Maya Sivanandan,
Kate McCurley, and Izzie Abilheira

### Research Question

What are common feelings that may create friction in the interaction
between the client and the attorney for a divorce-related case?

### Context

Our group was provided data from the American Bar Association with
information about attorneys, clients, and the interactions between them.
We were particularly interested in the interactions between the
attorneys and the clients regarding cases related to divorce due to the
high-emotion nature of the topic. We pulled in data from Reddit,
specifically r/legaladvice, to gain a better understanding of the tone
that users and commenters use on a more informal site vs. with pro bono
lawyers with the ABA. We ran the text data from the posts and the
conversations through sentiment analysis to understand the common tone
of these conversations and how lawyers can approach these conversations
for the benefit of the client.

### Data Wrangaling

``` r
df_attorneys <- read_csv("./data/attorneys.csv")
```

    ## Rows: 11544 Columns: 8
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr  (6): StateAbbr, AttorneyUno, City, County, StateName, PostalCode
    ## dbl  (1): Id
    ## dttm (1): CreatedUtc
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
df_attorneytimeentries <- read_csv("./data/attorneytimeentries.csv")
```

    ## Rows: 114613 Columns: 6
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr  (3): StateAbbr, TimeEntryUno, AttorneyUno
    ## dbl  (2): Id, Hours
    ## dttm (1): EnteredOnUtc
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
df_categories <- read_csv("./data/categories.csv")
```

    ## Rows: 430 Columns: 4
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (3): StateAbbr, CategoryUno, Category
    ## dbl (1): Id
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
df_clients <- read_csv("./data/clients.csv")
```

    ## Rows: 331426 Columns: 19
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr  (17): StateAbbr, ClientUno, County, StateName, PostalCode, EthnicIdenti...
    ## dbl   (1): Id
    ## dttm  (1): CreatedUtc
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
df_questionposts <- read_csv("./data/questionposts.csv")
```

    ## Warning: One or more parsing issues, call `problems()` on your data frame for details,
    ## e.g.:
    ##   dat <- vroom(...)
    ##   problems(dat)

    ## Rows: 405259 Columns: 5
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (5): Id, StateAbbr, QuestionUno, PostText, CreatedUtc
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
df_questions <- read_csv("./data/questions.csv")
```

    ## Rows: 202879 Columns: 14
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr  (12): StateAbbr, QuestionUno, CategoryUno, Category, SubcategoryUno, Su...
    ## dbl   (1): Id
    ## dttm  (1): AskedOnUtc
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
df_statesites <- read_csv("./data/statesites.csv")
```

    ## Rows: 42 Columns: 7
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (2): StateAbbr, StateName
    ## dbl (5): Id, AllowedAssets, BaseIncomeLimit, PerHouseholdMemberIncomeLimit, ...
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
df_subcategories <- read_csv("./data/subcategories.csv")
```

    ## Rows: 966 Columns: 5
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (4): StateAbbr, CategoryUno, SubcategoryUno, Subcategory
    ## dbl (1): Id
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
df_zip <- read_csv("./uszips.csv") %>%
  rename(PostalCode = zip)
```

    ## Rows: 33788 Columns: 18
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (10): zip, city, state_id, state_name, county_fips, county_name, county_...
    ## dbl  (4): lat, lng, population, density
    ## lgl  (4): zcta, parent_zcta, imprecise, military
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
df_zip
```

    ## # A tibble: 33,788 × 18
    ##    PostalCode   lat   lng city  state_id state_name zcta  parent_zcta population
    ##    <chr>      <dbl> <dbl> <chr> <chr>    <chr>      <lgl> <lgl>            <dbl>
    ##  1 00601       18.2 -66.8 Adju… PR       Puerto Ri… TRUE  NA               17126
    ##  2 00602       18.4 -67.2 Agua… PR       Puerto Ri… TRUE  NA               37895
    ##  3 00603       18.5 -67.1 Agua… PR       Puerto Ri… TRUE  NA               49136
    ##  4 00606       18.2 -66.9 Mari… PR       Puerto Ri… TRUE  NA                5751
    ##  5 00610       18.3 -67.1 Anas… PR       Puerto Ri… TRUE  NA               26153
    ##  6 00611       18.3 -66.8 Ange… PR       Puerto Ri… TRUE  NA                1283
    ##  7 00612       18.4 -66.7 Arec… PR       Puerto Ri… TRUE  NA               64090
    ##  8 00616       18.4 -66.7 Baja… PR       Puerto Ri… TRUE  NA               10186
    ##  9 00617       18.4 -66.6 Barc… PR       Puerto Ri… TRUE  NA               22803
    ## 10 00622       18.0 -67.2 Boqu… PR       Puerto Ri… TRUE  NA                7751
    ## # ℹ 33,778 more rows
    ## # ℹ 9 more variables: density <dbl>, county_fips <chr>, county_name <chr>,
    ## #   county_weights <chr>, county_names_all <chr>, county_fips_all <chr>,
    ## #   imprecise <lgl>, military <lgl>, timezone <chr>

``` r
#load population data from the 2019 census

df_pop_in <- read_csv("./data/ACSDT5Y2019.B01003-Data.csv", skip = 1)
```

    ## New names:
    ## Rows: 3220 Columns: 7
    ## ── Column specification
    ## ──────────────────────────────────────────────────────── Delimiter: "," chr
    ## (5): Geography, Geographic Area Name, Annotation of Estimate!!Total, Mar... dbl
    ## (1): Estimate!!Total lgl (1): ...7
    ## ℹ Use `spec()` to retrieve the full column specification for this data. ℹ
    ## Specify the column types or set `show_col_types = FALSE` to quiet this message.
    ## • `` -> `...7`

``` r
df_pop_narrow <- select(df_pop_in, c("Geography", "Geographic Area Name", "Estimate!!Total"))

df_pop_named <-
  df_pop_narrow %>% 
  rename(id = Geography) %>% 
  separate(
    col = `Geographic Area Name`,
    into = c("County", "state"),
    sep = (",") 
  ) %>%
  mutate_if(is.character, str_trim)

# df_pop_named

st_crosswalk <- tibble(state = state.name) %>%
   bind_cols(tibble(abb = state.abb)) %>% 
   bind_rows(tibble(state = "District of Columbia", abb = "DC"))

# st_crosswalk
 
df_population <- right_join(df_pop_named, st_crosswalk, by = "state")
```

``` r
#merge attorney data based on the unique identifier for the attorney and state

df_attorney_data <-
  merge(df_attorneys, df_attorneytimeentries, by = c("AttorneyUno", "StateAbbr")) %>%
  subset(select = -c(Id.x, Id.y, EnteredOnUtc, TimeEntryUno))

head(df_attorney_data,10)
```

    ##                             AttorneyUno StateAbbr           City
    ## 1  0023FF7C-934D-4974-87A9-B90BE52D4D5B        TX        Houston
    ## 2  0023FF7C-934D-4974-87A9-B90BE52D4D5B        TX        Houston
    ## 3  0023FF7C-934D-4974-87A9-B90BE52D4D5B        TX        Houston
    ## 4  003C4876-C682-4E94-B161-4BE4B5AD0FBD        IL        Chicago
    ## 5  00401285-58EE-4E39-9807-87A570C4B9ED        TX Mount Crawford
    ## 6  00401285-58EE-4E39-9807-87A570C4B9ED        TX Mount Crawford
    ## 7  00401285-58EE-4E39-9807-87A570C4B9ED        TX Mount Crawford
    ## 8  00609EE0-87BE-496A-9847-A711F4569A25        GA        ATLANTA
    ## 9  00609EE0-87BE-496A-9847-A711F4569A25        GA        ATLANTA
    ## 10 00609EE0-87BE-496A-9847-A711F4569A25        GA        ATLANTA
    ##                             County StateName PostalCode          CreatedUtc
    ## 1                           Harris     Texas      77002 2019-11-20 19:17:03
    ## 2                           Harris     Texas      77002 2019-11-20 19:17:03
    ## 3                           Harris     Texas      77002 2019-11-20 19:17:03
    ## 4                             Cook  Illinois      60603 2020-02-13 18:19:41
    ## 5  All Natural Disaster Assistance     Texas      22841 2017-09-06 17:57:52
    ## 6  All Natural Disaster Assistance     Texas      22841 2017-09-06 17:57:52
    ## 7  All Natural Disaster Assistance     Texas      22841 2017-09-06 17:57:52
    ## 8                          Clayton   Georgia      30315 2017-09-21 17:59:20
    ## 9                          Clayton   Georgia      30315 2017-09-21 17:59:20
    ## 10                         Clayton   Georgia      30315 2017-09-21 17:59:20
    ##    Hours
    ## 1    1.0
    ## 2    1.0
    ## 3    0.6
    ## 4    0.5
    ## 5    0.5
    ## 6    0.5
    ## 7    0.6
    ## 8    0.1
    ## 9    0.2
    ## 10   0.2

``` r
#merge question data based on the unique identifier for the question and state

df_question_data <-
  merge(df_questions, df_questionposts, by = c("QuestionUno", "StateAbbr")) %>%
  subset(select = -c(Id.x, Id.y, CategoryUno, SubcategoryUno, TakenOnUtc, ClosedOnUtc, LegalDeadline))

df_question_data <-
  df_question_data %>%
  rename(ClientUno = AskedByClientUno)

df_question_data <-
  df_question_data %>%
  rename(AttorneyUno = ClosedByAttorneyUno)

head(df_question_data,10)
```

    ##                             QuestionUno StateAbbr
    ## 1  00005375-D055-4DE4-8C37-748DC40ADA6E        TN
    ## 2  00005375-D055-4DE4-8C37-748DC40ADA6E        TN
    ## 3  00005375-D055-4DE4-8C37-748DC40ADA6E        TN
    ## 4  00005375-D055-4DE4-8C37-748DC40ADA6E        TN
    ## 5  00005375-D055-4DE4-8C37-748DC40ADA6E        TN
    ## 6  00005375-D055-4DE4-8C37-748DC40ADA6E        TN
    ## 7  00008AE7-5B06-454D-BA0F-969CE8809C33        AK
    ## 8  00011AA0-DE46-498C-AFF1-CF4E5E3E3066        US
    ## 9  00014611-580E-4A22-9A8C-51FDB6B6110F        IN
    ## 10 00023EBF-097B-4F46-81B3-7A495ECE4BFA        MA
    ##                             Category
    ## 1                Family and Children
    ## 2                Family and Children
    ## 3                Family and Children
    ## 4                Family and Children
    ## 5                Family and Children
    ## 6                Family and Children
    ## 7  Work, Employment and Unemployment
    ## 8                              Other
    ## 9                Family and Children
    ## 10          Housing and Homelessness
    ##                                                                     Subcategory
    ## 1                                                        Family/Divorce/Custody
    ## 2                                                        Family/Divorce/Custody
    ## 3                                                        Family/Divorce/Custody
    ## 4                                                        Family/Divorce/Custody
    ## 5                                                        Family/Divorce/Custody
    ## 6                                                        Family/Divorce/Custody
    ## 7                                                                 Worker's Comp
    ## 8  Veterans â€“ Other VA Benefits (Survivorâ€™s Benefits, Death Benefits, etc.)
    ## 9                                                                   Name Change
    ## 10                                                       Housing or Real Estate
    ##                               ClientUno          AskedOnUtc
    ## 1  034B7AAD-02C4-406A-9545-2A34ECC27A4C 2018-02-05 18:40:34
    ## 2  034B7AAD-02C4-406A-9545-2A34ECC27A4C 2018-02-05 18:40:34
    ## 3  034B7AAD-02C4-406A-9545-2A34ECC27A4C 2018-02-05 18:40:34
    ## 4  034B7AAD-02C4-406A-9545-2A34ECC27A4C 2018-02-05 18:40:34
    ## 5  034B7AAD-02C4-406A-9545-2A34ECC27A4C 2018-02-05 18:40:34
    ## 6  034B7AAD-02C4-406A-9545-2A34ECC27A4C 2018-02-05 18:40:34
    ## 7  27A0418D-5F83-4154-8DF9-D1C0DDD85F6F 2020-12-09 21:03:32
    ## 8  97180222-BD4E-4910-8201-99F4B727FF14 2021-07-22 17:23:07
    ## 9  37145D78-7CF7-4C6A-9AFE-8B9010C67047 2021-06-22 16:59:05
    ## 10 0E8FF7DB-9F32-4CCC-8F64-0393739756D4 2021-02-21 14:05:58
    ##                      TakenByAttorneyUno                          AttorneyUno
    ## 1  EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC
    ## 2  EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC
    ## 3  EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC
    ## 4  EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC
    ## 5  EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC
    ## 6  EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC EBD8DA6D-815B-4061-AEC2-D8FCD4275DFC
    ## 7                                  NULL                                 NULL
    ## 8                                  NULL                                 NULL
    ## 9                                  NULL                                 NULL
    ## 10 95C8CF0D-8B61-4DFA-82B8-D7B4757303B7 95C8CF0D-8B61-4DFA-82B8-D7B4757303B7
    ##                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       PostText
    ## 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     There was never a court order. Just mediation. I believe the correct wording was a parenting plan. He wants to pick her up and take her to his home. I've let him do it before but because of the previous incident, I no longer feel comfortable doing that. When I've tried to say no to him picking her up he gets angry and shows up at my home anyways planning to get her. The last time he showed up like that my father who owns the house I'm living in told him not to come back without my permission or unannounced. He wants to pick her up this afternoon band take her to his house. If I don't allow him to do that, will I be in any sort of violation?
    ## 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Regarding mediation, the mediator is not permitted to draft any documents which are submitted to the court.  Your current court Order is in effect until it is modified by an Order signed by the Judge, so just follow that Order.Parenting time and payment of child support are not dependent upon each other.  If Father never paid child support, he would still be entitled to exercise ordered parenting time.Regarding the carseat, Father cannot demand anything from you.  If it's not in the court's Order, you don't have to do it.  It becomes a practical matter of dealing with him.Regarding child support, have you contacted the child support services office in the ### County District Attorney's Office?  They may be able to assist you with the child support collection without any cost to you.Good luck to you.
    ## 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 When you were divorced from your husband, the Court entered Orders at that time.  Those are the Orders which are presently in effect.  Your agreements in mediation do not modify prior orders until you have both signed before a notary public and the Judge then signs the agreed Orders.
    ## 4  The Juvenile Court of the county where your child lives will have jurisdiction over your case.  If Father does not have an Order of Parentage from that Court naming him as the legal father, he has no legal rights at all.  Of course, you have no means to collect child support without an Order.If possible, employ a family law attorney to file a Complaint to Establish Parentage.  The Complaint should request that child support be set back to the birth of the child (less any child support payments made by Father).  Support is calculated using your gross income, Father's gross income, cost of medical insurance for the child and cost of daycare.  The amount may be different if either of you have other qualified children who are minors.  The Court will set child support based upon the Tennessee Child Support Guidelines, and establish a Permanent Parenting Plan.  The Tennessee child support calculator can be accessed at this website:  ###.You can contact the child support services offices in the District Attorney's Office for the Complaint to Establish Parentage and to set child support.  They can do this for you without any cost.  Ask your caseworker if they can assist with a Permanent Parenting Plan.  Most offices do not, as they are only required to assist with child support.In the meantime, you call the shots on ALL of Father's parenting time.  The maternal grandfather is correct that Father is trespassing if he shows up uninvited.
    ## 5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             My ex and I went to mediation at an attorney's office about visitation for our daughter. He (my ex-her father) never paid the lawyer to have the mediation papers finalized in court so there is nothing in writing in regards to visitation or child support payments. What am I legally obligated to do as far as letting him see our daughter right now? He isn't paying child support regularly and he keeps asking for more priveledges (unsupervised visits, picking her up on days other than what we agreed on etc) than we had agreed upon originally. Most recently he fell asleep while our daughter was at his house and he did not get her home on time. It took ###. He also wants me to buy a proper carseat for her in addition to the one we already bought her for my vehicle.
    ## 6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Okay....we were never married. Ex as in ex fiance. Sorry I should have clarified that...thought I marked single never married in my relationship status. So, yeah, no court order for divorce.
    ## 7                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 In ###. They put a plate in my knee. Had to have another surgery to remove the plate and found out that I have a broken screw in my knee. Now I am back at a different doctor for the same knee problem and my knee never healed correctly so now I have to have a knee replacement. I want to see if I have a case against the Doctor Who did the surgery and for my pain and suffering because I have been not able to do my job and now I have been out of work for seven weeks and I am dealing with Workers Comp and I am very stressed. Can you help? I have all the doctors notes but to big of file.
    ## 8                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               So I am wondering if I can still pursue this case and expunge or remove that 2nd dui with the valor act that I was not aware of at that time and or was given the option to use the valor act, and or informed that I had that option As a veteran. My friends through me a welcome party shortly after I returned home from my active duty service from the USMC Jan/2003 -Jan/2007. I was station in Camp ###, NC and served in both wars ### and ###. Separated as a Sgt in the Marine Corps. I have not had any civil,criminals charges against me for the last 14r or ###. I work in Human Resources as an HR Specialist for the ### VA Campus and have been there for ### this Oct/2021. And if possible, can I expunge my first DUI? Please advise. Thank you very much for your time.### ######-######
    ## 9                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           Hello, my name is ### Nun Mawi, mother of one year old Elead, wanting to change his last name. It is misspelled on his Social Security and in the system. Originally was named Elead Hmung in the hospital but I want to change it to Elead Mawia.
    ## 10                                                                                                                                                                                                                                                                          Dear ### - We're sorry to hear you had such a difficult time staying in the housing that ### Properties provided while it was working on your house.  I can imagine the loss of the sleep and the worsening of migraine headaches was very unpleasant.It sounds like you are now moved into the renovated house, and we hope that means you are now able to sleep.You asked if you could take ### Properties to court for the breach of quiet enjoyment you experienced when you were in the alternative place.  While it is possible for you to file a small claim lawsuit against ###, the wait to be heard could be quite long. Perhaps a better approach is to write a letter to ###, explain in detail what you endured, for how long, and how that affected your health. You should attach copies of the police reports to show you did what you could to solve the noise problem. You could ask for a partial credit against future rent. It would not be reasonable to ask for a credit representing the full time you were in the alternative housing because while the noise was an issue, you did have the other benefits of a tenancy - heat, hot water, etc.  We hope this information is helpful to you.### and team
    ##             CreatedUtc
    ## 1  2018-05-10 21:40:29
    ## 2  2018-05-10 21:40:29
    ## 3  2018-05-10 21:40:29
    ## 4  2018-05-10 21:40:30
    ## 5  2018-05-10 21:40:28
    ## 6  2018-05-10 21:40:30
    ## 7  2020-12-09 21:03:46
    ## 8  2021-07-22 17:23:58
    ## 9  2021-06-22 16:59:24
    ## 10 2021-03-05 16:13:43

``` r
#merge categories data based on the unique identifier for the categorey and state

df_categories_data <-
  merge(df_categories, df_subcategories, by = c("CategoryUno", "StateAbbr")) %>%
  subset(select = -c(Id.x, Id.y))

head(df_categories_data,10)
```

    ##                             CategoryUno StateAbbr                 Category
    ## 1  00235B20-0DD4-4664-920F-F684842409BE        TN        Individual Rights
    ## 2  00235B20-0DD4-4664-920F-F684842409BE        TN        Individual Rights
    ## 3  00951395-3B9F-4042-9D2C-47919CC31D60        TX                Education
    ## 4  009EBCC1-D9F0-452B-807B-D8763B49C28F        ND        Individual Rights
    ## 5  009EBCC1-D9F0-452B-807B-D8763B49C28F        ND        Individual Rights
    ## 6  029E5ABF-1A92-40A2-96EC-0F4B15DC9258        PA Housing and Homelessness
    ## 7  02A23E8B-8D73-46D7-A1F8-B0D3A92ABD68        AL      Family and Children
    ## 8  02A23E8B-8D73-46D7-A1F8-B0D3A92ABD68        AL      Family and Children
    ## 9  02A23E8B-8D73-46D7-A1F8-B0D3A92ABD68        AL      Family and Children
    ## 10 0326D0A1-1EA2-47C7-8A29-F4ED057C70CE        SD      Family and Children
    ##                          SubcategoryUno                    Subcategory
    ## 1  E7AFE12F-7523-47B6-B246-EA86D807C171                    Immigration
    ## 2  6D781146-6256-44B5-B784-6BA695F59D5E    Civil/Constitutional Rights
    ## 3  E3AE39AE-95F4-40E5-AF53-EB710898C20E              Special Education
    ## 4  DEBBF247-8A81-45A5-AB81-F9EE7420AA21    Civil/Constitutional Rights
    ## 5  F88F2FF1-E3CB-455B-A358-65F5135D6151                    Immigration
    ## 6  7B795DB7-635C-44CE-95F6-C948088E1D35      Housing or Property Owned
    ## 7  90EAE8EB-DEB3-420C-B97D-9C8FE8819E1F              Wills/Inheritance
    ## 8  D62A5903-3271-4A6C-9F95-722436BFBAAE Adult Guardian/Conservatorship
    ## 9  ED170CA5-7104-4679-ABEF-A1F383F4D7D1         Family/Divorce/Custody
    ## 10 830AB27C-7340-4A8E-A0F7-9956D703980B         Family/Divorce/Custody

``` r
#merge client data and state sites

df_client_state_data <-
  merge(df_clients, df_statesites, by = c("StateAbbr", "StateName")) %>%
  subset(select = -c(Id.x, Id.y, CreatedUtc))

head(df_client_state_data,10)
```

    ##    StateAbbr StateName                            ClientUno    County
    ## 1         AL   Alabama B33D05BC-B71E-4906-AAC9-794C2E95AF74    Etowah
    ## 2         AL   Alabama 27C11F18-2FED-4B3E-B719-CC3923D3FFCF   Colbert
    ## 3         AL   Alabama BA537BAC-4530-42A9-B3AB-1C1BCD911222 Jefferson
    ## 4         AL   Alabama 0BBE815C-17EC-43E9-8B6B-DD20046E0315   Baldwin
    ## 5         AL   Alabama 5CC9B260-21AE-4560-AB0A-079DEC3C0CEB    Etowah
    ## 6         AL   Alabama 13C3ED0B-578E-462E-B14E-DB4FC24C66B9   Chilton
    ## 7         AL   Alabama 14BAD627-6E61-448B-93AF-3136435FB3D7    Mobile
    ## 8         AL   Alabama BF7ACF1C-614C-4E90-81AB-42C2EB37E0D3   Madison
    ## 9         AL   Alabama 8CEC061E-ED90-4A12-8CF7-F0B87AA70835   Madison
    ## 10        AL   Alabama 1C57B14C-7A0F-4CFA-B902-35A36464AB55   Baldwin
    ##    PostalCode  EthnicIdentity  Age                Gender         MaritalStatus
    ## 1       35901       Caucasian   34 I'd rather not answer I'd rather not answer
    ## 2       35661       Caucasian   51                Female   Divorced or Widowed
    ## 3       35094       Caucasian   56                  Male                Single
    ## 4       80109 Caucasian,Other   66                Female   Married / remarried
    ## 5       35901       Caucasian   49                Female   Divorced or Widowed
    ## 6       35045       Caucasian   40                  Male   Married / remarried
    ## 7       36608            <NA>   57                  NULL                  NULL
    ## 8       35805       Caucasian   35                Female   Married / remarried
    ## 9       35758       Caucasian   41                Female                Single
    ## 10      36567       Caucasian NULL                Female                Single
    ##    Veteran Imprisoned NumberInHousehold AnnualIncome AllowedIncome
    ## 1     NULL         No                 3            0         37190
    ## 2       No         No                 2        75000         25390
    ## 3       No         No                 2         1500         25390
    ## 4       No         No                 2        26000         25390
    ## 5       No         No                12            0        143390
    ## 6       No         No                 2        30000         25390
    ## 7     NULL         No                 1        20000         13590
    ## 8       No         No                 4         2400         48990
    ## 9       No         No                 2         1600         25390
    ## 10      No       NULL              NULL         NULL          NULL
    ##    CheckingBalance SavingsBalance InvestmentsBalance AllowedAssets
    ## 1             NULL           NULL               NULL         10000
    ## 2              435           NULL               NULL         10000
    ## 3                1           NULL               NULL         10000
    ## 4              200           NULL               NULL         10000
    ## 5                0              0               NULL         10000
    ## 6              800           NULL               NULL         10000
    ## 7             1000           NULL               NULL         10000
    ## 8                3           NULL               NULL         10000
    ## 9             NULL           NULL               NULL         10000
    ## 10            NULL           NULL               NULL         10000
    ##    BaseIncomeLimit PerHouseholdMemberIncomeLimit IncomeMultiplier
    ## 1            13590                          4720              2.5
    ## 2            13590                          4720              2.5
    ## 3            13590                          4720              2.5
    ## 4            13590                          4720              2.5
    ## 5            13590                          4720              2.5
    ## 6            13590                          4720              2.5
    ## 7            13590                          4720              2.5
    ## 8            13590                          4720              2.5
    ## 9            13590                          4720              2.5
    ## 10           13590                          4720              2.5

``` r
#merge all dataframes into one 

full_data <-
  merge(df_question_data, df_client_state_data, by = c("ClientUno", "StateAbbr")) %>%
  subset(select = -c(QuestionUno, StateName))

head(full_data,10)
```

    ##                               ClientUno StateAbbr            Category
    ## 1  000005F5-A21D-40EA-A242-0CA3C46C0815        LA Family and Children
    ## 2  000005F5-A21D-40EA-A242-0CA3C46C0815        LA Family and Children
    ## 3  00000D61-F53C-4347-9FA5-F24888D61390        IN Family and Children
    ## 4  00000D61-F53C-4347-9FA5-F24888D61390        IN Family and Children
    ## 5  00000D61-F53C-4347-9FA5-F24888D61390        IN Family and Children
    ## 6  00000D61-F53C-4347-9FA5-F24888D61390        IN Family and Children
    ## 7  0000AFD0-5F95-478B-8F32-E3041A55A345        WI   Individual Rights
    ## 8  0000AFD0-5F95-478B-8F32-E3041A55A345        WI   Individual Rights
    ## 9  0000AFD0-5F95-478B-8F32-E3041A55A345        WI   Individual Rights
    ## 10 0001036B-B56D-48E7-BB60-4E64BA5F8B7D        TX Family and Children
    ##                        Subcategory          AskedOnUtc
    ## 1           Family/Divorce/Custody 2019-10-21 15:28:32
    ## 2           Family/Divorce/Custody 2019-10-21 15:28:32
    ## 3                    Child Support 2021-05-10 18:14:00
    ## 4                    Child Support 2021-05-10 18:14:00
    ## 5                    Child Support 2021-05-10 18:14:00
    ## 6                    Child Support 2021-05-10 18:14:00
    ## 7                     Civil Rights 2020-06-09 18:36:06
    ## 8                     Civil Rights 2020-06-09 18:36:06
    ## 9                     Civil Rights 2020-06-09 18:36:06
    ## 10 Family/Divorce/Custody/Adoption 2020-10-15 15:01:40
    ##                      TakenByAttorneyUno                          AttorneyUno
    ## 1  ED76E01E-EDD8-41AC-AF98-24E9E5536A1D ED76E01E-EDD8-41AC-AF98-24E9E5536A1D
    ## 2  ED76E01E-EDD8-41AC-AF98-24E9E5536A1D ED76E01E-EDD8-41AC-AF98-24E9E5536A1D
    ## 3  B162E55A-9445-476D-BFDD-008EAABD61B6 B162E55A-9445-476D-BFDD-008EAABD61B6
    ## 4  B162E55A-9445-476D-BFDD-008EAABD61B6 B162E55A-9445-476D-BFDD-008EAABD61B6
    ## 5  B162E55A-9445-476D-BFDD-008EAABD61B6 B162E55A-9445-476D-BFDD-008EAABD61B6
    ## 6  B162E55A-9445-476D-BFDD-008EAABD61B6 B162E55A-9445-476D-BFDD-008EAABD61B6
    ## 7  309091EC-9D25-4083-A668-F06A915CAA28 309091EC-9D25-4083-A668-F06A915CAA28
    ## 8  309091EC-9D25-4083-A668-F06A915CAA28 309091EC-9D25-4083-A668-F06A915CAA28
    ## 9  309091EC-9D25-4083-A668-F06A915CAA28 309091EC-9D25-4083-A668-F06A915CAA28
    ## 10 511B5566-7E02-46C2-A00A-163F790743FB 511B5566-7E02-46C2-A00A-163F790743FB
    ##                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                PostText
    ## 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Call Southeast ### Legal Services ### office at ###-### or New Orleans Pro Bono at ###-### to see if you qualify for free legal services.  Maybe the New Orleans Family Justice Center at ###-### since you are alleging that he is abusive and is a sex offender.  In addition the LSBA Modest Means Directory is a directory of attorneys who offer legal services at reduced rates
    ## 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Hi, I'm a single mom of ###. Recently there Dad has decided to bring me to court for custody and since he went first I'm having the hardest time finding a free lawyer and I can't afford one. The children have lived with me since birth. There Dad and I have been broken up for ###. I found out he is a sex offender and on top of him being very verbally and mentally abusive I decided to leave him. Now I'm forced to fight him over my kids and I don't know what to do or how to prepare. IV never done anything in the legal system so I don't know how the process works. I'm hoping maybe I could get some tips on how to prepare or find a free lawyer. I feel like IV called everyone. I'm at a lost and I don't want my babies exposed to this man. I need help on how to win this. Please! Thank you so much for your time. I'll be anticipating a response. My number is ###-###.
    ## 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               I have been trying to do that, but they just keep giving me the runaround, ### the noncustodial parent.
    ## 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               You need to petition the court to stop support on the ground that the child is now ###.
    ## 5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               My oldest daughter is 19yrs old, lives with me since she turned ###, been working since then, ex-wife hasn't reported to child support, ex-wife has been collecting money since then, need to stop paying on my oldest.
    ## 6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         I don't know what you mean by giving me the runaround. If you file a petition for emancipation, serving the other party with a copy, the court will rule on it. If you lose (which would be surprising), you can appeal. If the judge does not rule at all, three is a procedure to deal with that. You may need to get a lawyer to help you.
    ## 7  Hi ###,The FBI has been investigating in search of out of town agitators.  The stories I've heard are FBI agents questioning individuals at the police stations. It is likely these are FBI agents based on what I understand to be going on. You and your son have rights and you are right to be concerned, and to arm yourself with those rights.  ###) Unless you are under arrest or subject to an arrest warrant (you or your son), you do not have to answer their questions. I would recommend having an attorney present if you are going to speak to them.  ###) You do not have to let them in your house.  If anything, step outside to speak to them or stay in the doorway.  Unless they have a warrant signed by a judge, you do not have to let them in, or again, an arrest warrant with your name on it, you do not have to speak to them. They need your consent to enter. ###) Ask to see their badge/ID and get their names and IDs if they come back. ###) If they try to contact your son, advise him the same things.  He should definitely have his lawyer present or discuss with his lawyer since he was arrested.  I would not advise calling them back. I am attaching a know your rights about when the police are at your door from ACLU for your information.  If you have more questions on your rights, I would contact the Wisconsin ACLU.  They may have additional insight and advice to offer on this specific situation since it isn't happening to just you.  My advice would be to reach out to the ACLU regardless and let them know this happened.  Organizations like ACLU may be tracking these incidents.  The FBI seems to be trying to build a certain narrative around the protesters in an effort to charge them with federal crimes. ACLU of WisconsinExecutive Director: ### ############, WI 5######0###United States###Web: http://www.aclu-wi.orgI hope this helps. Please let me know if you have any further questions. ###
    ## 8                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Yesterday the FBI showed up at my door. Three men in black suits, banged on my door. The men did not show me an ID or badge, but were let in by my neighbor who claims he saw the ID. My neighbor also told me he is ex-FBI. My son was arrested for looting downtown during the protest. The men claimed they wanted to ask him information to find out-of-town agitators and his charges are between him and the local police. My son has not contacted them because we do not know if he should have an attorney first. I do not understand why they need to show up unexpectedly for information and bang on the door! I do not feel safe. They did not say they would return. I told them what I knew according to the questions they asked. My son uses my address for mail but does not live here. They gave me a ### FBI contact number. I do not trust anyone who approaches my home like this and I now ask if they are really FBI. I have not found any information about what my rights are and what if anything I may need to do anything . Is this normal behavior of how the FBI handles gathering information? Thank you for your time. D. Nehrkorn
    ## 9                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Thank You for the fast reply and clear information!!! ### Nehrkorn
    ## 10                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Hello ###,Lone Star Legal Aid may be able to help with finding a lawyer to represent you.  I understand from the information you gave that you have a legal deadline, so you if you want to try Lone Star you can call 800-### from ###.m. to ###.m. Monday-Friday.If turns out you don't have a legal deadline set yet, or if you want to read more about Lone Star Legal Aid, you can try their website (###/) and click on the Get Help link near the top right of the home page.Another place that might be helpful, but that does not provide a lawyer to represent you, is the CPS Family Helpline provided by the Texas Legal Service Center (https://www.tlsc.org/family).  They do not provide a lawyer to represent you in court, but they have lawyers who can answer questions on the phone and provide you with information.  Their number is ###-### and they are available from ###.m. - ###.m. Monday-Friday.I wish you the best.
    ##             CreatedUtc           County PostalCode     EthnicIdentity Age
    ## 1  2019-10-23 19:10:25 Jefferson Parish      70094          Caucasian  29
    ## 2  2019-10-21 15:28:53 Jefferson Parish      70094          Caucasian  29
    ## 3  2021-05-10 20:04:04           Marion      46214 Latino or Hispanic  42
    ## 4  2021-05-10 19:14:04           Marion      46214 Latino or Hispanic  42
    ## 5  2021-05-10 18:14:03           Marion      46214 Latino or Hispanic  42
    ## 6  2021-05-11 13:20:14           Marion      46214 Latino or Hispanic  42
    ## 7  2020-06-10 14:25:40             Dane      53704          Caucasian  48
    ## 8  2020-06-09 18:36:13             Dane      53704          Caucasian  48
    ## 9  2020-06-11 00:18:34             Dane      53704          Caucasian  48
    ## 10 2020-10-17 14:52:39       Washington      77833   African American  29
    ##    Gender       MaritalStatus Veteran Imprisoned NumberInHousehold AnnualIncome
    ## 1  Female              Single      No         No                 4        10000
    ## 2  Female              Single      No         No                 4        10000
    ## 3    Male Married / remarried      No         No                 5        50000
    ## 4    Male Married / remarried      No         No                 5        50000
    ## 5    Male Married / remarried      No         No                 5        50000
    ## 6    Male Married / remarried      No         No                 5        50000
    ## 7  Female              Single      No         No                 1        27000
    ## 8  Female              Single      No         No                 1        27000
    ## 9  Female              Single      No         No                 1        27000
    ## 10 Female              Single      No         No                 3          783
    ##    AllowedIncome CheckingBalance SavingsBalance InvestmentsBalance
    ## 1          70230               2           NULL               NULL
    ## 2          70230               2           NULL               NULL
    ## 3          60790             200           NULL               NULL
    ## 4          60790             200           NULL               NULL
    ## 5          60790             200           NULL               NULL
    ## 6          60790             200           NULL               NULL
    ## 7          13590             676           NULL               NULL
    ## 8          13590             676           NULL               NULL
    ## 9          13590             676           NULL               NULL
    ## 10         37190               0           NULL               NULL
    ##    AllowedAssets BaseIncomeLimit PerHouseholdMemberIncomeLimit IncomeMultiplier
    ## 1          5e+05           13590                          4720              4.0
    ## 2          5e+05           13590                          4720              4.0
    ## 3          1e+04           13590                          4720              2.5
    ## 4          1e+04           13590                          4720              2.5
    ## 5          1e+04           13590                          4720              2.5
    ## 6          1e+04           13590                          4720              2.5
    ## 7          2e+04           13590                          4720              4.0
    ## 8          2e+04           13590                          4720              4.0
    ## 9          2e+04           13590                          4720              4.0
    ## 10         1e+04           13590                          4720              2.5

### Data Visualization

We visualized the divorce-related data per state.

<img src="images/divorce_map.png" width="30%" style="display: block; margin: auto;" />

### Preparing Data for Sentiment Analysis

``` r
#Run the section below once to clean the `CreatedUtc` column and change to date/time
# full_data <-
#   full_data %>%
#   mutate(
#     CreatedUtc = if_else(
#       str_detect(CreatedUtc, "^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$"),
#       CreatedUtc,
#       NA_character_
#     ),
#     CreatedUtc = ymd_hms(CreatedUtc)
#   )



client_first_posts <-
  full_data %>%
    filter((str_detect(Subcategory, "[Dd]ivorce"))) %>%
    arrange(CreatedUtc) %>%
    group_by(ClientUno) %>%
    slice(1) %>%
    arrange(CreatedUtc) %>%
    select(PostText, ClientUno, CreatedUtc, StateAbbr, AttorneyUno)
# client_first_posts

client_posts <-
  client_first_posts %>% 
  ungroup() %>% 
  select(PostText)
client_posts
```

    ## # A tibble: 45,908 × 1
    ##    PostText                                                                     
    ##    <chr>                                                                        
    ##  1 "hello and thank you first for participating with this service:I have a ###.…
    ##  2 "Hi, I am separated on the process of signing the MSA. My husband fire an at…
    ##  3 "Hi ###,Good question. I can assist you with this. To confirm, are you okay …
    ##  4 "My husband moved out of the house on ###,after stating he wanted to seperat…
    ##  5 "I am looking to Change my ######mo old daughters last name. She has my maid…
    ##  6 "IN THE CIRUIT COURTTWENTIETH JUDICIAL CIRCUITST. ### COUNTY, ILLINOIS  ### …
    ##  7 "Dear Ms. Long,Apparently you do not understand the legal situation or the j…
    ##  8 "Hi ### - To answer your first question:  No.  You need a court order.  You …
    ##  9 "###,    Before you send these, you should prepare either a paper document, …
    ## 10 "I was granted a divorce on ### and in the divorce my husband the husband wi…
    ## # ℹ 45,898 more rows

``` r
#export data to csv from the first post text from any divorce related subcategory
write.csv(client_posts, './data/firstClientPosts.csv', row.names = FALSE)
```

``` r
#compiling the of unresolved, unopened, and resolved divorce related posts from the ABA

posts_unresolved <-
  full_data %>%
  filter((str_detect(Subcategory, "[Dd]ivorce"))) %>%
  filter(AttorneyUno != "NULL") %>% 
  select(PostText)

posts_unopened <-
  full_data %>%
  filter((str_detect(Subcategory, "[Dd]ivorce"))) %>%
  filter(AttorneyUno == "NULL") %>% 
  select(PostText)

posts_resolved <-
  full_data %>%
  filter((str_detect(Subcategory, "[Dd]ivorce"))) %>%
  filter(AttorneyUno != "NULL") %>% 
  select(PostText)
  
head(posts_unresolved,10)
```

    ##                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               PostText
    ## 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Call Southeast ### Legal Services ### office at ###-### or New Orleans Pro Bono at ###-### to see if you qualify for free legal services.  Maybe the New Orleans Family Justice Center at ###-### since you are alleging that he is abusive and is a sex offender.  In addition the LSBA Modest Means Directory is a directory of attorneys who offer legal services at reduced rates
    ## 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Hi, I'm a single mom of ###. Recently there Dad has decided to bring me to court for custody and since he went first I'm having the hardest time finding a free lawyer and I can't afford one. The children have lived with me since birth. There Dad and I have been broken up for ###. I found out he is a sex offender and on top of him being very verbally and mentally abusive I decided to leave him. Now I'm forced to fight him over my kids and I don't know what to do or how to prepare. IV never done anything in the legal system so I don't know how the process works. I'm hoping maybe I could get some tips on how to prepare or find a free lawyer. I feel like IV called everyone. I'm at a lost and I don't want my babies exposed to this man. I need help on how to win this. Please! Thank you so much for your time. I'll be anticipating a response. My number is ###-###.
    ## 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Hello ###,Lone Star Legal Aid may be able to help with finding a lawyer to represent you.  I understand from the information you gave that you have a legal deadline, so you if you want to try Lone Star you can call 800-### from ###.m. to ###.m. Monday-Friday.If turns out you don't have a legal deadline set yet, or if you want to read more about Lone Star Legal Aid, you can try their website (###/) and click on the Get Help link near the top right of the home page.Another place that might be helpful, but that does not provide a lawyer to represent you, is the CPS Family Helpline provided by the Texas Legal Service Center (https://www.tlsc.org/family).  They do not provide a lawyer to represent you in court, but they have lawyers who can answer questions on the phone and provide you with information.  Their number is ###-### and they are available from ###.m. - ###.m. Monday-Friday.I wish you the best.
    ## 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      I need a lawyer
    ## 5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 After re-hearing the judge signed off on my ex-husband's proposed parenting plan nearly verbatim, despite evidence, the best interest of the children or even the original judgment that was ordered after ###. This new order includes having our minor children attend a school district in which neither myself nor my ex-husband reside, forcing our ### ### to commute to school upwards of ###-###. My ex-husband has again testified since this order was made that he does not live in that school district and the judge repeatedly said that it's not her problem.I have been unable to locate any appeal case where this has happened previously. Are you aware of any cases where a judge has ordered ### to attend a school district where neither parent lives or what verbiage would I use in my appellate brief for this part of my appeal? Thank you for your help.
    ## 6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Case was dismissed, so I am closing this out.  You would be well-advised to retain an attorney.
    ## 7                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         There are articles on guardianship (which is custody for someone who is not a parent) and adoption on Legal Aid of ###' website - ###.  They also have forms that can be downloaded or filled in and printed out. You will look for the Family tab and click that.Guardianship gives you custody of the child and full authority to get medical help for him; to get him into school; etc. It still leaves his parents having rights such as visitation if wanted and it is only in effect until the child is ###. Adoption terminates all rights of the parents and you become the parent. If you are married, you and your husband should both Petition for adoption so you are both the child's parents. It is really just a matter of what you consider is in this child's best interest and what his mother is wanting also. If she agrees to either guardianship or adoption, she can sign a Consent. The father will have to be served with notice but, if he indicates he has no objection, a Consent can be sent to him to sign also.I suggest you read and review all information on the website. Then, if you have more specific questions, reply back. Your question is now in my responses box.
    ## 8  My sister and her husband (not the biological father) kicked her son out. His home life was not healthy and my sister's husband is verbally abusive to my nephew. He is a teenage special needs minor, with learning disabilities. Her husband refuses to acknowledge that my sister's son has any type of learning disability or their special need so he gets very angry with him. He was not allowed in certain parts of the home. He has basically been taking care of himself, the best he can, for a while now. I could go on but I feel I should just sum it up with it was not a safe, healthy, learning or loving environment to spend any time in let alone his formative years. If you need more details I am willing to supply them.My nephews biological father is currently serving in prison for soliciting minor, child pornography, something along those lines. I believe he has a sentence of ###. I didn't know if that would be an issue. I can supply his name if needed.My sister is cooperative. I have not discussed with her yet about full adoption, but that is my ultimate goal to fully adopt my nephew and give him the life he deserves. I have a special needs teenager already and have taken classes in college with a focus on youth and adolescent psychology and the have participated in parent/caregivers group meets that focus specifically on special needs children care. I know I have the ability and the knowledge to make his life full but I don't know where to start. His mother was not meeting his medical needs. I desperately need to get him a mental assessment. I also need to get him into regular therapy as he has been traumatized and I fear along with his disabilities he is suffering with PTSD. I need full parental rights so I can put them on my insurance, so I can get him enrolled in school and get his current medical records along with any other documents that I will need.I guess I just don't know where to begin with the whole process. I am in the process of getting a larger home to accommodate another teenager because I know that it's important for him to have his own personal space to retreat. So he is currently staying with my parents. They have a wonderful and loving  home and are absolutely willing to take him in but they are ###. My mother has expressed to me she has no clue how to raise a child with his needs. So, where do I start? What documents do I need to supply? What do I need to get from my sister? Where do I go to start the process?
    ## 9                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           God bless you for taking care of your grandchildren AND for being a foster parent!  Actually, I think you are making this particular suation harder than it needs to be.  If the mother contacted you about adopting her child, then obviously she is willing to sign a Consent to Adopt form and no termination of parental rights proceeding would be needed as to the mother.  That is a really, really good thing because there are no ### forms for terminating a parents rights and it is a very detailed and complex procedure. Now the issue that you haven't mentioned is your son - will be also consent to you adopting his child?  If he is also willing to sign a Consent to Adopt form, you are in great shape!  If he will not, however, then you are facing a termination of parental rights proceeding against your son.  Most Clerk of Superior Court's offices will provide you with the appropriate adoption forms and even a check-list of what you will need to file.  ALWAYS try to get both parents to sign Consent to Adopt forms if possible.  The process will be massively easier!  Good luck and best wishes.
    ## 10                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Our son is currently incarcerated. He has two children by different mothers, who we currently have court-ordered guardianship of. One of the mothers recently contacted us and asked if we would like to adopt the one grandson who she is the mother to. Having been a foster parent and adopted children ourselves, I know that a parent's rights would need to be terminated prior to adoption. My question is, is that a process that an individual can do on their own.? I know many legal matters can be handled by simply filling out the appropriate form, and I didn't know if this was one of those situations. We have contacted an attorney and the price they quoted us was between ### $###, which they want the majority of upfront. That is why I was curious if it terminating parental rights would be something simple that could be done without a lawyer. Thank you for your time and service!

``` r
head(posts_resolved,10)
```

    ##                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               PostText
    ## 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Call Southeast ### Legal Services ### office at ###-### or New Orleans Pro Bono at ###-### to see if you qualify for free legal services.  Maybe the New Orleans Family Justice Center at ###-### since you are alleging that he is abusive and is a sex offender.  In addition the LSBA Modest Means Directory is a directory of attorneys who offer legal services at reduced rates
    ## 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Hi, I'm a single mom of ###. Recently there Dad has decided to bring me to court for custody and since he went first I'm having the hardest time finding a free lawyer and I can't afford one. The children have lived with me since birth. There Dad and I have been broken up for ###. I found out he is a sex offender and on top of him being very verbally and mentally abusive I decided to leave him. Now I'm forced to fight him over my kids and I don't know what to do or how to prepare. IV never done anything in the legal system so I don't know how the process works. I'm hoping maybe I could get some tips on how to prepare or find a free lawyer. I feel like IV called everyone. I'm at a lost and I don't want my babies exposed to this man. I need help on how to win this. Please! Thank you so much for your time. I'll be anticipating a response. My number is ###-###.
    ## 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Hello ###,Lone Star Legal Aid may be able to help with finding a lawyer to represent you.  I understand from the information you gave that you have a legal deadline, so you if you want to try Lone Star you can call 800-### from ###.m. to ###.m. Monday-Friday.If turns out you don't have a legal deadline set yet, or if you want to read more about Lone Star Legal Aid, you can try their website (###/) and click on the Get Help link near the top right of the home page.Another place that might be helpful, but that does not provide a lawyer to represent you, is the CPS Family Helpline provided by the Texas Legal Service Center (https://www.tlsc.org/family).  They do not provide a lawyer to represent you in court, but they have lawyers who can answer questions on the phone and provide you with information.  Their number is ###-### and they are available from ###.m. - ###.m. Monday-Friday.I wish you the best.
    ## 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      I need a lawyer
    ## 5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 After re-hearing the judge signed off on my ex-husband's proposed parenting plan nearly verbatim, despite evidence, the best interest of the children or even the original judgment that was ordered after ###. This new order includes having our minor children attend a school district in which neither myself nor my ex-husband reside, forcing our ### ### to commute to school upwards of ###-###. My ex-husband has again testified since this order was made that he does not live in that school district and the judge repeatedly said that it's not her problem.I have been unable to locate any appeal case where this has happened previously. Are you aware of any cases where a judge has ordered ### to attend a school district where neither parent lives or what verbiage would I use in my appellate brief for this part of my appeal? Thank you for your help.
    ## 6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Case was dismissed, so I am closing this out.  You would be well-advised to retain an attorney.
    ## 7                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         There are articles on guardianship (which is custody for someone who is not a parent) and adoption on Legal Aid of ###' website - ###.  They also have forms that can be downloaded or filled in and printed out. You will look for the Family tab and click that.Guardianship gives you custody of the child and full authority to get medical help for him; to get him into school; etc. It still leaves his parents having rights such as visitation if wanted and it is only in effect until the child is ###. Adoption terminates all rights of the parents and you become the parent. If you are married, you and your husband should both Petition for adoption so you are both the child's parents. It is really just a matter of what you consider is in this child's best interest and what his mother is wanting also. If she agrees to either guardianship or adoption, she can sign a Consent. The father will have to be served with notice but, if he indicates he has no objection, a Consent can be sent to him to sign also.I suggest you read and review all information on the website. Then, if you have more specific questions, reply back. Your question is now in my responses box.
    ## 8  My sister and her husband (not the biological father) kicked her son out. His home life was not healthy and my sister's husband is verbally abusive to my nephew. He is a teenage special needs minor, with learning disabilities. Her husband refuses to acknowledge that my sister's son has any type of learning disability or their special need so he gets very angry with him. He was not allowed in certain parts of the home. He has basically been taking care of himself, the best he can, for a while now. I could go on but I feel I should just sum it up with it was not a safe, healthy, learning or loving environment to spend any time in let alone his formative years. If you need more details I am willing to supply them.My nephews biological father is currently serving in prison for soliciting minor, child pornography, something along those lines. I believe he has a sentence of ###. I didn't know if that would be an issue. I can supply his name if needed.My sister is cooperative. I have not discussed with her yet about full adoption, but that is my ultimate goal to fully adopt my nephew and give him the life he deserves. I have a special needs teenager already and have taken classes in college with a focus on youth and adolescent psychology and the have participated in parent/caregivers group meets that focus specifically on special needs children care. I know I have the ability and the knowledge to make his life full but I don't know where to start. His mother was not meeting his medical needs. I desperately need to get him a mental assessment. I also need to get him into regular therapy as he has been traumatized and I fear along with his disabilities he is suffering with PTSD. I need full parental rights so I can put them on my insurance, so I can get him enrolled in school and get his current medical records along with any other documents that I will need.I guess I just don't know where to begin with the whole process. I am in the process of getting a larger home to accommodate another teenager because I know that it's important for him to have his own personal space to retreat. So he is currently staying with my parents. They have a wonderful and loving  home and are absolutely willing to take him in but they are ###. My mother has expressed to me she has no clue how to raise a child with his needs. So, where do I start? What documents do I need to supply? What do I need to get from my sister? Where do I go to start the process?
    ## 9                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           God bless you for taking care of your grandchildren AND for being a foster parent!  Actually, I think you are making this particular suation harder than it needs to be.  If the mother contacted you about adopting her child, then obviously she is willing to sign a Consent to Adopt form and no termination of parental rights proceeding would be needed as to the mother.  That is a really, really good thing because there are no ### forms for terminating a parents rights and it is a very detailed and complex procedure. Now the issue that you haven't mentioned is your son - will be also consent to you adopting his child?  If he is also willing to sign a Consent to Adopt form, you are in great shape!  If he will not, however, then you are facing a termination of parental rights proceeding against your son.  Most Clerk of Superior Court's offices will provide you with the appropriate adoption forms and even a check-list of what you will need to file.  ALWAYS try to get both parents to sign Consent to Adopt forms if possible.  The process will be massively easier!  Good luck and best wishes.
    ## 10                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Our son is currently incarcerated. He has two children by different mothers, who we currently have court-ordered guardianship of. One of the mothers recently contacted us and asked if we would like to adopt the one grandson who she is the mother to. Having been a foster parent and adopted children ourselves, I know that a parent's rights would need to be terminated prior to adoption. My question is, is that a process that an individual can do on their own.? I know many legal matters can be handled by simply filling out the appropriate form, and I didn't know if this was one of those situations. We have contacted an attorney and the price they quoted us was between ### $###, which they want the majority of upfront. That is why I was curious if it terminating parental rights would be something simple that could be done without a lawyer. Thank you for your time and service!

``` r
head(posts_unopened,10)
```

    ##                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     PostText
    ## 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Ok. So I received a warrant for an Insurance ticket I got back during the covid-###. My problem is I made the mistake of picking up my ex and it's turned bad they keep making threats to call police if I get them out of my car. what do I have the right to do without involving the police or being around if they arrive
    ## 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         I need a little more information.  Who are the intervenors? Why were they given temporary custody?
    ## 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          My case number is ###My question is what are my rights to my children of the intervenors are granted temporary legal n physical custody of my kids. I am being blocked from all health information n schoolingi nformation n am not being allowed phone contact. Is this legal?? They have blocked my numbers and will not give me any answers regarding my kids.
    ## 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      I need help with my divorce paper my husband send it to me by mail.so I can understand befor sgin and what next step to take .I live in Pflugerville TXand I have pending ### not court date plece can you help me.call me at ###-###
    ## 5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Hello,My name is ###, I am ### ###. My cousin is a US citizen but she currently lives in ### with her parents. Her parents want her to come and finish high school here in Mesa ###. I would like to know what documents are necessary to fill out so I can have temporary guardianship until she turns ###?
    ## 6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             The mother of my kids died a month ago.I have been with my kids sine birth i signed there birth certificates and all.They stay with me now.My question was do i still have to go to court to gt custody (ligtamized) or is there a document i can go get to so i have custody?
    ## 7                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       I moved to ### in ######, I have a current custody and parenting order in ### county in Texas and need a divorce because I want to remarry. I am unsure how and where to file due to Texas having a current order and no consent has been filed for another state to have jurisdiction in the case. ### Herron and I have not been living together since ### of ###.
    ## 8  Hello ###, Thanks for Posting.Well, I am a little confused about your situation. You have a current custody and parenting order in ### County Texas, but you are not divorced in Texas is this correct. All of the States have adopted the Uniform Foreign Judgment Act. So there should be no problem you taking your Texas  Order concerning custody and filing it in ###  Iin Texas you can file a court order or the decree under the Texas Civil Practice and Remedies  35.###. You can file any order or decree or judgment from another foreign Court.You will need to file an Affidavit with the information contained in Civil Practice and Remedies 35.###.  What the affidavit needs to contain is contained in ###.  You can go to the Clerk of Courts and you can file it there. There will be a filing charge for filing it and you may have to send a copy of the Affidavit you have filed copy to the other party of the Order, Decree or Judgment certified mail with return receipt at her last known address.  If you want to waiver of the filing fee you will need to complete the forms for Waiver of Filing Fees. You will also need to sign an Certificate of Service which states that you sent a copy of the Order Decree or Judgment  by mail to the last known address postage prepaid to the other party involved.The small certified mail receipt will need to be filed with the Clerk of Courts in the case. Also the attached this Certificate of Service will need to be filed with the Clerk also. You might want to check with an attorney in ### as to the procedure for filing your custody and parenting order in ### see if you can't file for a divorce based on that filing. Of course you could file for a divorce in ### county and complete it there. You are looking at ###.
    ## 9                                                                                                                                                                                                                                                                                                                                                              Hello, I am currently married and my wife and I have been separated since March (###).  She was pregnant when she left and has been living with another man until our daughter was born on ###th, when she moved in with her parents.I have been offering her ### help and any form of marriage restoration since she has left, and she has only accepted some help financially with a few Dr bills.  I have attended all of the Dr appointments (except ###) and the birth with her.  I have offered to leave the house for her to move in.Recently I left ### for ### (I know it was a mistake).  My family contacted the police and I was put as a missing person until I made contact and came home.  I was by myself and to my knowledge did not do anything illegal.I am able to see our daughter at her parents home whenever she allows, however she told me it has to be supervised.  I'm also allowed to take our daughter to see my family if I'm supervised.I am now planning on moving to Tucson in a few weeks, and she has agreed to take over home payments and move in.  What can I do to protect myself and my daughter from any future legal issues?  My wife is planning on filing a divorce, and I want what's best for us as a separated family.  Currently things are civil. I don't like the situation, but I trust her to take care of our daughter, though she does not trust me.  I just don't want to loose my daughter.Thank you
    ## 10                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     My ex sister in law was in the middle of custody/visitation proceedings in ### and violated a court order in September and moved to ###, Wyoming with my ###. We are looking to see if we will need to hire a lawyer in Wyoming in order to have my niece returned to ### until the proceedings are concluded. Additionally, should we contact the ### County Sheriff's office about the bench warrant in ### Parish, ###, or contact the courthouse directly. Thanking you for your time and guidance.V/R,### ######

``` r
#export data to csv to be processed in python
write.csv(posts_unresolved, './posts_unresolved.csv', row.names = FALSE)
write.csv(posts_resolved, './posts_resolved.csv', row.names = FALSE)
write.csv(posts_unopened, './posts_unopened.csv', row.names = FALSE)
```

### Sentiment Analysis

The compiled CSV data of the unresolved, resolved, and unopened
divorce-related ABA posts were then used to conduct sentiment analysis
in Python. We made two sentiment analyses: one based on the
divorce-related Reddit posts and comments from r/legaladvice and the
other based on the divorce-related posts and replies from the pro bono
lawyers from the ABA.

All of this processing can be found in the ‘python-processing’ folder.

<img src="images/compare_emotions.png" width="30%" style="display: block; margin: auto;" />

<img src="images/overall_emotions.png" width="30%" style="display: block; margin: auto;" />

### Insights

Through looking at the data provided to us and data from Reddit, we
found some interesting trends within the sentiment analysis. One trend
we noticed was the language used in correspondence (for both Reddit and
ABA divorce cases) had a significant amount of fear detected, more than
any other emotion detected (as seen on our slides). The emotion level
for fear was between 0.4 and 0.5 on a scale from zero to one. It is
important to note that ABA correspondence has more fear than Reddit
correspondence and when the attorney comes into play, the fear level
increases. Reddit likely does not experience as high levels of fear
detected in the speech because of the informality and anonymity of the
platform. Also, by the time a client reaches the step of reaching out to
a lawyer, their fear level has had time to increase. Knowing this, ABA
attorneys should adjust the language they use to be more approachable
which would put the client at ease. We would expect this to decrease the
fear level and increase the happiness level of ABA correspondence.

<img src="images/word_cloud.png" width="30%" style="display: block; margin: auto;" />

We then chose to look at how the resolution of posts correlates with
their emotional score. We had 3 categories of resolution based on
whether posts had a \`TakenByAttorneyUno\` and \`ClosedByAttorneyUno\`
(resolved), only a \`TakenByAttorneyUno\` (unresolved), or neither
(unopened). As shown in our slides, we found that the unopened posts had
higher scores in anger and sadness but lower in fear when compared to
the other two categories. This could be because a more fearful tone is
interpreted to be more urgent, while high anger and sadness can be seen
as hysterical or hard to deal with. ABA attorneys could be encouraged to
work with emotionally intense questions to reach a larger number of
clients. The ABA could also provide more resources to clients on how to
engage with the attorneys so that their issues are conveyed clearly and
reasonably, and so they can be more likely to receive assistance. A
potential option for this is a message template for specific categories
or subcategories, so clients can more easily share their situation and
attorneys can more easily gain key information. This could also
potentially reduce the time needed to resolve issues.

  
