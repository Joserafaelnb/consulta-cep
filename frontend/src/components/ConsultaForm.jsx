import { useState } from 'react'

export default function ConsultaForm({ onConsultar }) {
  const [cep, setCep] = useState('')
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState('')

  async function aoEnviar(evento) {
    evento.preventDefault()
    setErro('')
    setCarregando(true)
    try {
      await onConsultar(cep)
      setCep('')   // só limpa se a consulta deu certo
    } catch (e) {
      setErro(e.message)
    } finally {
      setCarregando(false)
    }
  }

  return (
    <form onSubmit={aoEnviar} className="form">
      <label htmlFor="cep">CEP</label>
      <div className="linha">
        <input
          id="cep"
          value={cep}
          onChange={(e) => setCep(e.target.value)}
          placeholder="01001-000"
          maxLength={9}
          inputMode="numeric"
          autoComplete="off"
          required
        />
        <button type="submit" disabled={carregando}>
          {carregando ? 'Consultando...' : 'Consultar'}
        </button>
      </div>
      {erro && (
        <p role="alert" className="erro">
          {erro}
        </p>
      )}
    </form>
  )
}