# jw_download

Command line tool to download publication on jw.org.


## Installation

From Pypi (recommanded)
```shell
$ pip install jw_download
```

From github
```shell
$ git clone https://github.com/Unviray/jw_download.git
$ cd jw_download/
$ pip install -r requirements.txt
```


## Usage

```shell
$ jw --help
Usage: jw [OPTIONS] [DEST]

  JW book downloader

Options:
  --date TEXT        [default: 202001]
  --pub TEXT         Publication codename  [default: w]
  --fileformat TEXT  Comma separated file format  [default: JWPUB]
  --lang TEXT        [default: E]
  --help             Show this message and exit.

```


### ```--date```

Publication date in format ```{year}{month}```.  
Ex: for **March 2020** -> ```202003```


### ```--pub```

Publication code name.  
Supported code:
- ```w``` Watchtower
- ```g``` Awake


### ```--fileformat```

Comma separated file format.  
Ex: for **JWPUB** and **EPUB** -> ```JWPUB,EPUB```  
Supported file format:
- PDF
- EPUB
- JWPUB
- RTF
- TXT
- BRL
- BES
- DAISY

Some language doesn't include all file format.


### ```--lang```

Language code.  
Ex:
- ```E``` -> English
- ```FR``` -> French
- ```MG``` -> Malagasy


### ```DEST```

Destination directory.
```.``` for current directory.
