#!/bin/bash

#Carregas as configuracoes
if [ -f "config.sh" ]; then
    . config.sh 
else
    echo 'Arquivo de configuração "config.sh" não encontrado.'
exit

fi

#Grava o numero total de linhas da listagem atual
nl=$(wc -l titles-tab-utf-8.csv | cut -d' ' -f1)
echo $nl > nl.txt

cd $dir_trab

source $dir_trab/$path_venv/bin/activate

#Elimina arquivo error-log.txt
if [ -f "error-log.txt" ] ; then 
    rm error-log.txt
    touch error-log.txt
fi

#Versao 1
python journal-tab-v1.py | grep "Error" > error-log.txt
wait

#Versao 2
python journal-tab-v2.py | grep Erro >> error-log.txt
wait

#Versao 3
python journal-tab-v3.py | grep Erro >> error-log.txt
wait

#Permissao de leitura
chmod 644 titles-tab-utf-8.csv
chmod 644 markup_journals.csv
chmod 644 titles-tab-v2-utf-8.csv
chmod 644 markup_journals_v2.csv
chmod 644 titles-tab-v3-utf-8.csv
chmod 644 markup_journals_v3.csv

deactivate

#Verifica o tamanho do arquivo e copia para servidor
if [ "$(cat titles-tab-utf-8.csv | wc -l)" -ge "$nl" ] && [ "$(cat error-log.txt | wc -l)" -lt 1 ]
then
    echo "Arquivo maior ou igual ao anterior. Enviando para Orfeu..."
    #copia versao 1
    scp titles-tab-utf-8.csv $server:$path
    scp markup_journals.csv $server:$path
    #copia versao 2
    scp titles-tab-v2-utf-8.csv $server:$path
    scp markup_journals_v2.csv $server:$path
    #copia versao 3
    scp titles-tab-v3-utf-8.csv $server:$path
    scp markup_journals_v3.csv $server:$path
else 
    echo "Foram detectados erros e enviados por e-mail para: "$emails
    cat >mensagem.txt<<!
A equipe TI,

Foram detectados erros durante a tentativa de produzir listagem de periódicos "titles-tab-utf-8.csv" gerado para static-sps.
Provavelmente foram produzidos dados insuficientes; o arquivo pode esta menor em seu tamanho ou problemas de conexao.
Abaixo o nome dos scripts e seus erros:

!

cat error-log.txt >> mensagem.txt

cat >>mensagem.txt<<!

Por favor, verificar/corrigir o(s) script(s) e efetuar o reprocessamento.

Source: https://github.com/scieloorg

Processamento SciELO

!

mailx -s "Falha ao tentar gerar o arquivo titles-tab-utf-8.csv - $(date '+%d/%m/%Y') - SPS" $emails < mensagem.txt
rm mensagem.txt

fi

exit