import { useCallback, useEffect, useRef, useState } from 'react'
import { listarHistorico } from '../api/consultas'
import HistoricoTabela from './HistoricoTabela'

const TAMANHO = 10

export default function HistoricoGeral({ versao }) {
  const [itens, setItens] = useState([])
  const [temMais, setTemMais] = useState(true)
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState('')
  const sentinela = useRef(null)
  const emAndamento = useRef(false)
  const offset = useRef(0)

  const carregarMais = useCallback(async () => {
    if (emAndamento.current) return
    emAndamento.current = true
    setCarregando(true)
    try {
      const pagina = await listarHistorico(TAMANHO, offset.current)
      offset.current += pagina.length
      setItens((atual) => {
        const ids = new Set(atual.map((i) => i.id))
        return [...atual, ...pagina.filter((i) => !ids.has(i.id))]
      })
      setTemMais(pagina.length === TAMANHO)
      setErro('')
    } catch (e) {
      setErro(e.message)
      setTemMais(false)
    } finally {
      emAndamento.current = false
      setCarregando(false)
    }
  }, [])

  // recomeça do zero quando uma nova consulta é feita
  useEffect(() => {
    offset.current = 0
    setItens([])
    setTemMais(true)
  }, [versao])

  // observa a sentinela enquanto ainda houver itens para carregar
  useEffect(() => {
    const elemento = sentinela.current
    if (!elemento || !temMais) return
    const observador = new IntersectionObserver(
      ([entrada]) => {
        if (entrada.isIntersecting) carregarMais()
      },
      { rootMargin: '200px' },
    )
    observador.observe(elemento)
    return () => observador.disconnect()
  }, [temMais, itens.length, versao, carregarMais])

  return (
    <>
      <HistoricoTabela titulo="Buscas gerais" consultas={itens} erro={erro} />
      <div ref={sentinela} className="sentinela" aria-hidden="true" />
      {carregando && <p className="status">Carregando...</p>}
      {!temMais && !erro && itens.length > 0 && (
        <p className="status">Fim do histórico.</p>
      )}
      {erro && (
        <button type="button" className="link" onClick={() => setTemMais(true)}>
          Tentar novamente
        </button>
      )}
    </>
  )
}