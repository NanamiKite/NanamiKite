<div align="center">

<img src="./assets/banner.png" alt="NanamiKite cyber terminal banner" width="100%" />

</div>

```text
[ LINK STATUS ]  ACTIVE
[ CURRENTLY   ]  DirectHCI / FLOW 8 / SDR tooling
[ INTERESTS   ]  Bluetooth · SDR · Radio · Protocols · Systems
[ MODE        ]  build -> break -> inspect -> fix -> learn
```

I build software around **radios, Bluetooth devices, protocols, and odd hardware**.

Most of my projects start with some variation of:

> I have this weird piece of hardware.  
> The existing software annoys me.  
> Let's figure out how it works.

---

## `// FEATURED PROJECTS`

### [DirectHCI](https://github.com/NanamiKite/DirectHCI)

**Windows userspace Bluetooth controller ownership and Raw HCI infrastructure.**

DirectHCI explores temporarily taking ownership of a Bluetooth controller from the normal Windows stack, exposing low-level HCI/BLE access, and restoring Windows Bluetooth afterwards.

`Rust` · `Windows` · `WinUSB` · `Bluetooth HCI` · `USB`

```text
Windows Bluetooth Stack
          |
          v
 Controller Ownership
          |
          v
       WinUSB
          |
          v
       Raw HCI
          |
          v
 Restore Windows Stack
```

### [FLOW 8 PC Controller](https://github.com/NanamiKite/FLOW-8-PC-Controller)

**Native desktop control software for the Behringer FLOW 8 digital mixer.**

Built around real-device BLE protocol analysis, device-state synchronization, and hardware validation rather than simply wrapping a vendor API.

`Rust` · `BLE / GATT` · `Protocol RE` · `Desktop UI`

```text
FLOW 8 -> BLE -> Protocol Layer -> Mixer State -> Desktop UI
```

### [CodeRecoil for Coyote 2.0](https://github.com/NanamiKite/CodeRecoil-for-Coyote-2.0)

**Editor / compiler events -> physical hardware feedback.**

A small experiment in letting software events escape the screen and interact with a BLE device.

`JavaScript` · `VS Code` · `BLE` · `Hardware Integration`

---

## `// SELECTED ENGINEERING EXPERIENCE`

I've also worked in an existing team codebase on **developer tooling and system integration**.

- IDE / plugin-based tooling and workflow integration
- hardware-related visualization and resource handling
- project automation and template workflows
- changes contributed into an existing upstream / mainline codebase

Enough context to show the kind of engineering work I've touched, without turning this page into a résumé.

---

## `// SIGNAL PATH`

```text
+------------+
|  Hardware  |
+-----+------+
      |
      v
USB / BLE / CAT / IQ
      |
      v
Protocol Analysis
      |
      v
Systems / Application Layer
      |
      v
Rust / Python / JavaScript / Java
      |
      v
Desktop Tools / System Software
```

---

## `// OTHER THINGS I BUILD`

**Radio / SDR**

- [radioManger](https://github.com/NanamiKite/radioManger) — amateur-radio station management
- [PiRadioBox](https://github.com/NanamiKite/PiRadioBox) — Raspberry Pi radio tooling

**Hardware / Software experiments**

- [Pulsedesk](https://github.com/NanamiKite/Pulsedesk) — heart-rate telemetry visualization for OBS
- [CodeRecoil for Coyote 2.0](https://github.com/NanamiKite/CodeRecoil-for-Coyote-2.0) — physical feedback from development events

---

## `// WORKING WITH`

```text
SYSTEMS     Windows APIs / WinUSB / Bluetooth HCI / BLE-GATT / USB
RADIO       SDR / CAT / IQ / protocol analysis
LANGUAGES   Rust / Python / JavaScript / Java
LEARNING    OS / networking / DSP / deeper Rust / open source
```

I care more about **understanding how the pieces connect** than collecting a giant wall of technology badges.

---

## `// HOW I BUILD`

I use AI coding agents extensively as part of my development workflow.

My focus is usually on problem definition, architecture, protocol/device analysis, integration, debugging, real-hardware validation, and reviewing how the resulting system actually behaves.

I'm gradually working backwards through the stack and learning the underlying pieces more deeply instead of treating generated code as a black box.

---

## `// GITHUB TELEMETRY`

<div align="center">

<img height="165" src="https://github-readme-stats.vercel.app/api?username=NanamiKite&show_icons=true&hide_border=true&rank_icon=github&theme=transparent" alt="GitHub stats" />
<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=NanamiKite&layout=compact&hide_border=true&theme=transparent" alt="Top languages" />

</div>

---

<div align="center">

```text
~ RF ~~~~~ BLE ))) ===== USB ===== < HCI > ===== SOFTWARE
```

**Building things because apparently leaving weird hardware alone is not an option.**

</div>
