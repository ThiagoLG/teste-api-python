import logging

import azure.functions as func
import pandas as pd
import base64


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    doc = ''

    try:
        req_body = req.get_json()
        doc = req_body.get('b64')
    except ValueError:
        return func.HttpResponse(
            f'Não foi possível processar o documento evniado.\n{ValueError}',
            status_code=400
        )

    if doc:
        try:
            file = base64.b64decode(doc)
            file_content = pd.read_excel(file)
            formatted = file_content.to_json(orient='records')
        except ValueError:
            return func.HttpResponse(
                f'Não foi possível processar o documento evniado.\n{ValueError}',
                status_code=400
            )

        return func.HttpResponse(
            formatted,
            status_code=200
        )
    else:
        return func.HttpResponse(
            f'<p>Serviço utilizado para conversão de arqiuvos excel para json.</p>' +
            '<p>Para utilizar, realize uma requisição post enviando o seguinte body: </p>' +
            '<p>{ b64: conteúdo do arquivo em formato base64 }</p>',
            status_code=200
        )
