import polib
from deep_translator import GoogleTranslator
import concurrent.futures

def translate_entry(entry):
    if not entry.msgid.strip() or entry.msgstr.strip():
        return entry
    try:
        translator = GoogleTranslator(source='zh-CN', target='en')
        res = translator.translate(entry.msgid)
        entry.msgstr = res
    except Exception as e:
        print(f"Failed {entry.msgid[:10]}: {e}")
    return entry

def translate_po_file(file_path):
    print(f"Loading {file_path}")
    po = polib.pofile(file_path)
    
    untranslated = [e for e in po.untranslated_entries() if e.msgid.strip()]
    total = len(untranslated)
    print(f"Translating {total} entries concurrently...")
    
    if total == 0:
        return
        
    completed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(translate_entry, entry): entry for entry in untranslated}
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            if completed % 20 == 0:
                print(f"Completed {completed}/{total}")

    print("Saving PO file...")
    po.save(file_path)
    print("Translation complete!")

if __name__ == "__main__":
    translate_po_file("ego/locale/en/LC_MESSAGES/django.po")
