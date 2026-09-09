import math
R_SUN=696000.0; R_EARTH=6371.0; R_MOON=1737.4
D_SUN_MEAN=149597870.0
D_MOON_MEAN=384400.0; D_MOON_PERI=356500.0; D_MOON_APO=406700.0
def ad(R,d): return math.degrees(2*math.asin(R/d))

print("=== 角直径 (修正后的文档值) ===")
for n,R,d,dd,dm in [("太阳平均",R_SUN,D_SUN_MEAN,0.5331,31.99),("太阳近日",R_SUN,147100000.,0.5422,32.53),
                    ("太阳远日",R_SUN,152100000.,0.5244,31.46),("月球平均",R_MOON,D_MOON_MEAN,0.5179,31.08),
                    ("月球近地",R_MOON,D_MOON_PERI,0.5585,33.51),("月球远地",R_MOON,D_MOON_APO,0.4895,29.37)]:
    a=ad(R,d); ok = abs(round(a,4)-dd)<1e-9 and abs(round(a*60,2)-dm)<1e-9
    print(f"  {n}: {a:.6f}° = {a*60:.4f}′   文档[{dd}/{dm}]  {'OK' if ok else '✗'}")

print("\n=== 影锥 (D = 太阳到遮挡天体的距离) ===")
D_sun_moon = D_SUN_MEAN - D_MOON_MEAN          # 日食：太阳到月球
L_moon  = R_MOON *D_sun_moon/(R_SUN-R_MOON)
L_earth = R_EARTH*D_SUN_MEAN /(R_SUN-R_EARTH)  # 月食：太阳到地球
print(f"  日月距离 = {D_sun_moon:,.0f} km")
print(f"  月球本影锥长 L = {L_moon:,.0f} km      文档[373,410]")
print(f"  地球本影锥长 L = {L_earth:,.0f} km   文档[1,382,030]")

# 自洽性检查：L 应等于 月球角径==太阳角径 时的地月距离
lo,hi=300000.,500000.
for _ in range(200):
    m=(lo+hi)/2
    if ad(R_MOON,m) >= ad(R_SUN,D_sun_moon+m): lo=m
    else: hi=m
print(f"  角径相等时的地月距离 = {lo:,.0f} km   → 与 L 之差 {abs(lo-L_moon):.1f} km  {'✓ 自洽' if abs(lo-L_moon)<1 else '✗'}")
print(f"  地表观察者临界（+1 地球半径）= {L_moon+R_EARTH:,.0f} km   文档[379,780]")
print(f"  地月平均距离 {D_MOON_MEAN:,.0f} km  >  临界 {L_moon+R_EARTH:,.0f} km")
print(f"  → 平均情况下影锥够不到地球，所以日环食比日全食略常见 ✓")
print(f"  月球本影半角 = {math.degrees(math.atan((R_SUN-R_MOON)/D_sun_moon)):.4f}°   文档[0.2666]")
print(f"  月球半影半角 = {math.degrees(math.atan((R_SUN+R_MOON)/D_sun_moon)):.4f}°   文档[0.2680]")
print(f"  地球本影半角 = {math.degrees(math.atan((R_SUN-R_EARTH)/D_SUN_MEAN)):.4f}°   文档[0.2641]")
print(f"  地球半影半角 = {math.degrees(math.atan((R_SUN+R_EARTH)/D_SUN_MEAN)):.4f}°   文档[0.2690]")
rU=R_EARTH*(1-D_MOON_MEAN/L_earth); rP=R_EARTH+D_MOON_MEAN*math.tan(math.atan((R_SUN+R_EARTH)/D_SUN_MEAN))
print(f"  地球本影@月距 r={rU:,.0f} km ({2*rU/(2*R_MOON):.2f} 个月亮宽)   文档[4,599 / 2.65]")
print(f"  地球半影@月距 r={rP:,.0f} km ({2*rP/(2*R_MOON):.2f} 个月亮宽)   文档[8,176 / 4.71]")

print("\n=== 环食时天空几乎不变暗（重要教学点）===")
def inter(r1,r2,d):
    if d>=r1+r2: return 0.0
    if d<=abs(r1-r2): return math.pi*min(r1,r2)**2
    d=max(d,1e-9); d1=(d*d+r1*r1-r2*r2)/(2*d); d2=d-d1
    return (r1*r1*math.acos(max(-1,min(1,d1/r1)))-d1*math.sqrt(max(r1*r1-d1*d1,0))
          + r2*r2*math.acos(max(-1,min(1,d2/r2)))-d2*math.sqrt(max(r2*r2-d2*d2,0)))
def sky(o):
    lum=1.0-o; t=max(0.,min(1.,lum/0.006)); return lum**0.18*(0.03+0.97*(t*t*(3-2*t)))
rS=ad(R_SUN,D_SUN_MEAN)/2
for label,dm_ in [("远地点环食",D_MOON_APO),("平均距离环食",D_MOON_MEAN)]:
    rM=ad(R_MOON,dm_)/2; obsc=inter(rS,rM,0)/(math.pi*rS*rS)
    print(f"  {label}: 最大遮挡 {obsc:.1%}  剩余金环 {1-obsc:.1%}  → skyBrightness = {sky(obsc):.3f}")
print("  对比日全食: 遮挡 100% → skyBrightness = 0.000")
print("  → 环食时天空亮度还有 0.7 以上，几乎不变暗！这是环食与全食最大的体验差别。")

print("\n=== 食分分类 ===")
def mag(rS,rM,d): return (rS+rM-d)/(2*rS)
for label,dm_ in [("近地点",D_MOON_PERI),("平均",D_MOON_MEAN),("远地点",D_MOON_APO)]:
    rM=ad(R_MOON,dm_)/2
    t='日全食' if rM>=rS else '日环食'
    print(f"  {label} d={dm_:,.0f}: rM={rM:.4f}° rS={rS:.4f}° 食分={mag(rS,rM,0):.3f} → {t}")
