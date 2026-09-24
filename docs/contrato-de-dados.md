# Contrato de dados — Estação Meteorológica

| **Versão** | 0.1 (rascunho para validação com a equipe de firmware) |
| **Data** | 2026-09-24 |
| **Disciplina** | Projeto e Desenvolvimento II — Ciência da Computação |
| **Backend** | Yan Victor |
| **Firmware** | *(preencher)* |

> Este documento é a fonte oficial do formato das mensagens entre a ESP32 e o servidor.
> Qualquer mudança de campo, tipo, unidade ou faixa deve alterar a versão e o
> histórico no final do arquivo, com commit no Git. Cópias soltas em conversa ficam desatualizadas.

---

## 1. Objetivo e escopo

Definir **o que** a ESP32 envia, **em que formato** e **com que regras**, e o que o servidor responde.
Vale para os dois meios de transporte (MQTT e HTTPS): o corpo da mensagem é o mesmo.

Sensores previstos no plano de ensino: DHT22 (temperatura e umidade), BMP280 (pressão),
MQ-135 (qualidade do ar), LDR (luminosidade) e pluviômetro (chuva).

---

## 2. Pontos em aberto (validar com a equipe)

| # | Pergunta | Proposta da v0.1 | Status |
|---|---|---|---|
| 1 | Quantas estações físicas serão? | 1 real + estações simuladas para testes | A confirmar |
| 2 | Transporte principal: MQTT ou HTTPS? | Suportar os dois; MQTT como principal se a rede permitir | A confirmar |
| 3 | Frequência de envio | 1 leitura a cada 60 s | A confirmar |
| 4 | O que fazer se a ESP32 não sincronizar a hora (NTP)? | Firmware tenta sincronizar de novo e não envia sem hora válida | A confirmar |
| 5 | Onde fica a calibração do MQ-135 e do LDR? | No backend (firmware envia valor bruto) | A confirmar |
| 6 | Quantos mm equivale cada basculada do pluviômetro? | Depende do modelo; firmware converte para mm | A confirmar |
| 7 | Onde o servidor vai rodar e qual a URL do endpoint? | A definir | A confirmar |
| 8 | Modelos exatos dos sensores e faixas do datasheet | Faixas da seção 4 são as típicas de cada sensor | A confirmar |

---

## 3. Convenções gerais

- Formato: **JSON**, codificação **UTF-8**.
- Nomes de campo em `snake_case`, em inglês. **A unidade fica no nome** do campo (`_c`, `_pct`, `_hpa`, `_mm`).
- Números com **ponto** como separador decimal e no máximo **2 casas decimais**.
- Horário sempre em **UTC**, no formato **ISO 8601** com sufixo `Z` (ex.: `2026-09-24T14:30:00Z`).
  A conversão para o horário de Brasília acontece só na exibição, no dashboard.
- **Falha de sensor é `null`.** Nunca usar `0`, `-1`, `999` ou `NaN` para representar falha.
  O JSON não aceita `NaN`, e um valor "de mentira" entraria nas médias como se fosse real.
- **Todas as chaves devem estar presentes** em toda mensagem. Sensor sem leitura vai como `null`.
- Pelo menos **um** campo de sensor deve ser diferente de `null`; senão a mensagem não tem utilidade.

---

## 4. Mensagem de leitura

### 4.1 Campos

| Campo | Tipo JSON | Unidade | Faixa válida | Anulável | Origem | Descrição |
|---|---|---|---|---|---|---|
| `station_id` | texto | — | 3 a 32 caracteres: minúsculas, números e hífen (ex.: `est-01`) | não | cadastro | Código único da estação |
| `measured_at` | texto (ISO 8601 UTC) | data e hora | qualquer instante válido, não muito no futuro | não | firmware (NTP) | Momento em que a leitura foi feita |
| `temperature_c` | número decimal | °C | de -40 a 80 | sim | DHT22 | Temperatura do ar |
| `humidity_pct` | número decimal | % | de 0 a 100 | sim | DHT22 | Umidade relativa do ar |
| `pressure_hpa` | número decimal | hPa | de 300 a 1100 | sim | BMP280 | Pressão atmosférica na altitude da estação |
| `air_quality_raw` | inteiro | ADC (sem unidade) | de 0 a 4095 | sim | MQ-135 | Valor bruto do conversor analógico (12 bits) |
| `luminosity_raw` | inteiro | ADC (sem unidade) | de 0 a 4095 | sim | LDR | Valor bruto do conversor analógico (12 bits) |
| `rain_mm` | número decimal | mm | maior ou igual a 0 | sim | pluviômetro | Chuva medida **no intervalo desde a leitura anterior** (não é o total do dia) |

Observações por campo:

- **`rain_mm`**: `0.0` significa "não choveu"; `null` significa "sensor falhou". Cada leitura carrega a
  sua própria chuva do intervalo, mesmo que o envio anterior tenha falhado e a leitura fique
  guardada para reenvio.
- **`air_quality_raw` e `luminosity_raw`**: valores brutos. A conversão para um índice de qualidade do ar
  e para luminosidade fica no backend, para poder recalibrar sem regravar o firmware.
  O MQ-135 **não** mede ppm real: o dashboard trata o resultado como índice relativo.
- **Faixas**: são os limites físicos típicos de cada sensor (datasheet). Um valor fora delas
  indica falha de leitura. Faixas de plausibilidade climática (ex.: 60 °C é possível
  para o sensor, mas suspeito para a região) são tratadas depois, no backend, como
  regra de qualidade, e não fazem parte deste contrato.

### 4.2 Exemplo completo

