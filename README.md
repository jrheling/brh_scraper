Run following each market business day to scrape a few bits of price data 
that aren't easy to get historically, and write them to a three-week rolling 
window in a google sheet.

### Building

Note: this is pretty unsophisticated build process; among other things, it 
assumes everything is happening from trunk (master).

* Commit updates to repo
* Build tagged docker image:
```
docker build -t jrheling/brh_scraper:latest -t jrheling/brh_scraper:$(git rev-parse --short $(git ls-remote https://github.com/jrheling/brh_scraper.git | grep 'refs/heads/master' | cut -f 1)) https://github.com/jrheling/brh_scraper.git
```
* Push image to docker repo:
```
docker push jrheling/brh_scraper:latest
docker push jrheling/brh_scraper:$(git rev-parse --short $(git ls-remote https://github.com/jrheling/brh_scraper.git | grep 'refs/heads/master' | cut -f 1))
```
