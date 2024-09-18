import json
from pathlib import Path

EXCEL = Path(__file__).parent

with Path.open(EXCEL / "RelicMainAffixConfig.json", encoding="utf8") as f:
    RelicMainAffix = json.load(f)

with Path.open(EXCEL / "RelicSubAffixConfig.json", encoding="utf8") as f:
    RelicSubAffix = json.load(f)

with Path.open(EXCEL / "AvatarPromotionConfig.json", encoding="utf8") as f:
    AvatarPromotion = json.load(f)

with Path.open(EXCEL / "EquipmentPromotionConfig.json", encoding="utf8") as f:
    EquipmentPromotion = json.load(f)

with Path.open(EXCEL / "light_cone_ranks.json", encoding="utf8") as f:
    light_cone_ranks = json.load(f)
