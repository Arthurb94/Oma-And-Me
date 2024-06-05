import json


def lambda_handler(event, context):
    # Log pour débogage
    body = json.loads(event["body"])
    # Vérifier si le fichier est présent dans l'événement
    if "file" not in body.keys():

        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(event),
            # "body": json.dumps({"error": f"No file provided {entry}"}),
        }

    file = body["file"]

    # Appeler la fonction segmentate et traiter l'image
    try:
        scale, _ = segmentate(file)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(event),
        }
    except Exception as e:
        # Gérer les exceptions et log pour débogage
        print(f"Error during processing: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error", "details": str(e)}),
        }

    # Réponse par défaut (ceci ne devrait pas être atteint)
    return {
        "statusCode": 200,
        "body": json.dumps({"blob": "blobn"}),
    }


# Exemple de la fonction segmentate (désactivée pour l'instant)
def segmentate(file):
    # Fonction segmentate désactivée pour ce débogage
    return 1, None


# Exemple de la fonction predict (désactivée pour l'instant)
def predict(image):
    # Fonction predict désactivée pour ce débogage
    return [1]
