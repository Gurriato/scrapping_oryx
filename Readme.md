# Russian invasion of Ukraine Dashboard
Still WIP but working

Why I built this scrapper? because others had a lot of inconsistencies. Even with errors this is most accurate Oryx scrapper you are going to find.
Why others are not as accurate? because Oryx blog is manually feed. Therefore, there are a lot of exceptions you had to code in order to capture all the data.

Commits are welcome

#### Be aware
There are some equipment not been capture by the scrapper due coding errors on Oryx webpage
- Coding errors in Oryx page
    - 2 Ucranian tanks (2 M-55S)
        - Coding error in Oryx webpage
    - 29 unkown Russian Equipment. Impact on the df: (probably most of them are because they are )
        - 11 220mm TOS-1A appearing as MT-LB with 140mm Ogon-18 MRLS
        - UAZ PAtriot jeep labeled as LUAZ-969
        - Unkown error 8 UAZ-23632 (not scraped) and 8 UAZ-23632-148-64 not labeled correctly
            - Still missing 10 elements 😓
- Data errors in Oryx page:
    - UA:
        - 1 UAZ-3151: (23, destroyed) -> should be  1 UAZ-3151: (1, destroyed) On Russian equipment
        - BMP-1(P) proof 64 destroyed is missingm therefore, total number 348 (+1) (@31/10/2023)
        - BMP-2(K) is miscounted. Total number == 181 (-1) (@31/10/2023)
        - Unknown BMP-1/2 is miscounted. Total number == 27 (-1) (@31/10/2023)
        - BTR-70 proof 1 is missing, therefore total number = 28 (-1) (@31/10/2023)
        - AT105A Saxon is miscounted, total number = 13 (-1) (@31/10/2023)
        - 155mm M777A2 howitzer is miscounted, total number = 70 (+1) (@31/10/2023)
        - 122mm BM-21 Grad is missing proof 16, teherfore total number 37 (-1)
        - 5P85D/S (launcher for S-300PS) 13 and 14 are repeated? (@31/10/2023)
        - A1-SM Fury case 35 = 32 and miscounted. Total number = 55 (-1) (@31/10/2023)
        - KrAZ-255B miscounted total number 16(-1) (@31/10/2023)
        - GAZ-66 Format on first case, also miscounted total 107(-1) (@31/10/2023)
        - MAZ-537 miscounted, total 3 (+1) (@31/10/2023)
        - VEPR is duplicated, one under Armoured Fighting Vehicles the other  under Mine-Resistant Ambush Protected (MRAP)
    - RU:
        - Pending...

- Errors in my code:
    - 3388-3400 UA rows missing name they are 13 9A310M1 TELAR. Total number of cases is correct.



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
- Classes clasification (https://github.com/leedrake5/Russia-Ukraine/blob/main/data/classes.csv)


## Other related projects to explore
- https://github.com/leedrake5/Russia-Ukraine
- https://github.com/scarnecchia/scrape_oryx