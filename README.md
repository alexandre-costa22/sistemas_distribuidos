# Sistema_De_Cantina
 
INTRODUÇÃO 

Sistemas Distribuídos podem ser definidos como um conjunto de componentes computacionais independentes, localizados em lugares diferentes e conectados entre si por uma rede, compartilhando dados, tarefas e recursos. Os sistemas distribuídos são fundamentais para a internet e outros sistemas conectados a ela, por exemplo redes sociais, bancos, jogos online. 

O tema que será abordado neste trabalho é referente a uma Cantina Monetizada, onde o cliente pode fazer o seu cadastro no sistema, inserir valores em sua carteira digital e assim conseguirá realizar os pedidos na plataforma que estará sincronizada com a cozinha, onde receberão todos pedidos por ordem de chegada. 

Essa aplicação visa auxiliar as cantinas de instituições de ensino e escolas, facilitando assim a comercialização de produtos por meio de um sistema pré-pago. De tal forma a otimizar o processo de venda, uma vez que os clientes realizam o pagamento mediante aquisição de créditos na plataforma. A integração de um sistema de créditos como este não apenas moderniza o ambiente das cantinas, mas também oferece vantagem na administração do negócio. 

 

PROBLEMA 

O projeto do sistema Cantina Monetizada soluciona diversos problemas que estes estabelecimentos encontram no seu dia a dia. Hoje esses locais trabalham de forma manual em seus processos e com isso perdem na organização e logística de suas atividades, pois sem um sistema e ou automatização não temos agilidade e controle. 

Sem o sistema monetizado as cantinas ao trabalharem com dinheiro em espécie podem ter problemas com o controle de suas finanças, aumentando o risco de segurança tanto para seus funcionários quanto para os clientes. O uso de dinheiro físico pode trazer uma experiência ruim para os clientes, tendo que manusear valores quebrados e assim gerar filas desnecessárias no momento de alto fluxo. 

O sistema utiliza método de autenticação com usuário e senha visando a segurança na sua utilização, o cliente realiza o cadastro e informa o valor a ser adicionado em sua carteira digital. 

 

SOLUÇÃO DA CANTINA MONETIZADA 

A solução para a Cantina Monetizada está em criar um sistema síncrono onde os usuários da ferramenta poderão agilizar e facilitar, seus pagamentos, pedidos, controle de estoque, oferecendo assim uma forma eficiente de aprimorar tanto a experiência de funcionários e seus clientes. 

No sistema desenvolvido temos o servidor que é responsável pelo cadastro de usuários, processar os pedidos realizados, adicionar saldo na carteira do usuário, realizar autenticação com usuário e senha. Já o client tem a função de validar o pedido versus o cliente que o solicitou, inserir os dados de cadastro do cliente, informar o saldo após o cadastro do usuário, selecionar o item do menu informado pelo sistema. 

A comunicação é realizada da seguinte forma: inicia-se o servidor, após iniciamos o client. Com o serviço iniciado podemos executar a primeira etapa que é o cadastro de cliente com usuário e senha mais o saldo inicial. A autenticação valida se o usuário e senha cadastrados inicialmente conferem, e neste caso o sistema avança para a etapa de realização de pedido ou de adição de créditos.  


 
CONSIDERAÇÕES FINAIS 

Foi realizado o sistema com o cadastro de cliente, inserção de valores na carteira do cliente, realização de pedidos. 

Dificuldades encontradas foram relacionadas com a conexão do servidor onde ao iniciar ele, estabelecemos a comunicação e após execução de alguma atividade esta sessão encerra, e assim não conseguimos avançar nas etapas de pedido + client autenticado.  

 