# Firmware Research Decision Log

## Baseline Principles
- The project does NOT assume that the Redmi Watch Move supports custom firmware, sideloaded applications, or replacement operating systems (e.g. AsteroidOS or ZeppOS).
- Flashing firmware over BLE without official manufacturer recovery tooling poses a severe brick risk.

## Phase 6 Gates
Firmware modification or update investigations require all of the following conditions to be met:
1. **Authorized & Verifiable Firmware Images:** Image provided directly by manufacturer update servers or official releases.
2. **Hardware Revision & Bootloader Compatibility:** Confirmed SoC architecture (e.g., Apollo4, Nordic nRF53, or BES SoC).
3. **Recovery Path:** Hardware recovery mechanism verified (e.g., test points, SWD, or fail-safe bootloader recovery mode).
4. **User Explicit Approval:** Documented risk assessment signed off by user.

*Status: No firmware flashing or undocumented writes are permitted in this milestone.*
