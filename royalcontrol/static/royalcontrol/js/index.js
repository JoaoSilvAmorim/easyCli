function funcao1() {
    alert("Formulario enviado!");
};

function contaLinhasTabela(){
    var tabela = document.getElementById('tableAtendimentos');
    var linhas = tabela.getElementsByTagName('tr');
    alert('Número de atendimentos' + linhas.length + ' linhas');
};

function jsonp(url, timeout) {
    // Gera um nome aleatório para a função de callback
    const func = 'jsonp_' + Math.random().toString(36).substr(2, 5);

    return new Promise(function (resolve, reject) {
        // Cria um script
        let script = document.createElement('script');

        // Cria um timer para controlar o tempo limite
        let timer = setTimeout(() => {
            reject('Tempo limite atingido');
            document.body.removeChild(script);
        }, timeout);

        // Cria a função de callback
        window[func] = (json) => {
            clearTimeout(timer);
            resolve(json);
            document.body.removeChild(script);
            delete window[func];
        };

        // Adiciona o script na página para inicializar a solicitação
        script.src = url + '?callback=' + encodeURI(func);
        document.body.appendChild(script);
    });
}

function consultaCNPJ(cnpj) {
    // Limpa o CNPJ para conter somente numeros, removendo traços e pontos
    cnpj = cnpj.replace(/\D/g, '');

    // Consulta o CNPJ na ReceitaWS com 60 segundos de tempo limite
    return jsonp('https://www.receitaws.com.br/v1/cnpj/' + encodeURI(cnpj), 60000)
        .then((json) => {
            if (json['status'] === 'ERROR') {
                return Promise.reject(json['message']);
            } else {
                console.log(json)
                document.getElementById('cep').value = (json.cep)
                document.getElementById('rua').value = (json.logradouro);
                document.getElementById('bairro').value = (json.bairro);
                document.getElementById('cidade').value = (json.municipio);
                document.getElementById('uf').value = (json.uf);
                document.getElementById('nome').value = (json.nome);
                document.getElementById('email').value = (json.email);
                document.getElementById('nomeFantasia').value = (json.fantasia);
                return Promise.resolve(json);
            }
        });
}