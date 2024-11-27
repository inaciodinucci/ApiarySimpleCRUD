### Arquivo de texto dedicado ao professor da minha disciplina ou a quem quiser usar esse código. ###

Altere a senha da database nas seguintes classes

1 - .env > DB_PASSWORD:(senha do seu banco de dados)

2 - src>database>config.py> password=os.getenv('DB_PASSWORD', '(senha do seu banco de dados'),

====================================================

A criação de tabelas SQL está em src>database>schema.sql
