# WO2Net Delpher Tools

Tools for extracting and processing Delpher data for WO2Net. 

## Installation

```bash
pip install wo2net_delpher_tools
```

```bash
uv add wo2net_delpher_tools
```

## Usage
The example below extracts pica productions numbers (PPN) from a txt file and creates a json file for every number containing the metadata for the related issues.

```python
import wo2net_delpher_tools

ppn_numbers = wo2net_delpher_tools.load_ppn_numbers_from_txt('pnn_numbers.txt')

for number in ppn_numbers:
   wo2net_delpher_tools.process_ppn_to_json(number, f"{number}.json")
```

The example below does the same for a single PPN.

``python
from wo2net_delpher_tools import process_ppn_to_json

def main():
      process_ppn_to_json(271632224, '271632224.json')

if __name__ == "__main__":
      main()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://github.com/Stichting-WO2Net/wo2net-delpher-tools/blob/main/LICENSE)