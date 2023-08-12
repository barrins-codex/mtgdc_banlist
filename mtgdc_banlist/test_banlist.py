"""
Control of the banlists after 2023-07-31 banlist.
"""
from mtgdc_banlist.banlist_compiler import BanlistCompiler


banlist = BanlistCompiler()

commanders = ["Akiri, Line-Slinger", "Arahbo, Roar of the World", "Ardenn, Intrepid Archaeologist", "Asmoranomardicadaistinaculdacar", "Baral, Chief of Compliance", "Breya, Etherium Shaper", "Derevi, Empyrial Tactician", "Dihada, Binder of Wills", "Edgar Markov", "Edric, Spymaster of Trest", "Emry, Lurker of the Loch", "Esior, Wardwing Familiar", "Geist of Saint Traft", "Inalla, Archmage Ritualist", "Krark, the Thumbless", "Minsc & Boo, Timeless Heroes", "Najeela, the Blade-Blossom", "Oloro, Ageless Ascetic", "Omnath, Locus of Creation", "Prime Speaker Vannifar", "Rofellos, Llanowar Emissary", "Shorikai, Genesis Engine", "Tasigur, the Golden Fang", "Thrasios, Triton Hero", "Urza, Lord High Artificer", "Vial Smasher the Fierce", "Winota, Joiner of Forces", "Yuriko, the Tiger's Shadow", "Zurgo Bellstriker"]
missing_cz = []
for card in commanders:
    if not banlist.is_banned(card, command_zone=True):
        missing_cz.append(card)

assert len(missing_cz) == 0

cards = ["Ancestral Recall", "Ancient Tomb", "Back to Basics", "Bazaar of Baghdad", "Black Lotus", "Capture of Jingzhou", "Cavern of Souls", "Channel", "Chrome Mox", "Comet, Stellar Pup", "Deadly Rollick", "Deflecting Swat", "Dig Through Time", "Emrakul, the Aeons Torn", "Entomb", "Fastbond", "Field of the Dead", "Fierce Guardianship", "Flawless Maneuver", "Food Chain", "Gaea's Cradle", "Genesis Storm", "Gifts Ungiven", "Grim Monolith", "Hermit Druid", "Hogaak, Arisen Necropolis", "Humility", "Imperial Seal", "Jeweled Lotus", "Karakas", "Library of Alexandria", "Lion's Eye Diamond", "Lutri, The Spellchaser", "Loyal Retainers", "Maddening Hex", "Mana Crypt", "Mana Drain", "Mana Vault", "Mishra's Workshop", "Mox Amber", "Mox Diamond", "Mox Emerald", "Mox Jet", "Mox Opal", "Mox Pearl", "Mox Ruby", "Mox Sapphire", "Mystical Tutor", "Natural Order", "Necrotic Ooze", "Oath of Druids", "Polymorph", "Price of Progress", "Protean Hulk", "Ragavan, Nimble Pilferer", "Scapeshift", "Sensei's Divining Top", "Serra's Sanctum", "Sol Ring", "Strip Mine", "Temporal Manipulation", "Thassa's Oracle", "The One Ring", "The Tabernacle at Pendrell Vale", "Timetwister", "Time Vault", "Time Walk", "Time Warp", "Tinker", "Tolarian Academy", "Trazyn the Infinite", "Treasure Cruise", "Uro, Titan of Nature's Wrath", "Vampiric Tutor", "Wasteland"]
missing_md = []
for card in cards:
    if not banlist.is_banned(card):
        missing_md.append(card)

assert len(missing_md) == 0
