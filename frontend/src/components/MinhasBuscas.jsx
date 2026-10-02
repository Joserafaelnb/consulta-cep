import HistoricoTabela from './HistoricoTabela'

export default function MinhasBuscas({
  consentimento,
  dados,
  erro,
  pagina,
  onMudarPagina,
}) {
  if (consentimento !== 'aceito') {
    return (
      <section className="card">
        <h2>Minhas buscas</h2>
        <p>
          Aceite os cookies para guardar o histórico das suas buscas neste
          navegador.
        </p>
      </section>
    )
  }

  const totalPaginas = Math.max(1, Math.ceil(dados.total / dados.tamanho))

  return (
    <>
      <HistoricoTabela titulo="Minhas buscas" consultas={dados.itens} erro={erro} />
      {dados.total > dados.tamanho && (
        <nav className="paginacao" aria-label="Paginação das minhas buscas">
          <button
            type="button"
            disabled={pagina <= 1}
            onClick={() => onMudarPagina(pagina - 1)}
          >
            Anterior
          </button>
          <span>
            Página {pagina} de {totalPaginas}
          </span>
          <button
            type="button"
            disabled={pagina >= totalPaginas}
            onClick={() => onMudarPagina(pagina + 1)}
          >
            Próxima
          </button>
        </nav>
      )}
    </>
  )
}