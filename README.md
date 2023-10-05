# cine-database :robot::card_file_box:

**Purpose:** To create a database to contain most of Indian/Regional movie details<br />
**Functionality:** The code to scrap data from wikipedia and add/store to database i.e. to the movie_database.csv present in the current repository<br />

<img src="https://www.cloudifyapps.com/assets/images/icons/web-scraping-main-icon.png" width="200" height="200">

**Execution steps/guidelines:**
1. Run main.py
2. It would ask for personality's name. Enter the desired name
3. Application may ask for wikipedia url contain the filmography information if its not able to scrap the right one from search engine results
4. Post processing the results will get updated to movie_database.csv

**Features:**
1. It will search for results in search engines: google, yahoo and bing
2. If most relevant results are not retrieved, user can feed the right url
3. Script will extrat only the movie info table in wikipedia and skips irrelevant data
4. If multiple tables present, it will merge the right tables and skips the rest
5. It appends the Actor details if the movie info already present in the database

**Database:**
| Column      | Description                 |
| :----:      |:---                         |
| Year        | Release year of the movie   |
| Film        | Film Name                   |
| Language    | Language of the film        |
| Director    | Director of the film        |
| Writer      | Writer of the film          |
| Cast        | Cast acted in the film      |
| Producer    | Producer of the film        |
* Each row is an unique movie entry
