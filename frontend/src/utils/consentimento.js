const CHAVE = 'consentimento_cookies'

export function lerConsentimento() {
  try {
    return localStorage.getItem(CHAVE)
  } catch {
    return null
  }
}

export function salvarConsentimento(valor) {
  try {
    localStorage.setItem(CHAVE, valor)
  } catch {
    // armazenamento bloqueado pelo navegador: segue sem salvar
  }
}