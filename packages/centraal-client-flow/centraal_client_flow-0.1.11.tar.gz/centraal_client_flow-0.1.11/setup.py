# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['centraal_client_flow',
 'centraal_client_flow.connections',
 'centraal_client_flow.events',
 'centraal_client_flow.helpers',
 'centraal_client_flow.models',
 'centraal_client_flow.rules',
 'centraal_client_flow.rules.integration',
 'tests',
 'tests.connections',
 'tests.helpers',
 'tests.integration',
 'tests.models',
 'tests.rules',
 'tests.rules.integration']

package_data = \
{'': ['*']}

install_requires = \
['azure-cosmos>=4.7.0,<5.0.0',
 'azure-functions==1.20.0',
 'azure-servicebus==7.12.2',
 'pydantic>=2.8.0,<3.0.0']

extras_require = \
{'dev': ['black>=22.3.0,<23.0.0',
         'isort==5.10.1',
         'flake8==4.0.1',
         'flake8-docstrings>=1.6.0,<2.0.0',
         'tox>=3.24.5,<4.0.0',
         'twine>=3.8.0,<4.0.0',
         'pre-commit>=2.17.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'mypy>=1.5.1,<2.0.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=8.1.11,<9.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-autorefs>=0.3.1,<0.4.0',
         'mike>=1.1.2,<2.0.0',
         'setuptools>=68.0,<69.0',
         'pkginfo>=1.9,<2.0',
         'virtualenv>=20.0,<21.0'],
 'test': ['pytest>=8.0.1,<9.0.0', 'pytest-cov>=3.0.0,<4.0.0']}

