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
