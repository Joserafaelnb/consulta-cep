import { useEffect, useState } from 'react'
import { consultarCep, listarMinhas, revogarCookie } from './api/consultas'
import ConsultaForm from './components/ConsultaForm'
import ResultadoCard from './components/ResultadoCard'
import HistoricoGeral from './components/HistoricoGeral'
import MinhasBuscas from './components/MinhasBuscas'
import CookieBanner from './components/CookieBanner'
import { lerConsentimento, salvarConsentimento } from './utils/consentimento'

const MINHAS_VAZIO = { itens: [], total: 0, pagina: 1, tamanho: 5 }

export default function App() {
  const [resultado, setResultado] = useState(null)
  const [consentimento, setConsentimento] = useState(lerConsentimento())
  const [minhas, setMinhas] = useState(MINHAS_VAZIO)
  const [pagina, setPagina] = useState(1)
  const [versao, setVersao] = useState(0)
  const [erroMinhas, setErroMinhas] = useState('')


  // "versao" muda a cada nova consulta, forçando o recarregamento de "Minhas buscas"
  useEffect(() => {
    if (consentimento !== 'aceito') return
    let ativo = true
    listarMinhas(pagina)
      .then((dados) => {
        if (ativo) {
          setMinhas(dados)
          setErroMinhas('')
        }
      })
      .catch((e) => {
        if (ativo) setErroMinhas(e.message)
      })
    return () => {
      ativo = false
    }
  }, [pagina, consentimento, versao])

  async function aoConsultar(cep) {
    setResultado(null)
    const dados = await consultarCep(cep)
    setResultado(dados)
    setPagina(1)
    setVersao((v) => v + 1)
  }

  function escolher(valor) {
    salvarConsentimento(valor)
    setConsentimento(valor)
  }

  async function revogar() {
    await revogarCookie()
    escolher('recusado')
  }

  return (
    <main className="container">
      <h1>Consulta de CEP</h1>
      <ConsultaForm onConsultar={aoConsultar} />
      {resultado && <ResultadoCard resultado={resultado} />}
      <MinhasBuscas
        consentimento={consentimento}
        dados={minhas}
        erro={erroMinhas}
        pagina={pagina}
        onMudarPagina={setPagina}
      />
      <HistoricoGeral versao={versao} />
      {consentimento === 'aceito' && (
        <button type="button" className="link" onClick={revogar}>
          Revogar cookies
        </button>
      )}
      {consentimento === null && (
        <CookieBanner
          onAceitar={() => escolher('aceito')}
          onRecusar={() => escolher('recusado')}
        />
      )}
    </main>
  )
}