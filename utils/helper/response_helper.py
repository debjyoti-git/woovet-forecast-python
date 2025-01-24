# utils/response_helper.py
def generate_response(status_code, body, allowed_methods='GET'):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': allowed_methods
        },
        'body': body
    }
