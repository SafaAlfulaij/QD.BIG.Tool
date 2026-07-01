# QD.Unpacker (Python)

Python port of the [QD.Unpacker](../QD.Unpacker) C#/.NET tool for extracting and repacking BigFile archives from games developed by Quantic Dream.

No third-party dependencies — requires only Python 3.7+.

## Usage

```
python -m qdunpacker unpack <IndexFile> <Directory>
python -m qdunpacker pack <IndexFile> <SourceDirectory> <OutputDirectory>
```

- `IndexFile` - The game's `.idx` file (e.g. `BigFile_PC.idx`). For `pack`, this is used as a template for entry order/metadata; it is never modified.
- `Directory` - Destination directory for `unpack`.
- `SourceDirectory` - Directory containing (optionally modified) resources, laid out the same way `unpack` produces them.
- `OutputDirectory` - Destination directory for the repacked `.idx`/`.dat`/`.dNN` files.

If a `.dbg` debug file (same name as the `.idx` file) is present next to the index file, resource file names are resolved from it automatically for both modes.

## Examples

```
python -m qdunpacker unpack "E:\Games\BEYOND Two Souls\BigFile_PC.idx" D:\Unpacked
python -m qdunpacker unpack "E:\Games\Detroit Become Human\BigFile_PC.idx" D:\Unpacked
python -m qdunpacker pack "E:\Games\HEAVY RAIN\Resources\BigFile_WIN.idx" D:\Unpacked D:\Repacked
```

## Packing notes

- `pack` rebuilds `.dat`/`.dNN` archives from scratch: every entry's bytes are copied into a fresh archive, so `dwOffset` is always recalculated.
- For each entry, if a matching file exists under `SourceDirectory` (same relative path `unpack` writes), its current bytes are used — this is how you inject modified/replaced content. If the file isn't there, the original bytes are copied straight from the archive next to `IndexFile`, so you don't need to have extracted everything first.
- The real meaning/alignment of `dwPaddedSize` is undocumented (see the comments in the C# port), so the packer simply sets it equal to the new `dwSize` for every entry.
