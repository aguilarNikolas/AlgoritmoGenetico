
# comando para criar a base de dados de produtos 
#create database produtos;

# comando para usar a base
#use produtos;

# comando para criar minha lista de produtos
create table produtos(
	idproduto int not null auto_increment,
    nome varchar(50) not null,
    espaco float not null,
    valor float not null,
    quantidade int not null,
    constraint pk_produtos_iddproduto primary key (idproduto)
);

# comando para chamar a tabela
select * from produtos

# inserir elementos na minha tabela de produtos
insert into produtos (nome, espaco, valor, quantidade) values ('Geladeira Dako', 0.751, 999.9, 1);
insert into produtos (nome, espaco, valor, quantidade) values ('Iphone 6', 0.0000899, 2199.12, 5);
insert into produtos (nome, espaco, valor, quantidade) values ('TV 55', 0.400, 4346.99, 2);
insert into produtos (nome, espaco, valor, quantidade) values ('TV 50', 0.290, 3999.90, 3);
insert into produtos (nome, espaco, valor, quantidade) values ('TV 42', 0.200, 2999.00, 4);
insert into produtos (nome, espaco, valor, quantidade) values ('Notebook Dell', 0.00350, 2499.90, 1);
insert into produtos (nome, espaco, valor, quantidade) values ("Ventilador Panasonic", 0.496, 199.90, 10);
insert into produtos (nome, espaco, valor, quantidade) values ("Microondas Electrolux", 0.0424, 308.66, 2);
insert into produtos (nome, espaco, valor, quantidade) values ("Microondas LG", 0.0544, 429.90, 5);
insert into produtos (nome, espaco, valor, quantidade) values ("Microondas Panasonic", 0.0319, 299.29, 3);
insert into produtos (nome, espaco, valor, quantidade) values ("Geladeira Brastemp", 0.635, 849.00, 2);
insert into produtos (nome, espaco, valor, quantidade) values ("Geladeira Consul", 0.870, 1199.89, 6);
insert into produtos (nome, espaco, valor, quantidade) values ("Notebook Lenovo", 0.498, 1999.90, 2);
insert into produtos (nome, espaco, valor, quantidade) values ("Notebook Asus", 0.527, 3999.00, 1);

# comando para limpar uma tabela inteira
#TRUNCATE produtos;

#para saber a quantidade de produtos dentor da base
#select sum(quantidade) from produtos
