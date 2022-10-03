# Zeeker Scrapers

A collection of scrapy/Python spiders for web scraping legal materials in Singapore.

## What's Available

| Description    | Project    | Spider                  | Status | Features                                                    | Related Website                                   |
|----------------|------------|-------------------------|--------|-------------------------------------------------------------|---------------------------------------------------|
| PDPC Decisions | pdpcSpider | PDPCCommissionDecisions | Works  | List of all decisions in JSON <br/> Downloads PDF Decisions | https://www.pdpc.gov.sg/All-Commissions-Decisions |

## Quickstart

So you want to get scraping ASAP?

Clone this repository.

````commandline
git clone https://github.com/houfu/zeekerscrapers.git
````

Install with a python virtual environment (I use [poetry](https://python-poetry.org/)).

```commandline
cd zeekercrapers

poetry install
```

Change the directory to a Project (e.g. pdpcSpider)

```commandline
cd pdpcSpider
```

Run a spider using the scrapy command line tool, specifying an output file if desirable.

```commandline
scrapy crawl PDPCCommissionDecisions -o output.csv
```

Watch what you have wrought.

(scrapy contains many settings you can use. If you plan to make full use of these spiders,
please [be responsible](https://docs.scrapy.org/en/latest/topics/autothrottle.html).)

## License

MIT License, Copyright 2022 Ang Hou Fu

## Testing

This project runs on `pytest`. 
You can run all the tests written for all scrapers by running the `pytest` command in the root directory.

## Contributing

You are welcome to contribute new Spiders or new features to existing spiders.
Please open an Issue in the repository and let's work something out!
