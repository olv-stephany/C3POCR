# C3POCR

Biblioteca Python para analisar imagens, reconhecer textos e transformar informações visuais em JSON estruturado.

> Projeto open source em planejamento. O objetivo final é publicar o pacote no PyPI.

## Objetivo

```python
from c3pocr import extract

resultado = extract("documento.png")
```

Saída esperada:

```json
{
  "fields": {
    "valor_total": 89.90,
    "data": "19/03"
  },
  "confidence": 0.94
}
```

## Como o C3POCR deve funcionar

OCR puro retorna texto. O C3POCR também deve identificar a estrutura do documento, por exemplo:

```text
Valor Total .................... 89,90
Dia ............................ 19/03
```

O algoritmo usará posição das palavras, agrupamento por linhas, separadores visuais, expressões regulares, formatos conhecidos e confiança do OCR.

## Arquitetura

```text
Imagem
  ↓
Pré-processamento
  ↓
OCR
  ↓
Palavras com posição e confiança
  ↓
Agrupamento de linhas e blocos
  ↓
Detecção de padrões
  ↓
Normalização dos valores
  ↓
JSON validado
```

## Tecnologias

- **Pillow**: abrir, converter, redimensionar, cortar e melhorar imagens.
- **Tesseract + pytesseract**: primeira implementação de OCR.
- **OpenCV**: pré-processamento avançado no futuro.
- **Pydantic**: validação do JSON de saída.
- **PaddleOCR**: alternativa futura para documentos mais complexos.
- **pytest**: testes automatizados.

## Roadmap

### Fase 1 — MVP

- [ ] Criar estrutura do pacote `c3pocr`.
- [ ] Integrar Pillow.
- [ ] Integrar Tesseract.
- [ ] Retornar texto bruto, confiança e coordenadas.

### Fase 2 — Processamento de imagem

- [ ] Escala de cinza.
- [ ] Redimensionamento.
- [ ] Ajuste de contraste.
- [ ] Remoção de ruído.
- [ ] Correção de rotação.

### Fase 3 — Detecção de padrões

- [ ] Agrupar palavras na mesma linha.
- [ ] Detectar rótulos e valores.
- [ ] Identificar pontos e linhas como separadores.
- [ ] Relacionar campos pela posição horizontal.
- [ ] Usar regex para moeda, data, CPF e e-mail.

### Fase 4 — JSON

- [ ] Normalizar `89,90` para `89.90`.
- [ ] Normalizar datas.
- [ ] Validar campos com Pydantic.
- [ ] Incluir confiança por campo.
- [ ] Criar erros para dados incompletos.

### Fase 5 — Testes

- [ ] Criar imagens de teste.
- [ ] Testar imagens com baixa qualidade.
- [ ] Testar campos ausentes.
- [ ] Testar diferentes separadores.
- [ ] Criar testes de regressão.

### Fase 6 — PyPI

- [ ] Criar `pyproject.toml`.
- [ ] Definir versão `0.1.0`.
- [ ] Criar documentação de instalação.
- [ ] Publicar primeiro no TestPyPI.
- [ ] Testar instalação em ambiente limpo.
- [ ] Publicar no PyPI.
- [ ] Criar release e tag no GitHub.

## API planejada

```python
from c3pocr import extract

resultado = extract("documento.png", document_type="generic")
```

Retorno possível:

```python
{
    "text": "Valor Total .................... 89,90",
    "fields": {
        "valor_total": {
            "value": 89.90,
            "raw_value": "89,90",
            "confidence": 0.97
        }
    },
    "metadata": {
        "engine": "tesseract",
        "language": "por"
    }
}
```

## Princípios

- Separar OCR de interpretação dos campos.
- Priorizar resultados previsíveis e testáveis.
- Não depender de IA generativa no MVP.
- Permitir regras específicas por tipo de documento.
- Não enviar imagens para serviços externos por padrão.
- Manter uma API simples.

## Estrutura planejada

```text
C3POCR/
├── c3pocr/
│   ├── __init__.py
│   ├── extractor.py
│   ├── ocr.py
│   ├── preprocess.py
│   ├── patterns.py
│   ├── parsers.py
│   └── schemas.py
├── tests/
├── examples/
├── pyproject.toml
├── README.md
└── LICENSE
```

## Status

Em planejamento.

## Licença

A licença ainda será definida. MIT é uma opção simples para uma biblioteca open source.
