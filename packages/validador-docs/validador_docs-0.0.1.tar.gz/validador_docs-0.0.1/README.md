# Validator Docs
A Python package to validate and format Brazilian CPF and CNPJ documents.

## Features
- **CPF Validation**: Check if a given CPF is valid by verifying its check digits.
- **CNPJ Validation**: Validate CNPJ numbers by calculating their check digits.
- **CPF and CNPJ Formatting**: Format CPF and CNPJ numbers to standard Brazilian formats.

## Installation
You can install the package via `pip`:
```bash
pip install validator_docs
```
## Usage
### Import the package
> from validator_docs import validar_doc, formatar_cpf, formatar_cnpj

### Validate CPF and CNPJ
To validate a CPF or CNPJ, simply pass the document number (either as a string or integer) to the `validar_doc` function. The function will raise an exception if the document is invalid.
```
# Validate CPF
cpf = "123.456.789-09"
try:
    valid_cpf = validar_doc(cpf)
    print(f"CPF {valid_cpf} is valid.")
except ValueError as e:
    print(e)

# Validate CNPJ
cnpj = "12.345.678/0001-95"
try:
    valid_cnpj = validar_doc(cnpj)
    print(f"CNPJ {valid_cnpj} is valid.")
except ValueError as e:
    print(e)

```
### Format CPF and CNPJ

You can format valid CPF and CNPJ numbers using the provided `formatar_cpf` and `formatar_cnpj` functions:
```
cpf = "12345678909"
formatted_cpf = formatar_cpf(cpf)
print(f"Formatted CPF: {formatted_cpf}")  # Output: 123.456.789-09

cnpj = "12345678000195"
formatted_cnpj = formatar_cnpj(cnpj)
print(f"Formatted CNPJ: {formatted_cnpj}")  # Output: 12.345.678/0001-95
```
### Full Example

Here's a full example of how to use `validator_docs` to validate and format both CPF and CNPJ numbers:

```
from validator_docs import validar_doc

cpf = "123.456.789-09"
cnpj = "12.345.678/0001-95"

# Validate CPF and CNPJ
try:
    valid_cpf = validar_doc(cpf, formatado=True)
    print(f"Valid CPF: {valid_cpf}")
    
    valid_cnpj = validar_doc(cnpj, formatado=True)
    print(f"Valid CNPJ: {valid_cnpj}")
    
except ValueError as e:
    print(e)
```
## Roadmap

-   Adding support for other document types.
-   Improving performance for batch document validations.
## License

This project is licensed under the MIT License - see the LICENSE file for details.