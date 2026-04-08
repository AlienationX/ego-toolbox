import polib
from deep_translator import GoogleTranslator
import time

def translate_po_file_batch(file_path):
    print(f"Loading {file_path}")
    po = polib.pofile(file_path)
    translator = GoogleTranslator(source='zh-CN', target='en')
    
    untranslated = po.untranslated_entries()
    total = len(untranslated)
    print(f"Found {total} untranslated entries.")
    
    if total == 0:
        return
        
    # Filter non-empty
    valid_entries = [e for e in untranslated if e.msgid.strip()]
    print(f"Valid to translate: {len(valid_entries)}")
    
    msgids = [e.msgid for e in valid_entries]
    
    # Process in chunks of 20
    chunk_size = 20
    for i in range(0, len(valid_entries), chunk_size):
        chunk = valid_entries[i:i+chunk_size]
        chunk_msgids = [e.msgid for e in chunk]
        print(f"Translating batch {i} to {i+len(chunk)}...")
        
        try:
            results = translator.translate_batch(chunk_msgids)
            for j, translated_text in enumerate(results):
                chunk[j].msgstr = translated_text
        except Exception as e:
            print(f"Error on batch: {e}")
            # fallback
            for entry in chunk:
                try:
                    entry.msgstr = translator.translate(entry.msgid)
                except Exception as ex:
                    print(f"Error translating '{entry.msgid}': {ex}")
            
    print("Saving PO file...")
    po.save(file_path)
    print("Translation complete!")

if __name__ == "__main__":
    translate_po_file_batch("ego/locale/en/LC_MESSAGES/django.po")
