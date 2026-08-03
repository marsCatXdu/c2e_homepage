#!/usr/bin/env python3
"""Add 2024+ publications co-authored by People members and Danny H.K. Tsang."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "src/content/publications/publications.yaml"

# Sourced from Google Scholar (user 27LmFbwAAAAJ, verified email ece.ust.hk)
# and OpenAlex author A5040138091. Papers must list a People member and D.H.K. Tsang.
# Emails verified on arXiv HTML: eetsang@ust.hk (Danny).
CURATED = [
    # 2026
    {
        "authors": "T. Zhan, S. Shen, and D.H.K. Tsang",
        "title": "Physics-Informed Neural Optimization Based Antenna Coding Design for Pixel Antenna Systems",
        "venue": "arXiv preprint arXiv:2606.21235",
        "year": 2026,
        "type": "journal",
        "fields": ["wireless"],
        "url": "https://arxiv.org/abs/2606.21235",
    },
    {
        "authors": "J. Li, W. Xu, D.H.K. Tsang, and T. Chang",
        "title": "Poster: A Software-Defined Cost-Aware Load-Balancing Wi-Fi Mesh Network with Multiple Cellular-Enabled Gateways",
        "venue": "IEEE SECON",
        "year": 2026,
        "type": "conference",
        "fields": ["wireless", "cloud-edge"],
    },
    {
        "authors": "Y. Bi and D.H.K. Tsang",
        "title": "Online Active Learning for Adaptive Channel Estimation in Fluid Antenna Systems",
        "venue": "IEEE ICC",
        "year": 2026,
        "type": "conference",
        "fields": ["wireless"],
    },
    {
        "authors": "L. Gao, L. Liu, D.H.K. Tsang, and I.M.C. Lo",
        "title": "MLLM-Empowered Active Learning with Generated Attributes for Microscopic Algae Image Classification",
        "venue": "IEEE ICASSP",
        "year": 2026,
        "type": "conference",
        "fields": ["cloud-edge"],
    },
    {
        "authors": "X. He, H. Wen, Y. Zhang, Y. Chen, and D.H.K. Tsang",
        "title": "Modeling and tackling unit commitment constraint screening under uncertainty",
        "venue": "Applied Energy",
        "year": 2026,
        "type": "journal",
        "fields": ["smart-grids", "online-algorithms"],
        "url": "https://doi.org/10.1016/j.apenergy.2026.127582",
    },
    {
        "authors": "L. Deng, X.Y. Liu, W. Xu, J. Li, and D.H.K. Tsang",
        "title": "Masked Generative Models for Real-Time Network Traffic Forecasting",
        "venue": "IEEE Internet of Things Journal",
        "year": 2026,
        "type": "journal",
        "fields": ["cloud-edge"],
    },
    {
        "authors": "Y. Gao, D.H.K. Tsang, and V.K.N. Lau",
        "title": "Bayesian End-to-End Learning for FDD-Massive MIMO Physical-Layer Design",
        "venue": "IEEE Transactions on Signal Processing",
        "year": 2026,
        "type": "journal",
        "fields": ["wireless"],
    },
    {
        "authors": "X. He, Y. Pan, Y. Chen, and D.H.K. Tsang",
        "title": "Vertex-Guided Redundant Constraints Identification for Unit Commitment",
        "venue": "IEEE Transactions on Power Systems",
        "year": 2026,
        "type": "journal",
        "fields": ["smart-grids", "online-algorithms"],
    },
    {
        "authors": "G. Huang, Y. Cui, D.H.K. Tsang, W. Wang, and L. Liu",
        "title": "Semantic Modulated Prompting for Few-Shot Audio-Visual Classification",
        "venue": "IEEE Transactions on Audio, Speech and Language Processing",
        "year": 2026,
        "type": "journal",
        "fields": ["cloud-edge"],
    },
    {
        "authors": "T. Zhou, Z. Chen, W. Lyu, Z. Chen, D.H.K. Tsang, and J. Zhang",
        "title": "Learning design-score manifold to guide diffusion models for offline optimization",
        "venue": "npj Artificial Intelligence",
        "year": 2026,
        "type": "journal",
        "fields": ["online-algorithms", "cloud-edge"],
        "url": "https://doi.org/10.1038/s44387-025-00004-0",
    },
    {
        "authors": "G. Huang, D.H.K. Tsang, X.P. Zhang, and L. Liu",
        "title": "Lend a Hand: Semi Training-Free Cued Speech Recognition via MLLM-Driven Hand Modeling for Barrier-Free Communication",
        "venue": "IEEE ICASSP",
        "year": 2026,
        "type": "conference",
        "fields": ["cloud-edge"],
        "url": "https://doi.org/10.1109/icassp55912.2026.11462042",
    },
    # 2025
    {
        "authors": "X. He, Z. Fang, J. Lian, D.H.K. Tsang, B. Zhang, and Y. Chen",
        "title": "FREESH: Fair, Resource- and Energy-Efficient Scheduling for LLM Serving on Heterogeneous GPUs",
        "venue": "arXiv preprint arXiv:2511.00807",
        "year": 2025,
        "type": "journal",
        "fields": ["cloud-edge", "online-algorithms"],
        "url": "https://arxiv.org/abs/2511.00807",
    },
    {
        "authors": "G. Huang, D.H.K. Tsang, S. Yang, G. Lei, and L. Liu",
        "title": "Cued-Agent: A Collaborative Multi-Agent System for Automatic Cued Speech Recognition",
        "venue": "ACM Multimedia",
        "year": 2025,
        "type": "conference",
        "fields": ["cloud-edge"],
        "url": "https://doi.org/10.1145/3746027.3755423",
    },
    {
        "authors": "W. Xu, C. Pan, Y. Yuan, Y. Wu, and D.H.K. Tsang",
        "title": "Reconfigurable Intelligent Surface Aided Mobile Fog Computing: A Space Aggregation-based Lyapunov Driven Reinforcement Learning Approach",
        "venue": "IEEE Transactions on Mobile Computing",
        "year": 2025,
        "type": "journal",
        "fields": ["wireless", "cloud-edge"],
        "url": "https://doi.org/10.1109/tmc.2025.3619505",
    },
    {
        "authors": "J. Xie, D.H.K. Tsang, and S. Li",
        "title": "MSfusion: A Dynamic Model Splitting Approach for Resource-Constrained Machines to Collaboratively Train Larger Models",
        "venue": "Lecture Notes in Computer Science",
        "year": 2025,
        "type": "conference",
        "fields": ["cloud-edge"],
        "url": "https://doi.org/10.1007/978-3-032-04558-4_2",
    },
    {
        "authors": "Z. Li, Y. Cui, and D.H.K. Tsang",
        "title": "AMP-Based Joint Activity Detection and Channel Estimation for Massive Grant-Free Access in OFDM-Based Wideband Systems",
        "venue": "IEEE Transactions on Wireless Communications",
        "year": 2025,
        "type": "journal",
        "fields": ["wireless"],
        "url": "https://doi.org/10.1109/twc.2025.3598367",
    },
    {
        "authors": "T. Zhou, J. Yu, J. Zhang, and D.H.K. Tsang",
        "title": "Federated Prompt-based Decision Transformer for Resource Allocation of Customized VR Streaming in Mobile Edge Computing",
        "venue": "IEEE Transactions on Wireless Communications",
        "year": 2025,
        "type": "journal",
        "fields": ["cloud-edge", "online-algorithms"],
        "url": "https://doi.org/10.1109/twc.2025.3586371",
    },
    {
        "authors": "L. Deng, W. Xu, J. Li, and D.H.K. Tsang",
        "title": "Real-Time Network Traffic Forecasting with Missing Data: A Generative Model Approach",
        "venue": "arXiv preprint arXiv:2506.09647",
        "year": 2025,
        "type": "journal",
        "fields": ["cloud-edge"],
        "url": "https://arxiv.org/abs/2506.09647",
    },
    {
        "authors": "Y. Bi, V.K.N. Lau, and D.H.K. Tsang",
        "title": "Bayesian Reinforcement Learning for IRS-Assisted Massive MIMO-OFDM Channel Feedback, Beamforming, and IRS Control",
        "venue": "IEEE ICC",
        "year": 2025,
        "type": "conference",
        "fields": ["wireless"],
        "url": "https://doi.org/10.1109/icc52391.2025.11161200",
    },
    {
        "authors": "L. Deng and D.H.K. Tsang",
        "title": "Generative Matrix Completion for Real-Time Network Latency Estimation",
        "venue": "IEEE ICC",
        "year": 2025,
        "type": "conference",
        "fields": ["cloud-edge"],
        "url": "https://doi.org/10.1109/icc52391.2025.11161103",
    },
    {
        "authors": "Z. Zhang, J. Yu, and D.H.K. Tsang",
        "title": "Intelligent Attention-Based QoE Enhancement for VR Interaction: Keyframe Extraction and Resource Allocation",
        "venue": "IEEE ICC",
        "year": 2025,
        "type": "conference",
        "fields": ["cloud-edge"],
        "url": "https://doi.org/10.1109/icc52391.2025.11161962",
    },
    {
        "authors": "W. Xu, J. Jiang, L. Deng, and D.H.K. Tsang",
        "title": "A Lyapunov Drift-Plus-Penalty Method Tailored for Reinforcement Learning with Queue Stability",
        "venue": "arXiv preprint arXiv:2506.04291",
        "year": 2025,
        "type": "journal",
        "fields": ["online-algorithms", "cloud-edge"],
        "url": "https://arxiv.org/abs/2506.04291",
    },
    {
        "authors": "T. Zhan, S. Shen, and D.H.K. Tsang",
        "title": "Machine Learning Based Accurate Modeling of Rectenna Nonlinear Behavior",
        "venue": "IEEE WPTCE",
        "year": 2025,
        "type": "conference",
        "fields": ["wireless"],
        "url": "https://doi.org/10.1109/wptce62521.2025.11062091",
    },
    {
        "authors": "L. Deng, X.Y. Liu, and D.H.K. Tsang",
        "title": "Real-Time Network Latency Estimation With Pretrained Generative Models",
        "venue": "IEEE Transactions on Neural Networks and Learning Systems",
        "year": 2025,
        "type": "journal",
        "fields": ["cloud-edge"],
        "url": "https://doi.org/10.1109/tnnls.2025.3573200",
    },
    {
        "authors": "L. Deng, X.Y. Liu, H. Zheng, X. Feng, M. Zhu, and D.H.K. Tsang",
        "title": "Graph-Tensor FISTA-Net: Edge Computing-Aided Deep Learning for Distributed Traffic Data Recovery",
        "venue": "IEEE Transactions on Network Science and Engineering",
        "year": 2025,
        "type": "journal",
        "fields": ["cloud-edge"],
        "url": "https://doi.org/10.1109/tnse.2025.3554634",
    },
    {
        "authors": "Y. Yuan, D.H.K. Tsang, and V.K.N. Lau",
        "title": "Step Size Adaptation for Accelerated Stochastic Momentum Algorithm Using SDE Modeling and Lyapunov Drift Minimization",
        "venue": "IEEE Transactions on Signal Processing",
        "year": 2025,
        "type": "journal",
        "fields": ["online-algorithms", "wireless"],
        "url": "https://doi.org/10.1109/tsp.2025.3592678",
    },
    {
        "authors": "Z. Zhang, J. Yu, and D.H.K. Tsang",
        "title": "Causal-Aware Intelligent QoE Optimization for VR Interaction with Adaptive Keyframe Extraction",
        "venue": "arXiv preprint arXiv:2506.19890",
        "year": 2025,
        "type": "journal",
        "fields": ["cloud-edge"],
        "url": "https://arxiv.org/abs/2506.19890",
    },
    {
        "authors": "X. He, D.H.K. Tsang, and Y. Chen",
        "title": "Long-Term Carbon-Efficient Planning for Geographical Shiftable Resources: A Monte Carlo Tree Search Approach",
        "venue": "IEEE PES General Meeting",
        "year": 2025,
        "type": "conference",
        "fields": ["smart-grids", "online-algorithms"],
        "url": "https://doi.org/10.1109/pesgm52009.2025.11225081",
    },
    # 2024 additions / updates
    {
        "authors": "Z. Li, Y. Cui, and D.H.K. Tsang",
        "title": "AMP-based Joint Activity Detection and Channel Estimation for OFDM-based Grant-Free Access",
        "venue": "IEEE Globecom Workshops",
        "year": 2024,
        "type": "conference",
        "fields": ["wireless"],
        "url": "https://doi.org/10.1109/gcwkshp64532.2024.11100898",
    },
    {
        "authors": "X. He, D.H.K. Tsang, and Y. Chen",
        "title": "Is Locational Marginal Price All You Need for Locational Marginal Emission?",
        "venue": "arXiv preprint arXiv:2411.12104",
        "year": 2024,
        "type": "journal",
        "fields": ["smart-grids"],
        "url": "https://arxiv.org/abs/2411.12104",
    },
    {
        "authors": "X. He, H. Wen, Y. Zhang, Y. Chen, and D.H.K. Tsang",
        "title": "Efficient Unit Commitment Constraint Screening under Uncertainty",
        "venue": "arXiv preprint arXiv:2408.05185",
        "year": 2024,
        "type": "journal",
        "fields": ["smart-grids", "online-algorithms"],
        "url": "https://arxiv.org/abs/2408.05185",
    },
    {
        "authors": "Y. Cao, S. Yu, X. Tan, and D.H.K. Tsang",
        "title": "Competitive Analysis of Online Path Selection: Impacts of Path Length, Topology, and System-Level Costs",
        "venue": "arXiv preprint arXiv:2407.05239",
        "year": 2024,
        "type": "journal",
        "fields": ["online-algorithms"],
        "url": "https://arxiv.org/abs/2407.05239",
    },
    {
        "authors": "C. Xia, H. Ma, H. Guo, D.H.K. Tsang, and V.K.N. Lau",
        "title": "Multi-resolution Neural Network Compression Based on Variational Bayesian Inference",
        "venue": "IEEE ICC",
        "year": 2024,
        "type": "conference",
        "fields": ["cloud-edge"],
        "url": "https://doi.org/10.1109/icc51166.2024.10622200",
    },
    {
        "authors": "T. Liang, C.Y. Chiu, S. Gupta, and D.H.K. Tsang",
        "title": "Boosting RF-DC Rectification via Bias Voltage",
        "venue": "IEEE WPTCE",
        "year": 2024,
        "type": "conference",
        "fields": ["wireless"],
        "url": "https://doi.org/10.1109/wptce59894.2024.10557315",
    },
    {
        "authors": "Y. Cao, S. Yu, X. Tan, and D.H.K. Tsang",
        "title": "Competitive Online Path-Aware Path Selection",
        "venue": "ACM SIGMETRICS Performance Evaluation Review",
        "year": 2024,
        "type": "journal",
        "fields": ["online-algorithms"],
        "url": "https://doi.org/10.1145/3649477.3649498",
    },
    {
        "authors": "Y. Bi, V.K.N. Lau, and D.H.K. Tsang",
        "title": "Model-Driven Bayesian Reinforcement Learning for IRS-Assisted Massive MIMO-OFDM Channel Feedback, Beamforming, and IRS Control",
        "venue": "IEEE Transactions on Wireless Communications",
        "year": 2025,
        "type": "journal",
        "fields": ["wireless"],
        "url": "https://doi.org/10.1109/twc.2024.3522098",
    },
    {
        "authors": "W. Ma, Y. Cao, D.H.K. Tsang, and D. Xia",
        "title": "Optimal Regularized Online Allocation by Adaptive Re-Solving",
        "venue": "Operations Research",
        "year": 2025,
        "type": "journal",
        "fields": ["online-algorithms"],
        "url": "https://doi.org/10.1287/opre.2022.0486",
    },
    {
        "authors": "X. He, D.H.K. Tsang, and Y. Chen",
        "title": "Long-Term Carbon-Efficient Planning for Geographical Shiftable Resources: A Monte Carlo Tree Search Approach",
        "venue": "IEEE Transactions on Power Systems",
        "year": 2025,
        "type": "journal",
        "fields": ["smart-grids", "online-algorithms"],
        "url": "https://doi.org/10.1109/tpwrs.2024.3424409",
    },
]


def norm(title: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", title.lower())).strip()


def ye(s: str) -> str:
    return "'" + str(s).replace("'", "''") + "'"


def main() -> None:
    existing = yaml.safe_load(PATH.read_text()) or []
    by_title = {norm(p["title"]): p for p in existing}

    max_j = max(
        (int(re.sub(r"\D", "", str(p["id"])) or 0) for p in existing if str(p["id"]).startswith("j")),
        default=77,
    )
    max_c = max(
        (int(re.sub(r"\D", "", str(p["id"])) or 0) for p in existing if str(p["id"]).startswith("c")),
        default=56,
    )

    added = updated = 0
    for item in CURATED:
        key = norm(item["title"])
        found = by_title.get(key)
        if not found:
            for k, p in by_title.items():
                if key == k or (len(key) > 40 and (key in k or k in key) and abs(len(key) - len(k)) < 25):
                    found = p
                    key = k
                    break

        if found:
            changed = False
            # Prefer published year/venue/url when curated is better
            if item.get("year", 0) >= found.get("year", 0):
                if item["year"] != found.get("year"):
                    found["year"] = item["year"]
                    changed = True
            if item.get("url") and (
                not found.get("url")
                or ("arxiv" in (found.get("url") or "") and "doi.org" in item["url"])
            ):
                found["url"] = item["url"]
                changed = True
            if "arxiv" in (found.get("venue") or "").lower() and "arxiv" not in item["venue"].lower():
                found["venue"] = item["venue"]
                changed = True
            for f in item.get("fields") or []:
                if f not in found.get("fields", []):
                    found.setdefault("fields", []).append(f)
                    changed = True
            if changed:
                updated += 1
            continue

        entry = {
            "id": None,
            "authors": item["authors"],
            "title": item["title"],
            "venue": item["venue"],
            "year": item["year"],
            "type": item["type"],
            "fields": list(item.get("fields") or []),
        }
        if item.get("url"):
            entry["url"] = item["url"]
        if entry["type"] == "journal":
            max_j += 1
            entry["id"] = f"j{max_j}"
        else:
            max_c += 1
            entry["id"] = f"c{max_c}"
        existing.append(entry)
        by_title[norm(entry["title"])] = entry
        added += 1

    # Drop exact duplicate titles keeping best (doi > arxiv, higher year)
    best: dict[str, dict] = {}
    for p in existing:
        k = norm(p["title"])
        if k not in best:
            best[k] = p
            continue
        cur = best[k]

        def score(x: dict) -> tuple:
            return (
                1 if x.get("url") and "doi.org" in x.get("url", "") else 0,
                0 if "arxiv" in (x.get("venue") or "").lower() else 1,
                x.get("year") or 0,
                1 if x.get("url") else 0,
            )

        if score(p) > score(cur):
            best[k] = p
    existing = list(best.values())

    # Remove known redundant Tingxi title variant if Boosting exists
    titles = {norm(p["title"]) for p in existing}
    if norm("Boosting RF-DC Rectification via Bias Voltage") in titles:
        existing = [
            p
            for p in existing
            if "on the enhancement of rf-dc rectification" not in norm(p["title"])
        ]

    existing.sort(key=lambda p: (-(p.get("year") or 0), p.get("type", ""), p.get("id", "")))

    lines: list[str] = []
    for p in existing:
        lines.append(f"- id: {p['id']}")
        lines.append(f"  authors: {ye(p['authors'])}")
        lines.append(f"  title: {ye(p['title'])}")
        lines.append(f"  venue: {ye(p['venue'])}")
        lines.append(f"  year: {p['year']}")
        lines.append(f"  type: {p['type']}")
        fields = p.get("fields") or []
        lines.append(f"  fields: [{', '.join(fields)}]" if fields else "  fields: []")
        if p.get("url"):
            lines.append(f"  url: {ye(p['url'])}")
        lines.append("")
    PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"added={added} updated={updated} total={len(existing)}")


if __name__ == "__main__":
    main()
