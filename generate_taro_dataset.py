"""Generate the synthetic Taro Tsujimoto dataset. Tsujimoto is a fictional player (the Sabres' 1974 draft hoax),
so every row is simulated. Usage: python generate_taro_dataset.py (fixed seed, writes CSVs next to this file)."""
import csv, itertools, math, random

SEED, SEASONS, GAMES, SHOTS_PER_GAME = 1974, 20, 70, 3.0
FPS, PUCK_KG, MOVE, FACTOR = 1.46667, 0.17, 100, 1.25
BASE = [10, 16, 18, 14, 14]  # legs, hips/trunk, arms, stick flex, hands: blade mph for a 90 mph puck

sig = lambda x: 1 / (1 + math.exp(-x))
flight = lambda v, d: d / (v * FPS) * 1000
ke = lambda v: 0.5 * PUCK_KG * (v * 0.44704) ** 2
K0 = math.log(.91 / .09) - (flight(80, 35) - 180 - MOVE) / 25
save_prob = lambda v, d, r: sig((flight(v, d) - r - MOVE) / 25 + K0)

# slap share, slap (mean, sd, dist mean), wrist (mean, sd, dist mean), on-net rates (slap, wrist)
COHORTS = {
    "Tsujimoto (hypothetical)": (0.40, (100, 6, 45), (80, 5, 30), (0.50, 0.62)),
    "NHL average shooter": (0.40, (85, 8, 45), (70, 6, 30), (0.45, 0.55)),
}

def poisson(rng, lam):
    L, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= L: return k
        k += 1

def main():
    rng = random.Random(SEED)
    shots, seasons = [], []
    for cohort, (slap_share, slap, wrist, onnet) in COHORTS.items():
        for s in range(1, SEASONS + 1):
            sid = f"{cohort[0]}{s:03d}"
            n_shots = n_net = goals = 0; speeds = []
            for g in range(1, GAMES + 1):
                for k in range(1, poisson(rng, SHOTS_PER_GAME) + 1):
                    is_slap = rng.random() < slap_share
                    mu, sd, dm = slap if is_slap else wrist
                    v = max(40, rng.gauss(mu, sd)); d = min(70, max(10, rng.gauss(dm, 8)))
                    r = min(260, max(140, rng.gauss(180, 15)))
                    on = rng.random() < onnet[0 if is_slap else 1]
                    sp = save_prob(v, d, r)
                    saved = on and rng.random() < sp
                    goal = on and not saved
                    shots.append(dict(cohort=cohort, season_id=sid, game_num=g, shot_num=k,
                        shot_type="slap" if is_slap else "wrist", speed_mph=round(v, 1), distance_ft=round(d, 1),
                        time_to_net_ms=round(flight(v, d), 1), goalie_reaction_ms=round(r, 1),
                        window_ms=round(flight(v, d) - r, 1), on_net=int(on), save_prob=round(sp, 4),
                        saved=int(saved), goal=int(goal)))
                    n_shots += 1; n_net += on; goals += goal; speeds.append(v)
            seasons.append(dict(cohort=cohort, season_id=sid, games=GAMES, shots=n_shots, shots_on_net=n_net,
                goals=goals, shooting_pct=round(goals / n_shots, 3), avg_speed_mph=round(sum(speeds) / len(speeds), 1),
                reached_15_goals=int(goals >= 15)))
    def write(name, rows):
        with open(name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    write("taro_shots.csv", shots); write("taro_seasons.csv", seasons)
    levels = [0.5, 1.0, 1.5, 2.0]
    chain = []
    for c in itertools.product(levels, repeat=5):
        blade = sum(b * m for b, m in zip(BASE, c)); puck = blade * FACTOR
        chain.append(dict(legs_mult=c[0], trunk_mult=c[1], arms_mult=c[2], stick_flex_mult=c[3], hands_mult=c[4],
            blade_speed_mph=round(blade, 1), puck_speed_mph=round(puck, 1), puck_energy_j=round(ke(puck), 1),
            pct_of_108_8_record=round(puck / 108.8 * 100, 1), flight_time_35ft_ms=round(flight(puck, 35), 1)))
    write("taro_kinetic_chain.csv", chain)
    ref = [("Typical wrist shot", 75, "illustrative"), ("Typical slap shot", 90, "illustrative"),
           ("Shea Weber (2015)", 108.5, "NHL skills event"), ("Zdeno Chara (2012 record)", 108.8, "NHL skills event"),
           ("Hypothetical Tsujimoto", 106.5, "model preset")]
    write("taro_benchmarks.csv", [dict(shot=n, speed_mph=v, source=s, flight_time_35ft_ms=round(flight(v, 35), 1),
        puck_energy_j=round(ke(v), 1)) for n, v, s in ref])
    print(len(shots), "shots,", len(seasons), "seasons,", len(chain), "chain rows")

if __name__ == "__main__":
    main()
