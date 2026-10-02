import { formatarData } from '../utils/formatarData'

export default function HistoricoTabela({ titulo, consultas, erro }) {
  return (
    <section className="card">
      <h2>{titulo}</h2>
      {erro && (
        <p role="alert" className="erro">
          {erro}
        </p>
      )}
      {consultas.length === 0 && !erro ? (
        <p>Nenhuma consulta realizada ainda.</p>
      ) : (
        <div className="tabela-scroll">
          <table>
            <thead>
              <tr>
                <th>CEP</th>
                <th>Logradouro</th>
                <th>Bairro</th>
                <th>Cidade</th>
                <th>Data/Hora</th>
              </tr>
            </thead>
            <tbody>
              {consultas.map((c) => (
                <tr key={c.id}>
                  <td>{c.cep}</td>
                  <td>{c.logradouro}</td>
                  <td>{c.bairro}</td>
                  <td>{c.cidade}</td>
                  <td>{formatarData(c.dataConsulta)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}