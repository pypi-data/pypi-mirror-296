# secbulkdownload
Tool for bulk download filing archives and individual filing documents. It can do much more. check https://github.com/dlouton/sectoolkit 
as 'secbulkdownload' is based on it. The major changes are 1. it saves individual filings as LZMA compressed files (.xz) instead of .txt and 2. The parser is removed.

### Installation

The package can be installed via pip using the following statement:

`pip install secbulkdownload`

### Working with SEC index files

See the guide on https://github.com/dlouton/sectoolkit


### Appreciation Note
99.9% of this code is from https://github.com/dlouton/sectoolkit. A big thanks to dlouton. 
Other than saving in LMZA format this packaged also fixes the error showining up due to the newer versions of `tqdm` need different import statements.

### Changes in versions
version=0.0.2 removes `tqdm` as it was giving a lot of headcahes with dependencies for other packages that needed it too





