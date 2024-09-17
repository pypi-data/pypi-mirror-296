# Tinydb Helper
A Tinydb crud wrapper that make crud operations a breeze

## Installation
You can install the package using pip:

```bash
pip install tinydb-helper
```

## Usage
This package will install Tinydb

```python
from tinydb_helper.helper import Table
from tinydb import TinyDB, Query
import time

def main() -> None:
    db = TinyDB("db.json")
    timestamp = str(int(time.time()))

    # Exemple creating project table with custom primary key using default primary key generator 
    project = Table(db=db, table="project", primary_key="proj_id")
     
    # Example creating person table with custom primary key generator
    person = Table(db=db, table="person", key_gen=lambda: timestamp)

    # Example inserting a few record in person and project tables
    for i in range(4):
        project.insert(dict(name=f"test-{i}", year=f"{2004 + i}"), id=str(i + 1))
        person.insert(dict(first=f"first-{i}", year=f"{2004 + i}", id=str(i + 1)))

    # Exemple get all object from table person
    person.all()

    # Exemple find person object matching primary key field equal to "0"
    person.find(id="0")

    # Exemple filter person table base on Tinydb Query conditions
    person.filter(Query()['first'] == 'first-0')

    # Exemple update person object matching primary key field equal to "0" 
    person.update(id="0", item=dict(test='pass'))

     # Exemple delete person object matching primary key field equal to "0"
    person.delete(id="0")

if __name__ == "__main__":
    main()
```