"""Omnitrix Alien DNA database and profile definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class AlienProfile:
    """Represents an Omnitrix Alien DNA profile for the watch face."""

    id: int
    codename: str
    name: str
    species: str
    homeworld: str
    primary_ability: str
    signature_color: str
    dna_code: str
    ascii_art: str
    description: str


DEFAULT_ALIEN_ROSTER: List[AlienProfile] = [
    AlienProfile(
        id=1,
        codename="ALIEN-01",
        name="Heatblast",
        species="Pyronite",
        homeworld="Pyros",
        primary_ability="Pyrokinesis & Heat Generation",
        signature_color="#ff5500",
        dna_code="PYRO-7720-DNA",
        ascii_art=(
            "   .---.   \n"
            "  /  🔥 \\  \n"
            " | (o o) | \n"
            "  \\  ~  /  \n"
            "   `---'   "
        ),
        description="Plasma-based lifeform capable of projecting intense fiery blasts.",
    ),
    AlienProfile(
        id=2,
        codename="ALIEN-02",
        name="Diamondhead",
        species="Petrosapien",
        homeworld="Petropia",
        primary_ability="Crystalline Construct & Invulnerability",
        signature_color="#00ffff",
        dna_code="PETRO-8841-DNA",
        ascii_art=(
            "   /\\     \n"
            "  /  \\    \n"
            " / 💎 \\   \n"
            " \\    /   \n"
            "  \\  /    \n"
            "   \\/     "
        ),
        description="Organic crystal entity able to manipulate crystalline shards and reflect lasers.",
    ),
    AlienProfile(
        id=3,
        codename="ALIEN-03",
        name="XLR8",
        species="Kineceleran",
        homeworld="Kinet",
        primary_ability="Hypersonic Speed & Reflexes",
        signature_color="#00aaff",
        dna_code="KINE-9923-DNA",
        ascii_art=(
            "   />>     \n"
            "  // ⚡    \n"
            " //==\\    \n"
            " \\\\==/    \n"
            "  \\>>     "
        ),
        description="Friction-manipulating speedster reaching speeds exceeding 300 mph in seconds.",
    ),
    AlienProfile(
        id=4,
        codename="ALIEN-04",
        name="Four Arms",
        species="Tetramand",
        homeworld="Khoros",
        primary_ability="Superhuman Strength & Sonic Shockwaves",
        signature_color="#ff1133",
        dna_code="TETRA-4412-DNA",
        ascii_art=(
            " \\  ||  / \n"
            "  \\(oo)/  \n"
            "  / == \\  \n"
            " /  ||  \\ "
        ),
        description="Four-armed brawn powerhouse possessing unmatched sheer physical force.",
    ),
    AlienProfile(
        id=5,
        codename="ALIEN-05",
        name="Grey Matter",
        species="Galvan",
        homeworld="Galvan Prime",
        primary_ability="Super-Genius Intellect & Micro-Engineering",
        signature_color="#00ff66",
        dna_code="GALVAN-0001-DNA",
        ascii_art=(
            "   (o.o)   \n"
            "   / | \\   \n"
            "    | |    "
        ),
        description="Mastermind creator species of the Omnitrix; possesses unparalleled intellect.",
    ),
    AlienProfile(
        id=6,
        codename="ALIEN-06",
        name="Upgrade",
        species="Galvanic Mechamorph",
        homeworld="Galvan B",
        primary_ability="Technological Merging & Enhancement",
        signature_color="#00ff88",
        dna_code="MECHA-1010-DNA",
        ascii_art=(
            "  [0101]   \n"
            "  ( O O )  \n"
            "  / === \\  \n"
            "  ~~~~~~~  "
        ),
        description="Living nanotech entity that assimilates and hyper-upgrades any technology.",
    ),
    AlienProfile(
        id=7,
        codename="ALIEN-07",
        name="Ripjaws",
        species="Piscciss Volann",
        homeworld="Piscciss",
        primary_ability="Aquatic Agility & Steel-Crushing Jaws",
        signature_color="#00e5ff",
        dna_code="PISC-3390-DNA",
        ascii_art=(
            "  <><><>   \n"
            " ( \\VV/ )  \n"
            "  \\ II /   \n"
            "   `--'    "
        ),
        description="Deep-sea predator capable of diving through extreme oceanic pressures.",
    ),
    AlienProfile(
        id=8,
        codename="ALIEN-08",
        name="Ghostfreak",
        species="Ectonurite",
        homeworld="Anur Phaetos",
        primary_ability="Intangibility, Invisibility & Telekinesis",
        signature_color="#9966ff",
        dna_code="ECTO-0066-DNA",
        ascii_art=(
            "   .~~~~.  \n"
            "  ( (o)  ) \n"
            "   \\    /  \n"
            "    ~~~~   "
        ),
        description="Shadowy phantom lifeform with the ability to drift through solid matter.",
    ),
    AlienProfile(
        id=9,
        codename="ALIEN-09",
        name="Stinkfly",
        species="Lepidopterran",
        homeworld="Lepidopterra",
        primary_ability="360° Flight & Viscous Slime Projection",
        signature_color="#aacc00",
        dna_code="LEPID-5519-DNA",
        ascii_art=(
            "  \\ / \\ /  \n"
            "   (o-o)   \n"
            "  /{___}\\  \n"
            "  /     \\  "
        ),
        description="Agile aerial insectoid equipped with 4 eye-stalks and flammable toxin streams.",
    ),
    AlienProfile(
        id=10,
        codename="ALIEN-10",
        name="Cannonbolt",
        species="Arburian Pelarota",
        homeworld="Arburia",
        primary_ability="Armored Sphere Roll & Ricochet Defense",
        signature_color="#ffcc00",
        dna_code="ARBUR-7731-DNA",
        ascii_art=(
            "   .----.  \n"
            "  / (::) \\ \n"
            " | (====) |\n"
            "  \\      / \n"
            "   `----'  "
        ),
        description="Armored juggernaut that curls into an impervious rolling kinetic sphere.",
    ),
]

EXTENDED_ALIEN_ROSTER: List[AlienProfile] = [
    AlienProfile(
        id=11,
        codename="ALIEN-11",
        name="Wildmutt",
        species="Vulpimancer",
        homeworld="Vulpin",
        primary_ability="Thermographic & Ultrasonic Senses",
        signature_color="#ff8800",
        dna_code="VULP-1120-DNA",
        ascii_art=(
            "   /\\__ /\\   \n"
            "  (  o.o  )  \n"
            "   > ^ <     \n"
            "  /       \\  "
        ),
        description="Feral apex predator utilizing quill projection and thermographic perception.",
    ),
    AlienProfile(
        id=12,
        codename="ALIEN-12",
        name="Swampfire",
        species="Methanosian",
        homeworld="Methanos",
        primary_ability="Methane Pyrokinesis & Chlorokinesis",
        signature_color="#00dd55",
        dna_code="METH-3342-DNA",
        ascii_art=(
            "   (✿_✿)   \n"
            "  /{ 🔥 }\\ \n"
            "  / |🌿| \\ \n"
            "    |  |   "
        ),
        description="Living plant/methane hybrid capable of generating ignited gas blasts and plant control.",
    ),
    AlienProfile(
        id=13,
        codename="ALIEN-13",
        name="Humungousaur",
        species="Vaxasaurian",
        homeworld="Terradino",
        primary_ability="Dynamic Size Alteration & Titan Strength",
        signature_color="#cc7722",
        dna_code="VAXA-9910-DNA",
        ascii_art=(
            "  /🦖🦖\\   \n"
            " ( ◣_◢ )  \n"
            " /======\\  \n"
            "/ |    | \\ "
        ),
        description="Colossal dinosaurian titan capable of growing up to 60 feet in height with seismic power.",
    ),
    AlienProfile(
        id=14,
        codename="ALIEN-14",
        name="Big Chill",
        species="Necrofriggian",
        homeworld="Kylmyys",
        primary_ability="Absolute-Zero Cryokinesis & Cryo-Phasing",
        signature_color="#00bbff",
        dna_code="NECRO-5501-DNA",
        ascii_art=(
            "  /\\    /\\ \n"
            " (  ❄️  ❄️ ) \n"
            "  \\ |  | / \n"
            "   \\/  \\/  "
        ),
        description="Ghostly moth lifeform able to freeze solid objects by phasing through them at absolute zero.",
    ),
    AlienProfile(
        id=15,
        codename="ALIEN-15",
        name="Echo Echo",
        species="Sonorosian",
        homeworld="Sonorosia",
        primary_ability="Ultrasonic Soundwaves & Self-Replication",
        signature_color="#e0e0e0",
        dna_code="SONO-7711-DNA",
        ascii_art=(
            "  [🔊 🔊]  \n"
            "  (  ••  ) \n"
            "  /  ||  \\ \n"
            "  \\ (||) / "
        ),
        description="Living sound amplifier entity inside a silicon containment suit that duplicates indefinitely.",
    ),
    AlienProfile(
        id=16,
        codename="ALIEN-16",
        name="Chromastone",
        species="Crystalsapien",
        homeworld="Petropia",
        primary_ability="Energy Absorption & Ultraviolet Laser Beams",
        signature_color="#dd44ff",
        dna_code="CRYST-8822-DNA",
        ascii_art=(
            "    /\\     \n"
            "   / ✨\\   \n"
            "  | [oo] | \n"
            "   \\ -- /  \n"
            "    `--'   "
        ),
        description="Silicon-crystal conductor that absorbs electromagnetic radiation and channels ultraviolet blasts.",
    ),
    AlienProfile(
        id=17,
        codename="ALIEN-17",
        name="Way Big",
        species="To'kustar",
        homeworld="Cosmic Storms",
        primary_ability="Cosmic Energy Beams & Skyscraper Might",
        signature_color="#ff3344",
        dna_code="TOKU-0099-DNA",
        ascii_art=(
            "     |     \n"
            "   (•_•)   \n"
            "  /==|==\\  \n"
            " /   |   \\ "
        ),
        description="Monumental cosmic colossus born in interstellar storms, towering hundreds of feet high.",
    ),
    AlienProfile(
        id=18,
        codename="ALIEN-18",
        name="Alien X",
        species="Celestialsapien",
        homeworld="Forge of Creation",
        primary_ability="Omnipotent Reality Warping & Spacetime Control",
        signature_color="#8899bb",
        dna_code="CELEST-0000-DNA",
        ascii_art=(
            "   /\\||/\\  \n"
            "  ( ★  ★ ) \n"
            "  /  ✨  \\ \n"
            "   `----'  "
        ),
        description="All-powerful cosmic being of the Forge of Creation capable of warping reality at will.",
    ),
]


ALIEN_QUOTES: dict[int, str] = {
    1: "Let's turn up the heat!",
    2: "Time to crystallize this situation!",
    3: "Can't catch what you can't see!",
    4: "Four arms are better than two!",
    5: "A battle of wits? You are utterly unarmed!",
    6: "Time for a technological upgrade!",
    7: "Let's see how well you can swim!",
    8: "Boo! Did I frighten you?",
    9: "Incoming aerial slime bombardment!",
    10: "Let's roll!",
    11: "*Feral Vulpimancer hunter roar!*",
    12: "Smells like victory!",
    13: "Humungousaur! Time to smash!",
    14: "Chill out! Sub-zero freeze!",
    15: "Echo Echo! Hear the noise!",
    16: "Energy absorbed and redirected!",
    17: "Way Big! Stand down!",
    18: "Motion carried! Reality altered.",
}

ALIEN_STATS: dict[int, dict[str, int]] = {
    1: {"Strength": 65, "Speed": 70, "Defense": 75, "Energy": 95, "Intellect": 60},
    2: {"Strength": 80, "Speed": 50, "Defense": 95, "Energy": 70, "Intellect": 65},
    3: {"Strength": 45, "Speed": 100, "Defense": 55, "Energy": 60, "Intellect": 70},
    4: {"Strength": 98, "Speed": 55, "Defense": 90, "Energy": 40, "Intellect": 50},
    5: {"Strength": 20, "Speed": 40, "Defense": 30, "Energy": 50, "Intellect": 100},
    6: {"Strength": 60, "Speed": 65, "Defense": 85, "Energy": 90, "Intellect": 88},
    7: {"Strength": 75, "Speed": 80, "Defense": 65, "Energy": 50, "Intellect": 60},
    8: {"Strength": 50, "Speed": 70, "Defense": 80, "Energy": 85, "Intellect": 75},
    9: {"Strength": 55, "Speed": 85, "Defense": 50, "Energy": 75, "Intellect": 60},
    10: {"Strength": 85, "Speed": 80, "Defense": 100, "Energy": 45, "Intellect": 55},
    11: {"Strength": 78, "Speed": 82, "Defense": 70, "Energy": 35, "Intellect": 45},
    12: {"Strength": 82, "Speed": 65, "Defense": 85, "Energy": 90, "Intellect": 70},
    13: {"Strength": 100, "Speed": 45, "Defense": 95, "Energy": 40, "Intellect": 50},
    14: {"Strength": 65, "Speed": 80, "Defense": 80, "Energy": 92, "Intellect": 75},
    15: {"Strength": 40, "Speed": 65, "Defense": 60, "Energy": 95, "Intellect": 70},
    16: {"Strength": 85, "Speed": 65, "Defense": 90, "Energy": 100, "Intellect": 70},
    17: {"Strength": 100, "Speed": 70, "Defense": 95, "Energy": 98, "Intellect": 65},
    18: {"Strength": 100, "Speed": 100, "Defense": 100, "Energy": 100, "Intellect": 100},
}


def get_simulator_aliens(include_unlocked: bool = True) -> List[AlienProfile]:
    """Retrieve aliens for the Omnitrix Simulator (10 classic or all 18 unlocked)."""
    if include_unlocked:
        return list(DEFAULT_ALIEN_ROSTER) + list(EXTENDED_ALIEN_ROSTER)
    return list(DEFAULT_ALIEN_ROSTER)


def get_alien_quote(alien_id: int) -> str:
    """Get the heroic battle cry/quote for an alien."""
    return ALIEN_QUOTES.get(alien_id, "It's hero time!")


def get_alien_stats(alien_id: int) -> dict[str, int]:
    """Get power stats radar dictionary for an alien."""
    return ALIEN_STATS.get(alien_id, {"Strength": 50, "Speed": 50, "Defense": 50, "Energy": 50, "Intellect": 50})


def get_all_aliens() -> List[AlienProfile]:
    """Retrieve the complete Omnitrix DNA roster."""
    return list(DEFAULT_ALIEN_ROSTER)


def get_alien_by_id(alien_id: int) -> Optional[AlienProfile]:
    """Find alien profile by integer ID (1-10)."""
    for alien in DEFAULT_ALIEN_ROSTER:
        if alien.id == alien_id:
            return alien
    return None


def get_alien_by_name(name: str) -> Optional[AlienProfile]:
    """Find alien profile by name (case-insensitive)."""
    target = name.strip().lower()
    for alien in DEFAULT_ALIEN_ROSTER:
        if alien.name.lower() == target or alien.codename.lower() == target:
            return alien
    return None
