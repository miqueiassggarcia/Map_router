# Route Master (Sistema de Gerenciamento de Rotas para Empresas de Logística)

## Descrição

O Sistema de Gerenciamento de Rotas é uma aplicação web desenvolvida para empresas de logística que desejam otimizar a entrega de mercadorias. Ele permite o planejamento e a execução eficiente das rotas de entrega, levando em consideração diversos critérios, como urgência, peso, valor da carga e outros pontos relevantes.

## Funcionalidades Principais

- **Planejamento de Rotas:** O sistema permite o planejamento de rotas para entrega de mercadorias, levando em consideração múltiplos critérios de priorização.

- **Otimização de Entregas:** Utilizando algoritmos como Dijkstra aliado ao método greedy, o sistema determina a ordem mais eficiente para as entregas, minimizando custos e tempo de viagem.

- **Visualização de Rotas no Mapa:** A interface do usuário oferece a visualização das rotas planejadas em um mapa interativo, fornecido pela biblioteca Leaflet.

## Tecnologias Utilizadas

- **Frontend:** Desenvolvido com Next.js, um framework React para renderização de páginas web do lado do servidor.

- **Mapas:** A visualização das rotas é implementada com a biblioteca Leaflet, que fornece uma interface amigável e interativa para exibição de mapas.

- **Backend:** Uma API Flask em Python é responsável por gerenciar a lógica de negócios e fornecer os dados para o frontend. Esta API processa os dados da Overpass Turbo para obter informações sobre as rotas e as utiliza para calcular as melhores opções de entrega.

<!-- ## Licença

Este projeto é distribuído sob a licença [MIT](https://opensource.org/licenses/MIT). Consulte o arquivo LICENSE.md para obter mais detalhes. -->

## Uso de Dados

Este projeto utiliza dados da Overpass Turbo, uma fonte de dados licenciada sob a [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1.0/). A ODbL é uma licença de código aberto projetada para permitir o compartilhamento e uso livre de bancos de dados.

Os dados da Overpass Turbo são processados e aplicados nos algoritmos de planejamento de rotas para determinar a ordem de entrega mais eficiente.

## Licença

Os dados da Overpass Turbo utilizados neste projeto são licenciados sob a Open Database License (ODbL). Isso significa que:

- Você é livre para usar, modificar e distribuir os dados conforme desejar.
- Se você modificar os dados ou criar um trabalho derivado, deve compartilhá-lo sob os mesmos termos da ODbL.
- Você deve fornecer atribuição adequada à fonte original dos dados, indicando que os dados são provenientes da Overpass Turbo.
- Se aplicável, você deve notificar sobre quaisquer modificações feitas nos dados ao distribuir o trabalho derivado.

Por favor, revise a [licença completa da ODbL](https://opendatacommons.org/licenses/odbl/1.0/) para obter mais informações sobre seus termos e condições.

## Contribuições

Contribuições para este projeto são bem-vindas! Sinta-se à vontade para abrir problemas (issues) ou enviar solicitações de recebimento (pull requests) neste repositório.