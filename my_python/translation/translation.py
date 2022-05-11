from google.cloud import translate
import os

credential_path = "/credentials/speechtotextapi.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def translate_text(text, source_lang="en-US", target_lang="fr-FR", project_id="speechtotextapi-340414"):
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": source_lang,
            "target_language_code": target_lang,
        }
    )

    # Display the translation for each input text provided
    # Write transcription in a file
    fhand = open("transcript.txt", "w")
    for translation in response.translations:
        fhand.write("{}".format(translation.translated_text))
        print("Translated text: {}".format(translation.translated_text))
    time.sleep(0.5)
