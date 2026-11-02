# BO Wenqu — Back-to-School Flyer

主视觉海报，文案与品牌取自 `BOWenqu_BackToSchool_CopyPack.md`。

## 交付文件

| 文件 | 尺寸 | 用途 |
|---|---|---|
| `BOWenqu_BackToSchool_Flyer_A4.pdf` | A4 210×297mm，矢量 | 印刷 / PDF 分发 |
| `BOWenqu_BackToSchool_Flyer_A4_300dpi.png` | 2481×3508 px @300dpi | 印刷位图、社交平台 |
| `BOWenqu_BackToSchool_Flyer_A4.png` | 1323×1871 px @160dpi | 屏幕预览 |
| `BOWenqu_BackToSchool_Flyer_Social.pdf` | 1080×1350 px (4:5) | IG / TikTok / 小红书 图文 |
| `BOWenqu_BackToSchool_Flyer_Social.png` | 1080×1350 px | 同上，直接发 |

## 重新生成

```bash
python3 build_flyer.py
```

- A4 版样式在 `build_flyer.py` 的 `CSS_A4` 内
- 社交版样式在 `_social.css`
- 输出目录即本目录；`pdftoppm` 用于位图导出，需要 poppler-utils

依赖：`weasyprint`、`segno`（二维码）、`poppler-utils`。
字体：Fredoka（标题）+ Nunito（正文），缺失时回退到 DejaVu Sans。

## 文案占位值（发布前必须替换）

海报沿用了文案包 §10 的建议默认值，**均为占位**：

| 位置 | 海报当前值 | 替换为 |
|---|---|---|
| 早鸟折扣 / 截止 | `20% OFF · ENDS AUG 22` | 真实折扣与日期 |
| 礼盒价 | `$59` / `was $79` / `save $20` | 真实价格 |
| 件数 | `24 PIECES` | 真实 SKU 数 |
| 满赠门槛 | `$39` / `$69` | 真实门槛 |
| 认证 | `EN71 & ASTM D-4236` | 仅在确有该认证时保留 |
| 链接 / 二维码 | `bowenqu.com/backtoschool` | 真实落地页（二维码会自动重生成） |
| 发货 / 年龄 | `Ships within 48 hours` / `Ages 6+` | 真实政策 |

页脚已保留一行免责说明（英文），确认数据后可删除。

## 改文案

- 海报文案集中在 `build_flyer.py` 的 `HERO` / `OFFER` / `DUAL` / `GIFTS` / `FOOT` 模板字符串里
- 改完跑一次 `python3 build_flyer.py` 即可同时产出 A4 与社交版
- 改链接只需改顶部 `LANDING = "https://..."`，二维码自动同步

## 设计说明

- 主色：紫 `#6C4CF1`（主视觉）/ 橙 `#FF8A3D`（促销 CTA）/ 薄荷 `#2BC48A`（家长线、赠品）/ 粉 `#FF6FA5`（孩子线）
- 双线结构照搬文案包：家长线（FOR PARENTS，理性卖点）｜孩子线（FOR KIDS，社交货币）
- 角标信息条包含：早鸟折扣截止日、满赠门槛、认证、发货时效、质保 —— 也就是文案包里"每个 CTA 挂机制 + 时间"的原则
