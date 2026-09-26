"""LampNode sizing calculations for LPN-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
Reads geometry from cad/src/model.py (PARAMS and part volumes), costs from bom/bom.csv and the
budget from project.yaml. All inputs are assumptions for a paper design; nothing is measured.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, build_parts, head_frame  # noqa: E402

OUT = []  # (key, value, unit) for results.csv


def out(key, value, unit="", fmt="{:.3g}"):
    OUT.append((key, value, unit))
    v = fmt.format(value) if isinstance(value, (int, float)) else str(value)
    print(f"  {key:58s} {v} {unit}")
    return value


def section(t):
    print(f"\n== {t} ==")


# ---------------------------------------------------------------- inputs (Table 1)
LAT = 40.0             # deg N, reference mid-latitude city
H0 = -0.833            # deg, sun elevation at photocell switching (taken as sunset and sunrise)
P_LUM = 100.0          # W, reference luminaire
FLOOR = 0.30           # presence profile floor
BOOST = 0.15           # fraction of dimmed hours at full output (TRL 2 assumption)
K0_DRIVER = 0.06       # dimmed driver model: P_in / P_rated = K0 + (1 - K0) * light level
V_NOM = (120.0, 277.0); V_MIN, V_MAX = 100.0, 305.0
PF_FULL, PF_LOW = 0.90, 0.50
ARM_Z_ABS = 7.80       # m, arm centerline above the road in the reference case
TARIFF = (0.10, 0.25)  # USD per kWh

# 12 V side loads (W), typical parts, no datasheet chosen
L_CTRL = 0.05          # STM32WL-class module asleep, TCXO RTC, accelerometer, light sensor, regulators
L_METER = 0.05         # metering IC and digital isolator
L_COIL = 0.40          # 12 V power relay coil, energized in daytime only (fail-on)
L_RADAR = 0.20         # 24 GHz Doppler module with I/Q output, on at night only
L_HEAD_MCU = 0.03
PSU_NL = 0.10          # W, no-load input of the 5 W module
PSU_ETA = 0.72         # incremental efficiency at light load
PSU_RATED = 5.0        # W
PORT_W = 3.0           # W, hosted sensor allowance, two ports
TX_W = 0.40            # W, radio transmit transient (22 dBm class)


def banner():
    print("LampNode sizing, LPN-CAL-001 v0.1 (all values estimates)")


# ---------------------------------------------------------------- 1. night hours
def night_hours(lat=LAT, h0=H0):
    d = np.arange(1, 366)
    dec = np.radians(23.44) * np.sin(2 * np.pi * (284 + d) / 365)
    phi = math.radians(lat)
    c = (math.sin(math.radians(h0)) - math.sin(phi) * np.sin(dec)) / (math.cos(phi) * np.cos(dec))
    H = np.degrees(np.arccos(np.clip(c, -1, 1)))
    sunset = 12 + H / 15
    sunrise = 12 - H / 15
    return sunset, sunrise + 24          # night from sunset to next sunrise, local solar time


def overlap(a0, a1, b0, b1):
    return np.clip(np.minimum(a1, b1) - np.maximum(a0, b0), 0, None)


def profile_energy(dusk, dawn, kind, k0=0.0, boost=BOOST, floor=FLOOR):
    """Annual luminaire energy in kWh for one profile; clock = local solar time."""
    pin = lambda L: P_LUM * (k0 + (1 - k0) * L) if L < 1 else P_LUM
    total = dawn - dusk
    if kind == "photocell":
        wh = total * P_LUM
    elif kind == "schedule":
        dim = overlap(dusk, dawn, 23, 29)
        wh = (total - dim) * P_LUM + dim * pin(0.5)
    elif kind == "presence":
        dim = overlap(dusk, dawn, 22, 30)
        wh = (total - dim) * P_LUM + dim * (boost * P_LUM + (1 - boost) * pin(floor))
    return wh.sum() / 1000, (dim.sum() if kind != "photocell" else 0.0)


def energy():
    section("1. Night hours and annual energy (R7)")
    dusk, dawn = night_hours()
    nh = (dawn - dusk).sum()
    out("night hours per year at 40 N, sunset to sunrise", nh, "h", "{:.0f}")
    out("mean night length", nh / 365, "h", "{:.2f}")
    out("longest night / shortest night", f"{(dawn - dusk).max():.2f} / {(dawn - dusk).min():.2f}", "h")
    e_pc, _ = profile_energy(dusk, dawn, "photocell")
    e_sc, dim_sc = profile_energy(dusk, dawn, "schedule")
    e_pr, dim_pr = profile_energy(dusk, dawn, "presence")
    out("photocell, full power", e_pc, "kWh/yr", "{:.0f}")
    out("schedule only (50 % from 23:00 to 05:00)", e_sc, "kWh/yr", "{:.0f}")
    out("  schedule saving", 100 * (1 - e_sc / e_pc), "%", "{:.1f}")
    out("presence profile, dimmed hours per year", dim_pr, "h", "{:.0f}")
    out("  dimmed hours per night, mean", dim_pr / 365, "h", "{:.2f}")
    out("presence profile, luminaire only", e_pr, "kWh/yr", "{:.0f}")
    sc = self_consumption(nh)
    e_ctrl = sc["avg_in"] * 8760 / 1000
    out("controller energy per year", e_ctrl, "kWh/yr", "{:.1f}")
    e_tot = e_pr + e_ctrl
    out("presence profile with controller", e_tot, "kWh/yr", "{:.0f}")
    sav = 100 * (1 - e_tot / e_pc)
    out("R7 saving, ideal driver", sav, "%", "{:.1f}")
    out("  margin over the 35 % target, ideal driver", sav - 35, "points", "{:.1f}")
    e_pr_k, _ = profile_energy(dusk, dawn, "presence", k0=K0_DRIVER)
    sav_k = 100 * (1 - (e_pr_k + e_ctrl) / e_pc)
    out("presence profile, luminaire only, dimmed driver model", e_pr_k, "kWh/yr", "{:.0f}")
    out("presence profile with controller, dimmed driver model", e_pr_k + e_ctrl, "kWh/yr", "{:.0f}")
    out(f"R7 saving, dimmed driver model (K0 = {K0_DRIVER})", sav_k, "%", "{:.1f}")
    out("  shortfall against the 35 % target, dimmed driver model", 35 - sav_k, "points", "{:.1f}")
    out("energy saved per year, dimmed driver model", e_pc - e_pr_k - e_ctrl, "kWh", "{:.0f}")
    # TRL 2 method for comparison (4,100 h, 11.2 h per night, fixed split)
    trl2 = (3.2 * 100 + 8 * (0.15 * 100 + 0.85 * 30)) * 366 / 1000
    out("TRL 2 method, presence luminaire energy (check)", trl2, "kWh/yr", "{:.0f}")
    # Sensitivity: presence events per hour -> boost fraction
    ev_dur = (15 - 3) / 1.4 + 60 + 1.0      # s: detection to under the lamp, 60 s hold, ramp
    out("time from detection at 15 m to about 3 m from the pole", (15 - 3) / 1.4, "s", "{:.1f}")
    out("duration of one isolated pedestrian event", ev_dur, "s", "{:.0f}")
    out("isolated events per hour equal to 15 % boost", BOOST * 3600 / ev_dur, "per h", "{:.1f}")
    rows = []
    for evh in (0, 4, 8, 16, 30):
        f = 1 - math.exp(-evh * ev_dur / 3600)   # random arrivals, overlapping holds merge
        e, _ = profile_energy(dusk, dawn, "presence", k0=K0_DRIVER, boost=f)
        rows.append((evh, 100 * f, 100 * (1 - (e + e_ctrl) / e_pc)))
        print(f"    {evh:3d} events/h  boost {100 * f:5.1f} %  saving {rows[-1][2]:5.1f} %")
    OUT.append(("R7 saving at 30 events per hour, dimmed driver", rows[-1][2], "%"))
    # Latitude sensitivity
    d60, w60 = night_hours(60.0)
    e60_pc = profile_energy(d60, w60, "photocell")[0]
    e60_pr = profile_energy(d60, w60, "presence", k0=K0_DRIVER)[0] + e_ctrl
    out("60 N: night hours per year", (w60 - d60).sum(), "h", "{:.0f}")
    out("60 N: photocell energy", e60_pc, "kWh/yr", "{:.0f}")
    out("60 N: saving, dimmed driver model", 100 * (1 - e60_pr / e60_pc), "%", "{:.1f}")
    return dict(nh=nh, e_pc=e_pc, e_sc=e_sc, e_pr=e_pr, e_tot=e_tot, sav=sav, sav_k=sav_k,
                saved=e_pc - e_pr_k - e_ctrl, e_ctrl=e_ctrl, e_pr_k=e_pr_k, rows=rows)


# ---------------------------------------------------------------- 2. self-consumption
def self_consumption(nh, verbose=False):
    fn = nh / 8760
    coil = L_COIL * (1 - fn)
    head = (L_RADAR + L_HEAD_MCU) * fn
    sub = L_CTRL + L_METER + coil + head
    avg_in = PSU_NL + sub / PSU_ETA
    shunt = (P_LUM / (120 * PF_FULL)) ** 2 * 0.002 * fn        # 2 mOhm shunt at 120 V, night only
    return dict(fn=fn, coil=coil, head=head, sub=sub, avg_in=avg_in + shunt, shunt=shunt)


def power_budget(nh):
    section("2. Self-consumption (R10) and supply loading (R13)")
    s = self_consumption(nh)
    out("night fraction of the year", s["fn"], "", "{:.3f}")
    out("relay coil average (0.40 W, day only)", s["coil"], "W", "{:.3f}")
    out("radar and head board average (night only)", s["head"], "W", "{:.3f}")
    out("12 V side subtotal", s["sub"], "W", "{:.3f}")
    out("shunt loss, reference lamp at 120 V, averaged", s["shunt"] * 1000, "mW", "{:.1f}")
    out("R10 average from the mains", s["avg_in"], "W", "{:.2f}")
    day = L_CTRL + L_METER + L_COIL + PORT_W
    night = L_CTRL + L_METER + L_RADAR + L_HEAD_MCU + PORT_W
    peak = max(day, night) + TX_W
    out("12 V load, day, ports at 3 W", day, "W", "{:.2f}")
    out("12 V load, night, ports at 3 W", night, "W", "{:.2f}")
    out("12 V peak with radio transmit", peak, "W", "{:.2f}")
    out("supply loading at 25 to 50 C", 100 * peak / PSU_RATED, "%", "{:.0f}")
    return dict(s=s, peak=peak, day=day, night=night)


# ---------------------------------------------------------------- 3. relay and inrush
def relay():
    section("3. Switching and inrush (R3)")
    i_400 = 400 / (V_MIN * PF_FULL)
    out("steady current, 400 W at 100 V and PF 0.90", i_400, "A", "{:.2f}")
    i_100 = P_LUM / (V_NOM[0] * PF_FULL)
    out("steady current, reference 100 W at 120 V", i_100, "A", "{:.2f}")
    inr230 = 60.0   # A cold-start peak, typical 100 W outdoor driver at 230 V (assumption)
    inr277 = inr230 * 277 / 230
    out("reference driver inrush at 277 V, random closing", inr277, "A", "{:.0f}")
    out("four 100 W drivers on one relay, random closing", 4 * inr277, "A", "{:.0f}")
    # Zero-cross closing: residual from closing-time error plus bulk capacitor dv/dt current
    C_bulk = 47e-6
    for f in (50, 60):
        w = 2 * math.pi * f
        vpk = 277 * math.sqrt(2)
        dt = 0.5e-3   # s, closing-time error after learning the release time
        v_err = vpk * math.sin(w * dt)
        i_res = inr277 * v_err / vpk + C_bulk * vpk * w
        out(f"zero-cross closing, one driver, {f} Hz, 0.5 ms error", i_res, "A", "{:.0f}")
    out("switching cycles over 20 years at 2 per day", 2 * 365 * 20, "cycles", "{:.0f}")
    return dict(i_400=i_400, inr277=inr277, inr4=4 * inr277, i_zc=i_res)


# ---------------------------------------------------------------- 4. dimming output
def dimming():
    section("4. 0 to 10 V output (R4)")
    step = 10.0 / 4096
    out("12-bit PWM step on 0 to 10 V", step * 1000, "mV", "{:.2f}")
    out("1 % dimming step", 100, "mV", "{:.0f}")
    out("drivers per output at 2 mA control current, 10 mA sink", 10 / 2, "drivers", "{:.0f}")
    out("sink transistor dissipation at 10 mA, 10 V", 0.1, "W", "{:.2f}")


# ---------------------------------------------------------------- 5. clock
def clock():
    section("5. Clock drift without the network (R5)")
    k = 0.034   # ppm per K^2, tuning-fork crystal
    rows = {}
    for T in (25, -10, -30, 70):
        ppm = 20 + k * (T - 25) ** 2
        s30 = ppm * 1e-6 * 30 * 86400
        rows[T] = s30
        out(f"32 kHz crystal (+-20 ppm) held at {T} C, 30 days", s30, "s", "{:.0f}")
    tcxo = 3.5e-6 * 30 * 86400
    out("TCXO RTC (+-3.5 ppm, -40 to 85 C), 30 days", tcxo, "s", "{:.1f}")
    return dict(x_m10=rows[-10], x_m30=rows[-30], tcxo=tcxo)


# ---------------------------------------------------------------- 6. radar
def radar():
    section("6. Presence detection (R6)")
    hx, htop, hzc = head_frame(P)
    h = ARM_Z_ABS + (hzc - P["arm_z"]) / 1000
    tilt = P["radar_tilt"]
    out("radar height above the road (model)", h, "m", "{:.2f}")
    out("beam center reaches the road at", h / math.tan(math.radians(tilt)), "m", "{:.1f}")
    half = 17.0   # deg, half-power half-width in elevation (assumption, 4-patch module)
    for name, zt, rng in (("pedestrian", 1.0, 15.0), ("car or cyclist", 0.7, 25.0)):
        dep = math.degrees(math.atan((h - zt) / rng))
        out(f"{name} at {rng:.0f} m: depression angle", dep, "deg", "{:.1f}")
    ped_near = (h - 1.0) / math.tan(math.radians(tilt + half))
    ped_far = (h - 1.0) / math.tan(math.radians(tilt - half))
    out("pedestrian coverage inside the half-power beam, near", ped_near, "m", "{:.1f}")
    out("pedestrian coverage inside the half-power beam, far", ped_far, "m", "{:.1f}")
    lam = 3e8 / 24.125e9
    # radar equation
    pt, g, sigma = 8.0, 11.0, 0.5     # dBm, dBi each way, m^2 (walking person, assumption)
    nf, bw, snr_req = 35.0, 10.0, 15.0  # dB effective at low Doppler, Hz, dB
    noise = -174 + 10 * math.log10(bw) + nf
    def pr(R, sig=sigma, loss=0.0):
        return (pt + 2 * g + 20 * math.log10(lam) + 10 * math.log10(sig) - 30 * math.log10(4 * math.pi)
                - 40 * math.log10(R) - loss)
    R_ped = math.hypot(15, h - 1.0)
    snr15 = pr(R_ped) - noise
    out("slant range to pedestrian at 15 m", R_ped, "m", "{:.1f}")
    out("received power, pedestrian at 15 m", pr(R_ped), "dBm", "{:.0f}")
    out("noise floor (10 Hz, 35 dB effective noise figure)", noise, "dBm", "{:.0f}")
    out("SNR, pedestrian at 15 m", snr15, "dB", "{:.0f}")
    r_max = R_ped * 10 ** ((snr15 - snr_req) / 40)
    out("slant range at 15 dB SNR, pedestrian on boresight", r_max, "m", "{:.0f}")
    out("same with 6 dB two-way beam-edge loss", R_ped * 10 ** ((snr15 - snr_req - 6) / 40), "m", "{:.0f}")
    # Doppler
    def fd(v, dep):
        return 2 * v * math.cos(math.radians(dep)) / lam
    dep_p = math.degrees(math.atan((h - 1.0) / 15))
    out("Doppler, pedestrian 1.4 m/s approaching", fd(1.4, dep_p), "Hz", "{:.0f}")
    dep_c = math.degrees(math.atan((h - 0.7) / 25))
    out("Doppler, cyclist 5 m/s approaching", fd(5.0, dep_c), "Hz", "{:.0f}")
    out("Doppler, car 50 km/h approaching", fd(50 / 3.6, dep_c), "Hz", "{:.0f}")
    for vr, lab in ((2.0, "drizzle 2 m/s"), (7.0, "heavy rain 7 m/s")):
        out(f"Doppler, {lab} falling (receding)", 2 * vr * math.sin(math.radians(tilt)) / lam, "Hz", "{:.0f}")
    # timing
    t_resp = 2 * 0.128 + 0.01 + 0.01 + 0.05 + 0.30
    out("detection to full output (two 128 ms frames, link, driver 0.3 s)", t_resp, "s", "{:.2f}")
    out("warning before a pedestrian at 15 m reaches the pole", 15 / 1.4, "s", "{:.1f}")
    return dict(h=h, ped_near=ped_near, ped_far=ped_far, snr15=snr15, r_max=r_max, t_resp=t_resp,
                fd_p=fd(1.4, dep_p), fd_rain=2 * 2.0 * math.sin(math.radians(tilt)) / lam)


# ---------------------------------------------------------------- 7. metering
def metering():
    section("7. Metering accuracy (R8)")
    r_sh = 0.002
    i_max = 400 / (V_MIN * PF_FULL)
    i_min = 10 / (V_MAX * PF_LOW)
    out("current range, 10 W at 305 V PF 0.5 to 400 W at 100 V", f"{i_min * 1000:.0f} mA to {i_max:.2f} A", "")
    fs = 354.0 / 16   # mV rms, 500 mV peak input at PGA gain 16
    out("shunt signal at minimum current (2 mOhm)", i_min * r_sh * 1000, "mV", "{:.3f}")
    out("ratio of full scale to minimum signal", fs / (i_min * r_sh * 1000), ":1", "{:.0f}")
    out("shunt dissipation at 4.44 A", i_max ** 2 * r_sh, "W", "{:.3f}")
    terms = {"metering IC over 1000:1": 0.5, "shunt tempco 50 ppm/K over 50 K": 0.25,
             "divider tempco": 0.10, "phase error 0.1 deg at PF 0.5": 100 * math.radians(0.1) * math.tan(math.acos(0.5)),
             "bench reference for one-point calibration": 0.5}
    for k, v in terms.items():
        out(f"  {k}", v, "%", "{:.2f}")
    rss = math.sqrt(sum(v * v for v in terms.values()))
    lin = sum(terms.values())
    out("error with one-point calibration, RSS", rss, "%", "{:.2f}")
    out("error with one-point calibration, worst-case sum", lin, "%", "{:.2f}")
    unc = lin - terms["bench reference for one-point calibration"] + 1.0 + 0.2
    out("worst-case sum without calibration (1 % shunt, 0.2 % divider)", unc, "%", "{:.2f}")
    return dict(rss=rss, lin=lin, unc=unc)


# ---------------------------------------------------------------- 8. airtime and last gasp
def toa(pl_app, sf, bw=125e3, cr=1, pre=8, ldro=None):
    pl = pl_app + 13
    de = (1 if sf >= 11 else 0) if ldro is None else ldro
    ts = 2 ** sf / bw
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (pre + 4.25) * ts + n * ts


def radio():
    section("8. Radio airtime, fault reporting and last gasp (R9, R15)")
    per = 96
    res = {}
    for sf in (7, 9, 10, 12):
        t = toa(24, sf)
        res[sf] = t
        out(f"24-byte status at SF{sf}: time on air", t * 1000, "ms", "{:.0f}")
        out(f"  96 per day at SF{sf}", t * per, "s/day", "{:.1f}")
    out("EU868 1 % duty cycle: off time after one SF9 status", 99 * res[9], "s", "{:.0f}")
    t_fault = toa(6, 9)
    out("6-byte fault message at SF9", t_fault * 1000, "ms", "{:.0f}")
    # last gasp energy: 22 dBm transmit 120 mA, MCU 5 mA, two receive windows 0.3 s at 6 mA, margin x3
    e_msg = 3.3 * (0.120 * toa(6, 10) + 0.005 * 0.1 + 0.006 * 0.6)
    out("last-gasp energy at SF10, 22 dBm", e_msg, "J", "{:.3f}")
    C = 0.22
    e_cap = 0.5 * C * (5.0 ** 2 - 3.6 ** 2)
    out("0.22 F supercapacitor, 5.0 to 3.6 V, usable", e_cap, "J", "{:.2f}")
    out("last-gasp margin", e_cap / e_msg, "x", "{:.0f}")
    out("supercapacitor charge time at 20 mA", C * 5.0 / 0.020, "s", "{:.0f}")
    return dict(toa9=res[9], toa10=res[10], toa12=res[12], day9=res[9] * per, day10=res[10] * per,
                day12=res[12] * per, e_msg=e_msg, e_cap=e_cap)


# ---------------------------------------------------------------- 9. surge
def surge():
    section("9. Surge (R11)")
    # 8/20 us current wave as a double exponential fitted to T1 = 8 us, T2 = 20 us
    best = None
    for ta in np.linspace(15e-6, 40e-6, 126):
        for tb in np.linspace(1e-6, 8e-6, 141):
            t = np.linspace(0, 150e-6, 6001)
            i = np.exp(-t / ta) - np.exp(-t / tb)
            i /= i.max()
            t10, t90 = t[np.argmax(i >= 0.1)], t[np.argmax(i >= 0.9)]
            T1 = 1.25 * (t90 - t10)
            t0 = t10 - 0.1 * T1  # virtual origin: 10 %-90 % line crosses zero
            ip = np.argmax(i)
            t50 = t[ip + np.argmax(i[ip:] <= 0.5)]
            T2 = t50 - t0
            err = (T1 - 8e-6) ** 2 + (T2 - 20e-6) ** 2
            if best is None or err < best[0]:
                best = (err, ta, tb, np.trapezoid(i, t))
    q_per_a = best[3]
    out("8/20 us wave: charge per ampere of peak", q_per_a * 1e6, "us", "{:.1f}")
    for ip, vc in ((5000, 1000), (10000, 1150)):
        out(f"MOV energy at {ip / 1000:.0f} kA, clamping about {vc} V (385 V class)", vc * ip * q_per_a, "J", "{:.0f}")
    out("MOV continuous rating over 305 V maximum, 320 V class", 100 * (320 / 305 - 1), "%", "{:.0f}")
    out("MOV continuous rating over 305 V maximum, 385 V class", 100 * (385 / 305 - 1), "%", "{:.0f}")
    return dict(q=q_per_a, e5=1000 * 5000 * q_per_a)


# ---------------------------------------------------------------- 10. thermal
def thermal(pb):
    section("10. Controller temperature in sun (R11)")
    D, H = P["dome_d"] / 1000, (P["dome_h"] + P["base_h"]) / 1000
    T_amb, G, alpha, elev = 45.0, 1000.0, 0.35, 60.0
    Ap = D * H * math.cos(math.radians(elev)) + math.pi * D ** 2 / 4 * math.sin(math.radians(elev))
    q_sun = alpha * G * Ap
    As = math.pi * D * H + math.pi * D ** 2 / 4
    Tk = 273.15 + 58
    h_r = 4 * 0.9 * 5.67e-8 * Tk ** 3
    h = 5.0 + h_r
    UA = As * h
    Gb, dT_lum = 0.2, 20.0     # W/K to the luminaire top; luminaire top 20 K over ambient in sun
    q_int = PSU_NL + (L_CTRL + L_METER + L_COIL) / PSU_ETA   # all daytime input becomes heat in the dome
    q_int_ports = q_int + PORT_W * (1 / 0.80 - 1)   # extra supply loss at 80 % when ports carry 3 W
    shell = (q_sun + q_int + Gb * dT_lum) / (UA + Gb)
    shell_p = (q_sun + q_int_ports + Gb * dT_lum) / (UA + Gb)
    out("projected area in sun at 60 deg elevation", Ap * 1e4, "cm2", "{:.0f}")
    out("solar gain, absorptance 0.35", q_sun, "W", "{:.2f}")
    out("outer area", As * 1e4, "cm2", "{:.0f}")
    out("film coefficient, still air plus radiation", h, "W/(m2 K)", "{:.1f}")
    out("internal dissipation, day, ports unloaded", q_int, "W", "{:.2f}")
    out("internal dissipation, day, ports at 3 W", q_int_ports, "W", "{:.2f}")
    out("shell rise over 45 C ambient, ports unloaded", shell, "K", "{:.1f}")
    out("interior (shell + 5 K), ports unloaded", T_amb + shell + 5, "C", "{:.0f}")
    out("interior (shell + 5 K), ports at 3 W", T_amb + shell_p + 5, "C", "{:.0f}")
    T_int = T_amb + shell_p + 5
    derate = 1.0 if T_int <= 50 else max(0.6, 1 - 0.4 * (T_int - 50) / 20)
    out("supply capacity at that interior temperature (derating assumption)", PSU_RATED * derate, "W", "{:.2f}")
    out("12 V peak demand", pb["peak"], "W", "{:.2f}")
    return dict(T0=T_amb + shell + 5, T3=T_int, cap=PSU_RATED * derate)


# ---------------------------------------------------------------- 11. hosted power
def hosted():
    section("11. Hosted sensor ports (R13)")
    rho, a = 0.0172, 0.34
    i = PORT_W / 12
    dv = i * 2 * 10 * rho / a
    out("one port at 3 W, 10 m of 0.34 mm2 cable: drop", dv, "V", "{:.2f}")
    out("  as a share of 12 V", 100 * dv / 12, "%", "{:.1f}")
    i_head = (PORT_W + L_RADAR + L_HEAD_MCU) / 12
    out("controller to head cable current", i_head, "A", "{:.2f}")
    out("  drop over 1 m", i_head * 2 * 1 * rho / a, "V", "{:.3f}")
    return dict(dv=dv)


# ---------------------------------------------------------------- 12. mass
def mass():
    section("12. Mass (estimates; model volumes where the part is modeled as a shell)")
    vols = {n: s.volume / 1e3 for n, s, _, _, _ in build_parts()}
    dome = vols["Dome cover, UV-stable"] * 1.07 / 1000
    box = vols["Sensor head enclosure"] * 1.20 / 1000
    ctrl = {"dome, ASA": dome, "base, PC at 35 % of the solid envelope, brass blades": 0.35 * vols["Twist-lock base, 7-contact"] * 1.2 / 1000 + 0.02,
            "power supply module": 0.05, "relay": 0.02, "surge stage and fuse": 0.03,
            "controller board and supercapacitor": 0.03, "antenna and light pipe": 0.01, "potting, screws": 0.03}
    head = {"enclosure, PC": box, "radar": 0.02, "head board": 0.02, "two M12 ports": 0.03,
            "two band clamps and bracket": 0.15, "M12 port and 1 m cable": 0.07}
    mc, mh = sum(ctrl.values()), sum(head.values())
    for k, v in ctrl.items():
        out(f"  controller: {k}", v, "kg", "{:.3f}")
    for k, v in head.items():
        out(f"  head: {k}", v, "kg", "{:.3f}")
    out("controller mass", mc, "kg", "{:.2f}")
    out("sensor head with clamps and cable", mh, "kg", "{:.2f}")
    return dict(mc=mc, mh=mh)


# ---------------------------------------------------------------- 13. cost
def cost(saved):
    section("13. Cost and payback (R16)")
    rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
    budget = yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"]
    tot, ctrl, head = 0.0, 0.0, 0.0
    for r in rows:
        n = int(r["item"].split()[0])
        c = float(r["qty"]) * float(r["unit_cost_usd"])
        tot += c
        if n <= 9:
            ctrl += c
        elif n <= 15:
            head += c
    out("BOM lines", len(rows), "", "{:.0f}")
    out("controller parts (items 1 to 9)", ctrl, "USD", "{:.2f}")
    out("sensor head, cable and ports (items 10 to 15)", head, "USD", "{:.2f}")
    out("hardware and consumables (item 16)", tot - ctrl - head, "USD", "{:.2f}")
    out("BOM total", tot, "USD", "{:.2f}")
    out("budget_usd (project.yaml)", budget, "USD", "{:.0f}")
    out("margin", budget - tot, "USD", "{:.2f}")
    for t in TARIFF:
        out(f"payback on parts at ${t:.2f}/kWh", tot / (saved * t), "years", "{:.1f}")
    return dict(tot=tot, ctrl=ctrl, head=head, budget=budget)


def main():
    banner()
    e = energy()
    pb = power_budget(e["nh"])
    r = relay()
    dimming()
    c = clock()
    rd = radar()
    m = metering()
    ra = radio()
    s = surge()
    th = thermal(pb)
    hs = hosted()
    ms = mass()
    co = cost(e["saved"])

    status = [
        ("R1", "Fit the socket", "Representative ANSI C136.41 base in the model; fit and 5 min change not checkable on paper", "Not verifiable at TRL 3"),
        ("R2", "Mains range", "Supply 85 to 305 V; 385 V class MOV; 120 to 277 V scope (DDR item 9)", "Met (design review)"),
        ("R3", "Switch the luminaire", f"{r['i_400']:.2f} A steady at 400 W; inrush {r['inr277']:.0f} A per 100 W driver, {r['inr4']:.0f} A for four; about {r['i_zc']:.0f} A with zero-cross closing", "At risk"),
        ("R4", "Dim the luminaire", "2.4 mV steps; 10 mA sink = 5 drivers at 2 mA; D4i is a later variant (DDR item 5)", "Met (design review)"),
        ("R5", "Schedule without the network", f"Crystal: {c['x_m10']:.0f} s at -10 C, {c['x_m30']:.0f} s at -30 C per 30 days (not met); TCXO clock: {c['tcxo']:.0f} s", "Met on paper with the TCXO clock"),
        ("R6", "Detect presence", f"Beam covers {rd['ped_near']:.1f} to {rd['ped_far']:.0f} m; SNR {rd['snr15']:.0f} dB at 15 m; {rd['t_resp']:.2f} s to full; clutter and rain unverified", "At risk"),
        ("R7", "Save energy", f"{e['sav']:.1f} % ideal driver, {e['sav_k']:.1f} % dimmed driver model, target 35 %", "At risk"),
        ("R8", "Measure energy", f"{m['lin']:.2f} % worst case with one-point calibration ({m['unc']:.2f} % without)", "Met on paper (calibration required)"),
        ("R9", "Report faults", f"Last gasp {ra['e_msg']:.3f} J against {ra['e_cap']:.2f} J stored; 15 min status", "Met (design review)"),
        ("R10", "Self-consumption", f"{pb['s']['avg_in']:.2f} W average", "Met on paper"),
        ("R11", "Environment", f"Interior {th['T0']:.0f} to {th['T3']:.0f} C at 45 C in sun (70 C rating); MOV {s['e5']:.0f} J at 5 kA; IP66 and surge need tests", "At risk"),
        ("R12", "Fail safe", "NC relay, open 0 to 10 V = full, coil needs a toggling drive, day decision needs clock AND light sensor", "Met (design review)"),
        ("R13", "Host other sensors", f"{hs['dv']:.2f} V drop at 10 m; {pb['peak']:.2f} W peak against {th['cap']:.2f} W derated supply at {th['T3']:.0f} C", "At risk"),
        ("R14", "Privacy", "Doppler radar, no image; presence counts only", "Met (design review)"),
        ("R15", "Secure and open", f"LoRaWAN 1.0.4, open payload; {ra['day9']:.1f} s/day at SF9; TALQ in CityTwin (DDR item 10)", "Met (design review)"),
        ("R16", "Affordable", f"${co['tot']:.2f} against ${co['budget']}", "Met"),
    ]
    section("Results table")
    for row in status:
        print(f"  {row[0]:4s} {row[3]:36s} {row[2]}")
    with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "value", "unit"])
        for k, v, u in OUT:
            w.writerow([k, f"{v:.4g}" if isinstance(v, float) else v, u])
        w.writerow([])
        w.writerow(["requirement", "title", "result", "status"])
        for row in status:
            w.writerow(row)
    print("\nwrote docs/04-calcs/results.csv")


if __name__ == "__main__":
    main()
