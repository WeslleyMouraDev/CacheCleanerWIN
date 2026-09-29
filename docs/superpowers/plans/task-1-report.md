# Relatório de Execução - Task 1: Initialize Project and Launcher

- **Status:** DONE
- **Commits:**
  - `93ef845`: `feat: add launcher and requirements`

## Arquivos Criados / Modificados
1. `requirements.txt`:
   - Dependências especificadas: `rich>=13.0.0` e `pytest>=7.0.0`.
2. `iniciar.bat`:
   - Script em lote para Windows com suporte a UTF-8 (`chcp 65001 >nul`), manipulação estrita de quebras de linha Windows CRLF (`\r\n`), verificação/criação de virtual environment (`.venv`), instalação de dependências e execução da aplicação CLI.
   - Sem parênteses em blocos condicionais vulneráveis (utiliza rótulos e saltos com `goto`).
3. `src/__init__.py`:
   - Inicializador de módulo do pacote Python do projeto.

## Verificação
- Final de linha de `iniciar.bat` validado via script Python: 40 ocorrências de `\r\n` (100% CRLF, 0 LF órfãos).
- Arquivos adicionados e commitados com sucesso no Git: `feat: add launcher and requirements` (`93ef845`).
