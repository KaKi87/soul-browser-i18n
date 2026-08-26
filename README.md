
![screen_1024x500](https://user-images.githubusercontent.com/47548927/152998096-b4f225d6-ffbc-4cc3-b0b0-2eeab3d188f6.jpg)

<!-- BEGIN I18N -->

## Translation status

Translation coverage is calculated against the English base located at:

```text
Language/values/strings.xml
````

The English source currently contains **1063 translation keys**.

| Language           | Directory       | Translated | Missing | Completion                    |
| ------------------ | --------------- | ---------: | ------: | ----------------------------- |
| English (base)     | `values`        |       1063 |       0 | `████████████████████` 100.0% |
| বাংলা              | `values-bn`     |       1063 |       0 | `████████████████████` 100.0% |
| العربية            | `values-ar`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Čeština            | `values-cs`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Deutsch            | `values-de`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Español            | `values-es`     |       1037 |      26 | `███████████████████░` 97.6%  |
| فارسی              | `values-fa`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Français           | `values-fr`     |       1037 |      26 | `███████████████████░` 97.6%  |
| हिन्दी             | `values-hi`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Magyar             | `values-hu`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Bahasa Indonesia   | `values-in`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Italiano           | `values-it`     |       1037 |      26 | `███████████████████░` 97.6%  |
| 日本語                | `values-ja`     |       1037 |      26 | `███████████████████░` 97.6%  |
| 한국어                | `values-ko`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Polski             | `values-pl`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Português          | `values-pt`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Português (Brasil) | `values-pt-rBR` |       1037 |      26 | `███████████████████░` 97.6%  |
| Română             | `values-ro`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Русский            | `values-ru`     |       1037 |      26 | `███████████████████░` 97.6%  |
| ᱥᱟᱱᱛᱟᱲᱤ            | `values-sat`    |       1037 |      26 | `███████████████████░` 97.6%  |
| ไทย                | `values-th`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Türkçe             | `values-tr`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Українська         | `values-uk`     |       1037 |      26 | `███████████████████░` 97.6%  |
| Tiếng Việt         | `values-vi`     |       1037 |      26 | `███████████████████░` 97.6%  |
| 简体中文               | `values-zh-rCN` |       1037 |      26 | `███████████████████░` 97.6%  |
| 繁體中文               | `values-zh-rTW` |       1037 |      26 | `███████████████████░` 97.6%  |

### Check translation coverage

The repository includes a lightweight Python translation coverage checker under `scripts/`.

No external Python packages are required.

Check a specific language:

```bash
python3 scripts/test_covarage.py --bn
```

The language argument automatically maps to the corresponding Android resource directory:

```text
--bn       → Language/values-bn/strings.xml
--de       → Language/values-de/strings.xml
--fr       → Language/values-fr/strings.xml
--pt-rBR   → Language/values-pt-rBR/strings.xml
--zh-rCN   → Language/values-zh-rCN/strings.xml
```

List all available translations:

```bash
python3 scripts/test_covarage.py --list
```

Check every available translation:

```bash
python3 scripts/test_covarage.py --all
```

The checker reports:

* Total translation keys
* Translated keys
* Missing keys
* Empty translations
* Extra keys not present in the English base
* Translation completion percentage

Example:

```text
Total strings:          1063
Translated strings:     1063
Missing translations:   0
Empty translations:     0
Extra translations:     0
Translation completion: 100.00%

✅ All keys are translated. 100% complete.
```

### Updating the translation table

The status table above is generated automatically.

After adding or updating translations, regenerate it with:

```bash
python3 scripts/update_i18n_table.py
```

> The English `Language/values` resource is the source of truth. A translation is considered complete when every key from the English resource exists and contains a non-empty value.

<!-- END I18N -->
