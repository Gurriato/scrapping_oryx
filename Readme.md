# Russian invasion of Ukraine Dashboard
Still WIP but working

Why I built this scrapper? because others had a lot of inconsistencies. Even with errors this is most accurate Oryx scrapper you are going to find.
Why others are not as accurate? because Oryx blog is manually feed. Therefore, there are a lot of exceptions you had to code in order to capture all the data and all other projects were created long time ago, so there are new exceptions not capture by their code.

Commits are welcome

#### Be aware
There are some equipment not been capture by the scrapper due coding errors on Oryx webpage
- Coding errors in Oryx page
    - 2 Ucranian tanks (2 M-55S)
        - Coding error in Oryx webpage, my code is unable to capture this, added manually
    - 29 unkown Russian Equipment. Impact on the df: (probably most of them are because they are )
        - 11 220mm TOS-1A appeari+ng as MT-LB with 140mm Ogon-18 MRLS
        - UAZ PAtriot jeep labeled as LUAZ-969
        - MT-LB captured 69 & 70 missing a comma between them
        - Unkown error 8 UAZ-23632 (not scraped) and 8 UAZ-23632-148-64 not labeled correctly
            - Still missing 10 elements 😓
- Data errors in Oryx page:
    - UA:
        - 1 UAZ-3151: (23, destroyed) -> should be  1 UAZ-3151: (1, destroyed) On Russian equipment (@31/10/2023) Fixed on an update(@06/11/2023)
        - BMP-1(P) proof 64 destroyed is missing, also miscounted, total number 349 (+1) (@31/10/2023)
        - BMP-2(K) is miscounted. Total number == 181 (-1) (@31/10/2023)
        - Unknown BMP-1/2 is miscounted. Total number == 27 (-1) (@31/10/2023)
        - BTR-70 proof 1 is missing, therefore total number = 28 (-1) (@31/10/2023)
        - AT105A Saxon is miscounted, total number = 13 (-1) (@31/10/2023)
        - 155mm M777A2 howitzer is miscounted, total number = 70 (+1) (@31/10/2023)
        - 122mm BM-21 Grad is missing proof 16, therefore total number 37 (-1) (@31/10/2023)
        - 5P85D/S (launcher for S-300PS) 13 and 14 are repeated? (@31/10/2023)
        - A1-SM Fury case 35 = 32 and miscounted. Total number = 55 (-1) (@31/10/2023)
        - KrAZ-255B miscounted total number 16(-1) (@31/10/2023)
        - GAZ-66 Format on first case, also miscounted total 107(-1) (@31/10/2023)
        - MAZ-537 miscounted, total 3 (+1) (@31/10/2023)
        - VEPR is duplicated, one under Armoured Fighting Vehicles the other under Mine-Resistant Ambush Protected (MRAP)
        - ZiL-131 case 71 format (@06/11/2023)
    - RU:
        - T-72B3 miscounted, total 347 (-2)
        - T-72B3 Obr. 2016 miscounted, total 240 (-1)
        - T-80BV miscounted, total 422 (-1)
        - T-80U miscounted, total 93 (-1)
        - unkown tank, miscounted, total 287 (-3)
        - MT-LB miscounted, total 508 (+1)
        - Unknown AFV miscounted, total 208 (+1)
        - BMP-1(P) miscounted, total 543 (-2)
        - BMP-3 miscounted, total 296 (-1)
        - PTS-2  tracked amphibious transport, miscounted, total 15 (-1)
        - PMP floating bridge miscounted, total 11 (-1)
        - 9P149 Shturm-S miscounted, total 36 (-1)
        - 100mm MT-12 anti-tank gun miscounted, total 28 (-1)
        - 152mm2S5 Giatsint-S, total 52 (+1)
        - 152mm 2S19 Msta-S, total 147 (-5)
        - 152mm 2S33 Msta-SM2, total 34 (-1)
        - 122mm BM-21 Grad, total 177 (+1)


- Errors in my code:
    - 3388-3400 UA rows missing name they are 13 9A310M1 TELAR. Total number of cases is correct.
    - 1V110 BM-21 Grad battery command vehicle, bad scrap
    - 2V15M fire control and observation vehicle, bad scrap
    - 1V16battalion fire direction vehicle, bad scrap
    - 19 122mm 2B17 Tornado-G labeled as 122mm 2B26 Grad-K
    - 220mm TOS-1A labeled as MT-LB with 140mm Ogon-18 MRLS
    - 14 9A310M1-2 TELAR (for Buk-M1-2) missing names around rows ~9017-9120
    - more un RU side


#### To Do
- Add dates to all entries. This information is not available in Oryx as is a blog post that is regulary updated, but some other people has capture some of this dates (see other related projects).
- Create Python module structure
- Clean code & Tests
- Create cron to update and to push to git
- Create code to look for differences on the daily update

## ToDo Project
- Dashboard (grafana? dash?)
- add lostarmor.info and bmpvsu.ru as datasources
- add platforms and system database
- addmap (see leedrake solution in R in other related projects)
- GIS add

## Datasources
- Oryx (https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html
        https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html )


## Other related projects to explore
- https://github.com/leedrake5/Russia-Ukraine
- https://github.com/scarnecchia/scrape_oryx

