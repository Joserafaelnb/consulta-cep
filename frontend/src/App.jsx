import { useCallback, useEffect, useState } from 'react'
import { consultarCep, listarHistorico } from './api/consultas'
import ConsultaForm from './components/ConsultaForm'
import ResultadoCard from './components/ResultadoCard'
import HistoricoTabela from './components/HistoricoTabela'

export default function App() {
  const [resultado, setResultado] = useState(null)
  const [historico, setHistorico] = useState([])
  const [erroHistorico, setErroHistorico] = useState('')

  const carregarHistorico = useCallback(async () => {
    try {
      setHistorico(await listarHistorico())
      setErroHistorico('')
    } catch (e) {
      setErroHistorico(e.message)
    }
  }, [])

  useEffect(() => {
    carregarHistorico()
  }, [carregarHistorico])

  async function aoConsultar(cep) {
    setResultado(null)
    const dados = await consultarCep(cep)
    setResultado(dados)
    await carregarHistorico()
  }

  return (
    <main className="container">
      <h1>Consulta de CEP</h1>
      <ConsultaForm onConsultar={aoConsultar} />
      {resultado && <ResultadoCard resultado={resultado} />}
      <HistoricoTabela consultas={historico} erro={erroHistorico} />
    </main>
  )
}