```json
{
  "station_id": "est-01",
  "measured_at": "2026-09-24T14:30:00Z",
  "temperature_c": 24.3,
  "humidity_pct": 61.2,
  "pressure_hpa": 1013.2,
  "air_quality_raw": 412,
  "luminosity_raw": 2300,
  "rain_mm": 0.0
}
```

### 4.3 Exemplo com falha de sensor (DHT22 sem resposta)

```json
{
  "station_id": "est-01",
  "measured_at": "2026-09-24T14:31:00Z",
  "temperature_c": null,
  "humidity_pct": null,
  "pressure_hpa": 1013.1,
  "air_quality_raw": 410,
  "luminosity_raw": 2312,
  "rain_mm": 0.0
}
```

---

## 5. Transporte

### 5.1 HTTPS

| | |
|---|---|
| Método e caminho | `POST /api/v1/readings` |
| Autenticação | Header `X-API-Key: <chave da estação>` (uma chave por estação) |
| Corpo | O JSON da seção 4 |
| Cabeçalho de conteúdo | `Content-Type: application/json` |

Resposta de sucesso (`201 Created`):

```json
{
  "status": "received",
  "is_valid": true,
  "flags": []
}
```

Se a leitura for salva mas reprovada nas regras de qualidade, a resposta continua sendo `201`,
com `is_valid: false` e a lista de `flags` explicando o motivo. Os nomes das flags
ficam em `docs/regras-de-validacao.md`.

### 5.2 MQTT

| | |
|---|---|
| Tópico | `estacao/{station_id}/leituras` |
| Payload | O JSON da seção 4 |
| QoS | 1 |
| Autenticação | Usuário e senha por estação |
| Porta | 1883 (desenvolvimento) e 8883 com TLS (produção) |

O backend confere se o `station_id` do tópico é igual ao do payload. Se forem diferentes, a mensagem é descartada e registrada em log.

Redes de faculdade costumam bloquear a porta 1883. Se isso acontecer, o transporte HTTPS (porta 443) é o plano B.

---

## 6. Respostas do servidor (HTTPS) e o que o firmware deve fazer

| Código | Significado | Ação do firmware |
|---|---|---|
| `201` | Recebida e salva (válida ou marcada como inválida) | Nada: é sucesso |
| `401` ou `403` | Chave da estação ausente ou inválida | Não reenviar; corrigir a configuração |
| `409` | Leitura já recebida (mesma estação e mesmo `measured_at`) | Não reenviar; tratar como sucesso |
| `422` | Formato inválido (campo faltando, tipo errado, data malformada, todos os sensores `null`) | Não reenviar; é erro de formato |
| `5xx` ou sem resposta | Falha do servidor ou da rede | Tentar de novo depois, guardando a leitura |

**Regra importante:** o servidor só devolve `422` para problemas de **formato**, porque uma mensagem
malformada não pode ser salva. Um valor **fora da faixa** (por exemplo, `temperature_c` de 200)
tem o formato correto: ele é **salvo** com `is_valid: false`, para preservar o dado bruto
e poder investigar a falha depois.

---

## 7. Campos adicionados pelo servidor

Estes campos **não** fazem parte da mensagem enviada pela estação.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | inteiro | Identificador interno da leitura |
| `received_at` | data e hora (UTC) | Momento em que o servidor recebeu a mensagem |
| `is_valid` | booleano | Resultado das regras de validação |
| `flags` | lista de textos | Motivos de reprovação ou aviso (vazia se estiver tudo certo) |

Unicidade: a combinação (`station_id`, `measured_at`) não pode se repetir. Isso evita duplicidade em reenvios.

---

## 8. Cadastro da estação (não vai em cada mensagem)

A estação é fixa, então os dados de localização ficam no cadastro (tabela `stations`), e não em cada leitura.

| Campo | Tipo | Faixa | Descrição |
|---|---|---|---|
| `code` | texto | igual ao `station_id` | Código único |
| `name` | texto | — | Nome de exibição |
| `latitude` | decimal | de -90 a 90 | Graus decimais (WGS 84) |
| `longitude` | decimal | de -180 a 180 | Graus decimais (WGS 84) |
| `altitude_m` | decimal | — | Altitude em metros (usada para corrigir a pressão ao nível do mar) |
| `installed_at` | data e hora | — | Data de instalação |
| `is_active` | booleano | — | Estação em operação |
| `api_key_hash` | texto | — | Resumo (hash) da chave; a chave em si nunca é guardada |

---

## 9. Mapeamento de tipos entre as camadas

| No contrato (JSON) | No backend (Python / Pydantic) | No banco (PostgreSQL) |
|---|---|---|
| texto | `str` | `text` |
| data e hora ISO 8601 UTC | `datetime` (com fuso) | `timestamptz` |
| número decimal | `float` | `double precision` |
| inteiro | `int` | `integer` |
| `null` | `None` | `NULL` |
| lista de textos (`flags`) | `list[str]` | `text[]` |
| booleano | `bool` | `boolean` |

---

## 10. Versionamento

- Mudança que **adiciona um campo opcional** é compatível: sobe a versão menor (0.1 → 0.2).
- Mudança que **remove, renomeia ou muda o tipo, a unidade ou a faixa** de um campo quebra a compatibilidade:
  sobe a versão maior (0.x → 1.0) e exige alinhamento com o firmware antes do merge.
- Todo alinhamento com a equipe de firmware é registrado no histórico abaixo.

### Histórico de mudanças

| Versão | Data | Mudança |
|---|---|---|
| 0.1 | 2026-09-24 | Versão inicial (rascunho) |