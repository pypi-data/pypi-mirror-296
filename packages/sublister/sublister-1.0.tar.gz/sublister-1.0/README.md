# sublister


## Introduction
**[Sublist3r](https://github.com/aboul3la/Sublist3r)** is no longer actively maintained and hasn't received updates in several years. Many of its functionalities doesn't work anymore. As a replacement, **sublister** offers a fast and robust up-to-date tool for discovering subdomains passively.


![sublister](./images/sublister.png "the new sublister")


## Features

### Websites
- crt.sh
- ThreatCrowd.org
- DNSDumpster.com

### Apis
- Shodan
- VirusTotal
- C99  (TODO)

### Search Engine
- Google
- Bing
- Yahoo


## How to install

You can install **sublister** directly from pip with the following command:
> pip install sublister

Or you can install it directly from the repository:
> git clone https://github.com/42zen/sublister


## How to use

When installed you can **scan a domain** and **store the results** on a file with a simple command:
> sublister example.com -o subdomains.txt

You can also create a .env file with the following values to specify apis keys:
```
VIRUSTOTAL_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
SHODAN_API_KEY=YYYYYYYYYYYYYYYYYYYYYYYYYYYY
```

Or using the **python library**:
```
from sublister import SubLister
VIRUSTOTAL_API_KEY = 'XXXX'
SHODAN_API_KEY = 'YYYY'
subdomains = SubLister(vt_api_key=VIRUSTOTAL_API_KEY, shodan_api_key=SHODAN_API_KEY).get_subdomains("example.com")
for subdomain in subdomains:
    print(subdomain)
```


## Credits

- [Mathias Bochet](https://www.linkedin.com/in/mathias-bochet/) (aka [Zen](https://github.com/42zen/)) - Author
- [Ahmed Aboul-Ela](https://x.com/aboul3la) (aka [aboul3la](https://github.com/aboul3la/)) - Author of the original sublister tool