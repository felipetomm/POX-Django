# POX-Django
This is my first project in GitHub.
It's about Policy Conflitct Detection in SDN with POX.

Projeto desenvolvido na disciplina de Conclusão de Curso, no curso de Ciências da Computação (URI - Frederico Westphalen).
Seu propósito inicial é detectar conflitos entre políticas (regras de rede) em Redes Definidas por Software (Software Defined Networking - SDN), onde até o presente momento, está realizando esta funcão de forma satisfatória. Além disso, este trabalho foi apontado como um grande diferencial do assunto, visto que nenhum trabalho até a sua data de publicação, propunha algo semelhante.
Como todo projeto, este também necessita de seus ajustes e melhorias, bem como adição de novas funcionalidades (ex: resolução dos conflitos).
O projeto utiliza os seguintes recursos:
> Python 2.7
> Django
> PostgreSQL
> Pox

O código responsável pela detecção dos conflitos fica por conta de um módulo externo ao pox. Este módulo é caracterizado como o módulo principal do projeto, denominado MDC (Módulo de Detecçao de Conflitos).

Componentes do Projeto:
> Módulo de Detecção de Conflitos (MDC);
> Módulo de Coleta (MC);
> Interface WEB com Django;
> Banco de Dados PostgreSQL;

Funcionalidades dos Componentes:
1º MDC: Realiza a análise de duas regras, apontando 0-n conflitos. Toda sua estrutura está no arquivo fonte scd_new_analisador_conflitos.py;
2º MC: Realiza a coleta das regras de todos os Switch (Comutadores) presentes no POX. Após a coleta, realiza a chamada para a função de análise de conflitos. Para finalizar, fica responsável por armazenar os resultados da análise no banco de dados, onde efetua, a toda execução, a limpeza da base e adiciona os novos resultados (os dados passam a ser somente temporários)1
3º Interface WEB: Apresenta, de forma simples, os resultados obtidos pela análise das regras.
4º Banco de Dados: Armazena os resultados da análise das regras.

Funcionamento:
1º Levantar o controlador POX sua estrutura de comutadores;
2º Inserir algumas regras de teste (exemplo no arquivo regras_tcc.sh);
3º Executar o Módulo de Coleta (scd_coletor.py);
4º Analisar os resultados.

OBS:
1º Houve ainda uma tentativa de paralelizar o processo do módulo de coleta. O mesmo pode ser encontrado no arquivo scd_coletor_thread.py;
2º Para mais informações sobre utilização, favor entrar em contato. Fico a disposição (e muito feliz) em ajudar no entendimento do projeto.
