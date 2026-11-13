# Taro Tsujimoto dataset: data dictionary

Taro Tsujimoto is a fictional player, the Buffalo Sabres' imaginary pick in the 11th round (183rd overall) of the 1974 NHL draft. **Every row is simulated** from the simplified models in the Taro Tsujimoto Lab, so treat it as practice data. Regenerate it with `python generate_taro_dataset.py` (seed 1974).

## Files

| File | Rows | Grain |
| --- | --- | --- |
| `taro_shots.csv` | 8,468 | One row per shot, 20 simulated 70-game seasons per cohort |
| `taro_seasons.csv` | 40 | One row per simulated season |
| `taro_kinetic_chain.csv` | 1,024 | One row per combination of five slap shot segment multipliers (0.5, 1.0, 1.5, 2.0) |
| `taro_benchmarks.csv` | 5 | One row per reference shot |

## taro_shots.csv

| Column | Meaning |
| --- | --- |
| cohort | `Tsujimoto (hypothetical)` or `NHL average shooter` |
| season_id, game_num, shot_num | Season, game within the season, and shot within the game |
| shot_type | `slap` or `wrist` |
| speed_mph | Puck speed at release |
| distance_ft | Distance from the shot to the goalie |
| time_to_net_ms | Distance divided by speed, no drag |
| goalie_reaction_ms | The goalie's simulated reaction time |
| window_ms | Flight time minus goalie reaction |
| on_net | 1 if the shot was on target |
| save_prob | Modeled chance the goalie stops an on-target shot |
| saved, goal | 1 if saved or scored (both 0 for shots that missed the net) |

## taro_seasons.csv

cohort, season_id, games, shots, shots_on_net, goals, shooting_pct (goals per shot), avg_speed_mph, reached_15_goals (1 if the season reached the legend's 15 goals).

## taro_kinetic_chain.csv

legs_mult, trunk_mult, arms_mult, stick_flex_mult, hands_mult scale a 90 mph shot's blade-speed split of 10, 16, 18, 14, and 14 mph. blade_speed_mph is their sum, puck_speed_mph is blade speed times 1.25, puck_energy_j uses a 0.17 kg puck, pct_of_108_8_record compares to Zdeno Chara's 2012 record, and flight_time_35ft_ms is the time to cover 35 ft.

## taro_benchmarks.csv

shot, speed_mph, source (`illustrative`, `NHL skills event`, or `model preset`), flight_time_35ft_ms, puck_energy_j. The Chara (108.8 mph, 2012) and Weber (108.5 mph, 2015) speeds are from NHL All-Star skills events.

## Known limitations

- Blocks, screens, deflections, rebounds, passes, and shot placement are not modeled, and every shot is independent.
- The save curve is tuned to a 91 percent save rate for an 80 mph shot from 35 ft against a 180 ms goalie, and it rewards closer shots, so wrist shots from 30 ft score more often than real data would show.
- The "Hypothetical Tsujimoto" cohort is invented. The legend gives him no skill beyond a reported stat line of 15 goals and 25 points, and the dataset has no assists.
- Season goal totals run higher than real NHL scoring because every shot is treated as a real scoring chance.
