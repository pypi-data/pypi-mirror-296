# LogAid

A log aid for you.

## Installation
```
pip install logaid
```

## Usage
```
import logaid as log

log.info("Info")
log.debug("Debug")
log.warning("Warning")
log.error("Error")
```
### or 
```
from logaid import log
log.init(level='DEBUG',save=True)

log.info('hello world',{'key':'value'})
```