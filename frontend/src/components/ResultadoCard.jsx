import { formatarData } from '../utils/formatarData'

export default function ResultadoCard({ resultado }) {
  return (
    <section className="card" aria-live="polite">
      <h2>Resultado</h2>
      <dl>
        <dt>CEP</dt>
        <dd>{resultado.cep}</dd>
        <dt>Logradouro</dt>
        <dd>{resultado.logradouro || '—'}</dd>
        <dt>Bairro</dt>
        <dd>{resultado.bairro || '—'}</dd>
        <dt>Cidade</dt>
        <dd>{resultado.cidade}</dd>
        <dt>Consultado em</dt>
        <dd>{formatarData(resultado.dataConsulta)}</dd>
      </dl>
    </section>
  )
}