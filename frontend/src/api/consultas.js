const BASE_URL = '/api/consultas'

async function requisitar(url, opcoes) {
  let resposta
  try {
    resposta = await fetch(url, opcoes)
  } catch {
    throw new Error('Não foi possível conectar ao servidor.')
  }

  if (resposta.ok) {
    return resposta.json()
  }

  if (resposta.status === 429) {
    throw new Error('Muitas consultas seguidas. Aguarde um minuto.')
  }

  let mensagem = 'Erro inesperado. Tente novamente.'
  try {
    const corpo = await resposta.json()
    if (typeof corpo.detail === 'string') {
      mensagem = corpo.detail
    } else if (Array.isArray(corpo.detail) && corpo.detail[0]?.msg) {
      mensagem = corpo.detail[0].msg.replace('Value error, ', '')
    }
  } catch {
    // o corpo não era JSON, mantém a mensagem genérica
  }
  throw new Error(mensagem)
}

export function consultarCep(cep) {
  return requisitar(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cep }),
  })
}

export function listarHistorico(limite = 50) {
  return requisitar(`${BASE_URL}?limite=${limite}`)
}