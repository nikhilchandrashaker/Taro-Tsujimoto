# The Taro Tsujimoto Lab

An interactive hockey analytics and biomechanics project about Taro Tsujimoto, the fictional forward the Buffalo Sabres "drafted" in the 11th round (183rd overall) of the 1974 NHL draft. He supposedly came from the "Tokyo Katanas," and neither the player nor the team existed. This is a companion to the Sidd Finch Lab.

Every number is a modeled estimate. The legend gives Tsujimoto no signature skill, so all ability settings are hypotheticals.

## Files

| File | Purpose |
| --- | --- |
| `taro-tsujimoto-lab.html` | Interactive page, open in any modern browser |
| `generate_taro_dataset.py` | Generates the synthetic dataset (seed 1974) |
| `taro_shots.csv`, `taro_seasons.csv`, `taro_kinetic_chain.csv`, `taro_benchmarks.csv` | The dataset |
| `DATA_DICTIONARY.md` | Column definitions and limitations |

## What is in the lab

1. **Shot lab:** sliders for shot speed, distance, goalie reaction, and shots on net. Outputs flight time, time left after the goalie reacts, save rate, and goal chance per shot.
2. **Biomechanics:** a five-link slap shot kinetic chain (legs, hips and trunk, arms, stick flex, hands) that gives blade speed, puck speed, and puck energy, compared to Zdeno Chara's 108.8 mph record.
3. **Benchmarks:** reference shot speeds, flight times, and energies.
4. **Could he score 15?** Simulates 1,000 seasons from the shot lab settings and reports how often the legend's 15 goals is reached.

## Models and assumptions

- **Flight time:** distance divided by speed, no drag.
- **Save rate:** a logistic curve on the time left after the goalie's reaction and a fixed 100 ms movement, tuned to a 91 percent save rate for an 80 mph shot from 35 ft against a 180 ms goalie.
- **Kinetic chain:** a 72 mph blade-speed split of 10, 16, 18, 14, and 14 mph for a 90 mph shot, with puck speed set to 1.25 times blade speed.
- **Puck energy:** 0.5 times 0.17 kg times speed squared.

## Limitations

No blocks, screens, deflections, rebounds, or shot placement, and no 3D motion model. The kinetic chain split and puck factor are teaching assumptions.

## Ideas for extending it

- Add a 3D slap shot simulation like the Sidd Finch delivery simulation
- Fit the save curve to real shot data
- Add shot location and goalie positioning

## Sources

Draft facts from reporting on the 1974 NHL draft hoax (Buffalo Sabres, Punch Imlach, Paul Wieland). Hardest shot records from NHL All-Star skills competitions.