setup_kwargs = {
    'name': 'centraal-client-flow',
    'version': '0.1.11',
    'description': 'Proyecto que facilita el flujo de información de cliente.',
    'long_description': '# centraal-client-flow\n\n<a href="https://pypi.python.org/pypi/centraal_client_flow">\n    <img src="https://img.shields.io/pypi/v/centraal_client_flow.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/centraal-api/centraal-client-flow/actions">\n    <img src="https://github.com/centraal-api/centraal-client-flow/actions/workflows/dev.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://centraal-api.github.io/centraal-client-flow/">\n    <img src="https://img.shields.io/website/https/centraal-api.github.io/centraal-client-flow/index.html.svg?label=docs&down_message=unavailable&up_message=available" alt="Documentation Status">\n</a>\n\n\n`centraal-client-flow` es una librería de Python diseñada para facilitar la implementación de una una solución basada en eventos para la sincronización y consistencia de datos entre sistemas distribuidos de clientes utilizando Azure. Esta librería proporciona herramientas para manejar eventos, aplicar reglas de procesamiento, integrar con sistemas externos y mantener un esquema unificado de clientes.\n\n## **Introducción**\n\n`Centraal-Cliente-Flow` facilita la implementación de arquitecturas de sincronización de datos en Azure, proporcionando una base sólida para manejar eventos en tiempo real, reglas de negocio, integración con APIs externas y mantenimiento de un log de auditoría.\n\n## **Arquitectura**\n\nLa arquitectura está diseñada para unificar la información de los clientes alrededor de un identificador único, asegurando la consistencia de los datos a través de los siguientes componentes clave:\n\n- **Eventos**: Gestionados por Azure Functions para manejar eventos entrantes en tiempo real y operaciones periódicas de extracción de datos.\n- **Reglas**: Implementan la lógica de procesamiento de eventos para actualizar un esquema unificado de clientes.\n- **Reglas de Integración**: Sincronizan las actualizaciones del esquema unificado con sistemas externos a través de APIs REST.\n- **Esquema Unificado**: Modelo de datos centralizado que asegura consistencia y escalabilidad en la información de los clientes.\n- **Log de Auditoría**: Registra todas las actualizaciones del esquema unificado para asegurar trazabilidad.\n- **Uso de Pydantic**: La libreria hace uso extensivo e incentiva que cada intercambio de datos este mediado por modelos [Pydantic](https://docs.pydantic.dev/latest/), ya de esta manera se asegura calidad y reglas de negocio.\n\n```\n                Evento\n                  ^\n                  |\n                  v\n+------------------------------+\n|   Receiver/Timer Function     |\n|  (Valida y envía a la cola    |\n|   usando Pydantic)            |\n+------------------------------+\n            |\n            |\n         [P]-EventoBase(IdModel)\n            |\n            v\n+------------------------------+\n|   Azure Service Bus Queue     |\n|  (Ordena eventos por          |\n|   Session ID)                 |\n+------------------------------+\n            |\n            v\n+---------------------------------------+\n|  Processor Function                   |\n|  Reglas de Actualización              |\n|  (Actualiza esquema y log de          |\n|   auditoría usando Pydantic,          |\n|   Publica actualizaciones)            |\n+---------------------------------------+\n            |                   |\n            |                   |\n         [P]-EntradaEsquemaUnificado\n    [P] - AuditoriaEntry        |\n            |                   |\n            v                   v\n+-----------------------+   +-------------------------+\n|     Cosmos DB         |   |  Azure Service Bus      |\n| (Esquema Unificado y  |   |         Topic           |\n|  Log de Auditoría)    |   |                         |\n+-----------------------+   +-------------------------+\n            |                           |\n            |                           |\n      [P]-AuditoriaEntry                |\n            |                           |\n            v                           v\n+-----------------------+   +-------------------------+\n| Log de Auditoría en   |   | Integration Function    |\n| Cosmos DB             |   | Reglas  y Estrategias   |\n| (Registra cambios)    |   | de Integración          |\n+-----------------------+   |                         |\n                            |                         |\n                            +-------------------------+\n                                       |\n                                 [P]-BaseModel\n                                       |\n                                       v\n                            +-------------------------+\n                            |    Sistemas Externos    |\n                            | (Reciben actualizaciones|\n                            |  a través de APIs REST) |\n                            +-------------------------+\n\n```\n\n## **Componentes Clave**\n\n### 1. **Eventos**\n\n- **Receiver Functions**: Manejan eventos entrantes en tiempo real. Implementadas en el módulo `receiver.py` utilizando clases como `EventFunctionBuilder`.\n- **Timer Functions**: Ejecutan tareas periódicas para extraer información de sistemas externos, definidas en `timer.py` usando `TimerFunctionBuilder`.\n\n### 2. **Reglas de Procesamiento**\n\nLas reglas para actualizar el esquema unificado de clientes se implementan usando `UpdateProcessor` y `RuleProcessor`, que permiten procesar y aplicar reglas específicas a los eventos entrantes.\n\n### 3. **Reglas de Integración**\n\nSe implementan en `strategy.py` usando la clase `RESTIntegration`, que permite la sincronización de datos con APIs REST externas.\n\n### 4. **Esquema Unificado**\n\nDefinido en `schemas.py`, utiliza modelos Pydantic para asegurar la validación y consistencia de datos. Los modelos incluyen `IDModel`, `EntradaEsquemaUnificado`, y otros sub-esquemas específicos.\n\n### 5. **Log de Auditoría**\n\nPara asegurar la trazabilidad de las actualizaciones, todos los cambios en los sub-esquemas se registran en una colección de auditoría en Cosmos DB.\n\n## **Uso de la Librería**\n\n### 1. **Configuración Inicial**\n\nAsegúrate de tener configuradas las variables de entorno necesarias para las conexiones a Cosmos DB y Azure Service Bus.\n\n```python\nimport os\n\nos.environ["COSMOS_CONN"] = "<tu_cosmos_db_connection_string>"\nos.environ["DATABASE"] = "<tu_database_name>"\nos.environ["BUS_CONN"] = "<tu_service_bus_connection_string>"\n```\n\n### 2. **Registrar Funciones de Azure**\n\n#### Eventos\n\nUtiliza el siguiente ejemplo para registrar funciones receptoras y de temporización.\n\n```python\nfrom azure.functions import FunctionApp\nfrom centraal_client_flow.receiver import Recieve\nfrom centraal_client_flow.timer import Pull\n\napp = FunctionApp()\n\n# Registrar función receptora\nreceiver = Recieve(event_source="source_name", queue_name="queue_name", service_bus_client=service_bus_client_instance)\nreceiver.register_function(app, processor=event_processor_instance, event_model=event_model_instance)\n\n# Registrar función de temporización\npull = Pull(schedule="0 */5 * * * *", event_source="source_name", queue_name="queue_name", service_bus_client=service_bus_client_instance)\npull.register_function(app, processor=pull_processor_instance)\n```\n\n#### Reglas de Actualización\n\n```python\nfrom azure.functions import FunctionApp\nfrom update_rules import bp_update_rules\n\napp = FunctionApp()\napp.register_functions(bp_update_rules)\n```\n\n#### Reglas de Integración\n\n```python\nfrom azure.functions import FunctionApp\nfrom integration_rules import bp_int_rules\n\napp = FunctionApp()\napp.register_functions(bp_int_rules)\n```\n\n### 3. **Definir Modelos y Procesadores**\n\nDefine los modelos de datos utilizando Pydantic para asegurar la validación de datos entrantes.\n\n```python\nfrom pydantic import BaseModel, EmailStr\n\nclass EventoEjemplo(BaseModel):\n    id: int\n    nombre: str\n    email: EmailStr\n```\n\nImplementa procesadores para manejar la lógica de actualización de acuerdo con las reglas de negocio.\n\n```python\nfrom centraal_client_flow.rules.update import UpdateProcessor\nfrom modelos import EventoEjemplo\n\nclass EjemploProcessor(UpdateProcessor):\n    def process_message(self, event: EventoEjemplo, current_registro=None):\n        # Lógica de procesamiento de eventos\n        pass\n```\n\n### 4. **Ejecutar la Aplicación**\n\nAsegúrate de que todas las dependencias estén instaladas y ejecuta la aplicación utilizando un servidor de funciones de Azure.\n\n```bash\nfunc start\n```\n\n## **Contribuciones**\n\nLas [contribuciones](./CONTRIBUTING.md) son bienvenidas. Por favor, abre un issue o un pull request en el repositorio para discutir cualquier cambio.\n\n* Free software: Apache-2.0\n* Documentation: <https://centraal-api.github.io/centraal_client_flow/>\n\n\n## Credits\n\nThis package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool. For more information, please visit the [project page](https://zillionare.github.io/python-project-wizard/).\n\n\n',
    'author': 'German',
    'author_email': 'equipo@centraal.studio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/centraal-api/centraal_client_flow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
