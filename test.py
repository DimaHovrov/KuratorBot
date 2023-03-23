import json

text = 'sd'
title_text = {"title": text}
title_text["json"] = []
title_text["json"].append(12)
title_text["json"].append(22)
print(json.dumps(title_text))
