# spring-boot-scraper-demo
Very simple Spring Boot API for interacting with a database.

I have setup this API as a go between for a python web scraper which I refactored to use spring boot.

The process for this scraper will be to gather a list of possible images to download from a subreddit (Dungeons and Dragons maps in our case here) and then ask the API to see if they are already in our database. If yes then done and go to the next, if no then download the associated images and meta information and then add that to the database.
These are accomplished by making calls to the Spring Boot API via get methods for ID checks, and then Post method for placing information in the database.

[1](https://github.com/mikem5/spring-boot-scraper-demo/blob/main/screenshots/spring_boot.png)

[2](https://github.com/mikem5/spring-boot-scraper-demo/blob/main/screenshots/json_post_to_spring.png)

[3](https://github.com/mikem5/spring-boot-scraper-demo/blob/main/screenshots/test_in_db.png)

[4](https://github.com/mikem5/spring-boot-scraper-demo/blob/main/screenshots/python.png)
