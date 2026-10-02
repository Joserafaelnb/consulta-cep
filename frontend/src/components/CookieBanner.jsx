export default function CookieBanner({ onAceitar, onRecusar }) {
  return (
    <aside className="cookie-banner" role="region" aria-label="Aviso de cookies">
      <p>
        Usamos um cookie anônimo para guardar o histórico das suas buscas neste
        navegador. Ele não contém dados pessoais nem serve para login. Se você
        recusar, o site funciona normalmente, mas sem &quot;Minhas buscas&quot;.
      </p>
      <div className="cookie-acoes">
        <button type="button" className="secundario" onClick={onRecusar}>
          Recusar
        </button>
        <button type="button" onClick={onAceitar}>
          Aceitar
        </button>
      </div>
    </aside>
  )
}