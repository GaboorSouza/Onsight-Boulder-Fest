# Onsight Boulder Fest 🧗‍♂️

Aplicativo para gerenciamento de um campeonato de escalada, com funcionalidades para o cadastro de participantes, registro de pontuação em boulders e exibição do ranking público. Desenvolvido em Python usando Streamlit para a interface e armazenamento local em SQLite.

## Funcionalidades

- **Cadastro de Participantes**: Adiciona participantes com nome, categoria e sexo. Participantes também podem ser removidos da lista.
- **Cadastro de Boulders**: Cadastra boulders com nome e pontuação base específica. Cada boulder pode ser removido individualmente.
- **Lançamento de Pontuação**: Registra a pontuação de cada participante em diferentes boulders, com as seguintes opções de pontuação:
  - **Flash**: Pontuação completa.
  - **Cadena**: Pontuação do boulder - 200 pontos.
  - **Insucesso**: Zero pontos, sem restrição de lançamentos.
  
  **Regras de Lançamento**:
  - **Flash**: Permitido apenas uma vez para cada boulder. Não pode ser lançado se o participante já tiver pontuação no boulder.
  - **Cadena**: Permitido apenas uma vez para cada boulder. Permitido caso o participante tenha somente lançamentos de "Insucesso" para o boulder.
  - **Insucesso**: Sem restrições, mas não pode ser lançado se o participante tiver "Flash" ou "Cadena" no mesmo boulder.
  
- **Ranking Público**: Exibe o ranking dos participantes de acordo com a pontuação acumulada, considerando apenas as 10 maiores pontuações de cada participante. A lista é atualizada automaticamente a cada 10 segundos e oferece filtros por categoria e sexo.

## Tecnologias Utilizadas

- **Python**
- **Streamlit**: Framework para a criação de interfaces web.
- **SQLite**: Banco de dados local.
- **streamlit-autorefresh**: Biblioteca para atualização automática do ranking.

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/GaboorSouza/kmonRepository
   cd kmon-de-escalada

Instale as dependências necessárias:

bash
Copiar código
pip install -r requirements.txt

Execute o aplicativo:

bash
Copiar código
streamlit run app.py

Uso

Cadastro de Participantes
Acesse a aba Cadastro de Participantes.
Insira o Nome, Categoria e Sexo do participante.
Clique em Adicionar Participante para salvar.
A lista de participantes permite visualizar e remover qualquer participante cadastrado.
Cadastro de Boulder
Acesse a aba Cadastro de Boulder.
Insira o Nome do Boulder e a Pontuação Base.
Clique em Adicionar Boulder para salvar.
A lista exibe os boulders com a opção de removê-los individualmente.
Lançamento de Pontuação
Acesse a aba Lançamento de Pontuação.
Selecione um participante e um boulder.
Escolha o tipo de pontuação: Flash (pontuação completa), Cadena (pontuação completa - 200) ou Insucesso (0 pontos).
Clique em Lançar Pontuação para registrar.
Ranking Público
Acesse a aba Ranking Público para visualizar o ranking dos participantes.
A lista é atualizada automaticamente a cada 10 segundos e exibe as 10 maiores pontuações de cada participante.
Utilize os filtros por Categoria e Sexo para ajustar a visualização do ranking.

Observação: Este aplicativo foi desenvolvido para armazenamento local, utilizando SQLite, o que facilita testes e protótipos. Em produção, considere uma configuração de banco de dados persistente.

Esse `README.md` inclui informações sobre as regras específicas para o lançamento de pontuações, a atualização do ranking com as 10 melhores pontuações e detalhes de instalação e uso. Com isso, ele está completo e pronto para orientar usuários e desenvolvedores no uso do projeto!