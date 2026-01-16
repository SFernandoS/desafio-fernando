## O que é o La Palma?

O La Palma é uma equipe multidisciplinar comprometida com a observabilidade dos produtos da empresa. Diferente de monitoramentos isolados, pontuais ou reativos, buscamos integrar e conectar diferentes áreas funcionais, proporcionando ferramentas escaláveis e reutilizáveis.

### Arquitetura Proposta

A arquitetura é composta por múltiplas aplicações backend acessadas por meio de um API Gateway, todas instrumentadas com OpenTelemetry e integradas a uma camada central de observabilidade.



### Visão Geral

O fluxo começa com o usuário acessando o sistema via Gateway, que encaminha as requisições para diferentes aplicações internas (apps).
Cada aplicação é responsável apenas por sua lógica de negócio e pela emissão de sinais de observabilidade, sem conhecimento direto dos backends de armazenamento.

![Arquitetura](img/diagrama-arquitetura.png?raw=true)

#### Aplicações (Apps)
 - Serviços independentes responsáveis pela lógica de negócio
 - Instrumentados com OpenTelemetry
 - Enviam traces, métricas e logs via protocolo OTLP
 - Não possuem dependência direta dos backends de observabilidade

#### OpenTelemetry Collector
 - Ponto central de ingestão dos sinais
 - Recebe dados via OTLP
 - Atua como camada de desacoplamento entre aplicações e backends
 - Distribui cada tipo de sinal para seu backend especializado

#### Backends de Observabilidade
 - Tempo: armazenamento e consulta de traces
 - Loki: armazenamento e consulta de logs
 - Mimir: armazenamento de métricas em larga escala

#### Grafana
 - Camada unificada de visualização
 - Consome dados diretamente de Tempo, Loki e Mimir
 - Permite correlação entre métricas, logs e traces a partir de uma única interface


### Monitoração de Infraestrutura

A monitoração de infraestrutura cobre todo o ambiente de execução, incluindo os componentes da stack de observabilidade.

```txt
                    ┌────────────────────────────────────────────────────┐
                    │                     Host / VM                      │
                    │                                                    │
                    │  ┌──────────────────┐   ┌────────────────────────┐ │
                    │  │  Node Exporter   │   │        cAdvisor        │ │
                    │  │                  │   │                        │ │
                    │  │ - CPU            │   │ - CPU por container    │ │
                    │  │ - Memória        │   │ - Memória container    │ │
                    │  │ - Disco          │   │ - I/O                  │ │
                    │  │ - Filesystem     │   │ - Limites              │ │
                    │  │ - Processos      │   │                        │ │
                    │  └─────────┬────────┘   └─────────┬──────────────┘ │
                    │            │                      │                │
                    └────────────┼──────────────────────┼────────────────┘
                                 │                      │
                                 ▼                      ▼
                         ┌──────────────────────────────────────────┐
                         │               Prometheus                 │
                         │                                          │
                         │ - Scrape Node Exporter                   │
                         │ - Scrape cAdvisor                        │
                         │ - Scrape OTel Collector                  │
                         │ - Scrape Loki                            │
                         │ - Scrape Tempo                           │
                         │ - Scrape Mimir                           │
                         └──────────────────┬───────────────────────┘
                                            │
                                            ▼
                                  ┌──────────────────┐
                                  │     Grafana      │
                                  │                  │
                                  │ - Infra Host     │
                                  │ - Infra Contêiner│
                                  │ - Infra Stack    │
                                  └──────────────────┘
```

#### Host / VM

A coleta é realizada via **Node Exporter**, cobrindo CPU, memória, disco, filesystems, processos e serviços `systemd`.

O objetivo é identificar gargalos de recursos e avaliar a capacidade do ambiente onde a aplicação e a stack de observabilidade estão executando.

---

#### Containers

A coleta é realizada via **cAdvisor**, permitindo acompanhar o consumo de CPU, memória, I/O e disco por container, além da relação entre limites configurados e uso real.

Essa camada inclui tanto os containers da aplicação quanto os containers da stack de observabilidade, possibilitando correlação direta entre consumo de recursos e serviços específicos.

---

#### Infraestrutura da Observabilidade

A stack de observabilidade é monitorada como **componente crítico**.
O **Prometheus** coleta métricas dos próprios serviços, incluindo Prometheus, OpenTelemetry Collector, Loki, Tempo e Mimir.

São observados aspectos como ingestão, erros, latência, uso de memória, cardinalidade e saúde dos pipelines, garantindo confiança no funcionamento da plataforma de observabilidade.

---

## Como subir o ambiente

O ambiente é composto por dois Docker Compose:
- um para as aplicações
- outro para a stack de observabilidade

### Subindo manualmente

```bash
cd observability
docker compose -f compose.apps.yml up -d --build
docker compose -f compose.observability.yml up -d
```
### Subindo via Makefile

```bash
make up        # sobe aplicações e observabilidade
make down      # derruba todo o ambiente
make rebuild   # recria tudo do zero
make logs      # acompanha logs das aplicações
```

### Interfaces e Acessos (UI)

Após subir o ambiente, as seguintes interfaces ficam disponíveis via `localhost`:

---

#### Aplicação (API Gateway)
- **API:** http://localhost:5000/roll
- **Swagger:** http://localhost:5000/docs

Ponto de entrada da aplicação.
A maioria dos endpoints **simula erros propositalmente** para gerar sinais de observabilidade.

---

#### Grafana
- **URL:** http://localhost:3000
- **Usuário/Senha:** `admin` / `admin`

Interface central para visualização de métricas, logs, traces e profiling.

---

#### Prometheus
- **URL:** http://localhost:9090

Usado para inspeção direta de métricas, scrapes e regras.

