# VerseTools

A package for getting Bible verses in different languages given references in English

### Prerequisites

```
Python version >= 3.6
```

### Installing
```
pip install -i https://test.pypi.org/simple/ verseTools-CrudeRags
```
### Usage
```
from verse_tools import GetVerses 
retriever = GetVerses.GetVerses('English')
my_verse = retriever.get("John 3:16")
print(my_verse)

my_list_of_references = ["Gen 1:1","Exo 1:1", "Lev 1:1", "Num 1:1"]
my_verses = retriever.get(my_list_of_references)
print(my_verses)
```
## Authors

* **Crude Rags** - *Initial work* - [CrudeRags](https://github.com/https://github.com/CrudeRags)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GNU GPL v3 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Stackoverflow.com - for many insights and code snippets
