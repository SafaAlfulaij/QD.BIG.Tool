# QD.Unpacker (Python)

Python port of the [QD.Unpacker](../QD.Unpacker) C#/.NET tool for extracting BigFile archives from games developed by Quantic Dream.

No third-party dependencies — requires only Python 3.7+.

## Usage

```
python -m qdunpacker <IndexFile> <Directory>
```

- `IndexFile` - Source `.idx` file (e.g. `BigFile_PC.idx`)
- `Directory` - Destination directory

## Examples

```
python -m qdunpacker "E:\Games\BEYOND Two Souls\BigFile_PC.idx" D:\Unpacked
python -m qdunpacker "E:\Games\Detroit Become Human\BigFile_PC.idx" D:\Unpacked
python -m qdunpacker "E:\Games\HEAVY RAIN\Resources\BigFile_WIN.idx" D:\Unpacked
```

If a `.dbg` debug file (same name as the `.idx` file) is present next to the index file, resource file names will be resolved from it automatically.
