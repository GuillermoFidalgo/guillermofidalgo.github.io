#!/usr/bin/env python3
"""Build the CV, the resume and a JSON Resume export from _data/cv.yml.

Usage:
    python cv/build_cv.py                # build everything
    python cv/build_cv.py --only resume  # cv | resume | json

Outputs (written next to this script):
    CV.md        full academic CV
    resume.md    short resume: only entries (and highlights) with `resume: true`
    resume.json  JSON Resume schema (https://jsonresume.org/schema)

Only dependency: PyYAML (pip install pyyaml).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "_data" / "cv.yml"
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
SITE_URL = ""  # basics.url, set in main(); prefixes site-relative links


# --------------------------------------------------------------------------- #
# Dates
# --------------------------------------------------------------------------- #
def _parts(value) -> tuple[int, ...]:
    """'2022-07-19' -> (2022, 7, 19); '2022' -> (2022,); '' / None -> ()."""
    if value is None or value == "":
        return ()
    if isinstance(value, (dt.date, dt.datetime)):  # unquoted YAML dates
        return (value.year, value.month, value.day)
    return tuple(int(p) for p in str(value).split("-"))


def fmt_date(value) -> str:
    if str(value).lower() == "present":
        return "Present"
    p = _parts(value)
    if len(p) == 1:
        return str(p[0])
    if len(p) == 2:
        return f"{MONTHS[p[1] - 1]} {p[0]}"
    if len(p) == 3:
        return f"{MONTHS[p[1] - 1]} {p[2]}, {p[0]}"
    return ""


def fmt_range(start, end) -> str:
    """Compact range: 'Jul 19–23, 2022', 'Jan–May 2021', '2020–2024'."""
    if not end:
        return fmt_date(start)
    if not start:
        return fmt_date(end)
    if str(end).lower() == "present":
        return f"{fmt_date(start)}–Present"
    s, e = _parts(start), _parts(end)
    if len(s) == len(e) == 3 and s[0] == e[0]:
        if s[1] == e[1]:
            return f"{MONTHS[s[1] - 1]} {s[2]}–{e[2]}, {s[0]}"
        return f"{MONTHS[s[1] - 1]} {s[2]}–{MONTHS[e[1] - 1]} {e[2]}, {s[0]}"
    if len(s) == len(e) == 2 and s[0] == e[0]:
        return f"{MONTHS[s[1] - 1]}–{MONTHS[e[1] - 1]} {s[0]}"
    return f"{fmt_date(start)}–{fmt_date(end)}"


def when(item: dict) -> str:
    if item.get("period"):
        return item["period"]
    return fmt_range(item.get("start") or item.get("date"), item.get("end"))


def iso(value) -> str | None:
    """JSON Resume wants ISO 8601 (YYYY, YYYY-MM or YYYY-MM-DD)."""
    p = _parts(value) if str(value).lower() != "present" else ()
    return "-".join(f"{x:02d}" if i else str(x) for i, x in enumerate(p)) or None


def sort_key(item: dict):
    """Newest first; 'present' sorts on top, undated items last."""
    for key in ("end", "date", "start"):
        v = item.get(key)
        if str(v).lower() == "present":
            return (9999,)
        if v:
            return _parts(v)
    return (0,)


def newest_first(items):
    return sorted(items or [], key=sort_key, reverse=True)


# --------------------------------------------------------------------------- #
# Markdown helpers
# --------------------------------------------------------------------------- #
def absolute(url: str | None) -> str | None:
    """'/assets/x.pdf' -> 'https://<site>/assets/x.pdf' (the CV leaves the site)."""
    if url and url.startswith("/"):
        return SITE_URL.rstrip("/") + url
    return url


def link(text: str, url: str | None) -> str:
    return f"[{text}]({absolute(url)})" if url else text


def highlights(item: dict, resume: bool, indent: str = "  ") -> list[str]:
    out = []
    for h in item.get("highlights") or []:
        h = {"text": h} if isinstance(h, str) else h
        if not resume or h.get("resume"):
            out.append(f"{indent}- {h['text']}")
    return out


def pick(items, resume: bool):
    return [i for i in items or [] if not resume or i.get("resume")]


def header(cv: dict) -> list[str]:
    b = cv["basics"]
    loc = b.get("location", {})
    contact = [
        f"[{b['email']}](mailto:{b['email']})",
        link(b["url"].removeprefix("https://").rstrip("/"), b["url"]),
    ] + [link(p["network"], p["url"]) for p in b.get("profiles", [])]
    if loc:
        contact.insert(
            0, ", ".join(v for v in (loc.get("city"), loc.get("region")) if v)
        )
    return [f"# {b['name']}", "", f"**{b['label']}**", "", " · ".join(contact), ""]


def section(title: str, body: list[str]) -> list[str]:
    return [f"## {title}", "", *body, ""] if body else []


# --------------------------------------------------------------------------- #
# Sections (shared by CV and resume; `resume=True` filters and condenses)
# --------------------------------------------------------------------------- #
def education(cv, resume):
    out = []
    for e in pick(cv.get("education"), resume):
        title = f"**{e['degree']} in {e['area']}**"
        if e.get("minor"):
            title += f", minor in {e['minor']}"
        out.append(f"- {title} — {e['institution']} ({when(e)})")
        if e.get("advisor") and not resume:
            out.append(f"  - Advisor: {e['advisor']}")
        if t := e.get("thesis"):
            label = "Thesis" if not t.get("note") else t["note"]
            out.append(f"  - {label}: *{link(t['title'], t.get('url'))}*")
    return out


def research(cv, resume):
    out = []
    for r in pick(newest_first(cv.get("research")), resume):
        out.append(f"### {r['position']}")
        meta = [r["organization"], r.get("location"), when(r)]
        out.append(f"*{' | '.join(m for m in meta if m)}*")
        if r.get("supervisor") and not resume:
            # Own paragraph: a trailing-space line break would be stripped by
            # the trailing-whitespace pre-commit hook.
            out += ["", f"Supervisor: {r['supervisor']}"]
        out.append("")
        out += highlights(r, resume, indent="")
        if r.get("links") and not resume:
            out.append(
                "- " + " · ".join(link(l["label"], l["url"]) for l in r["links"])
            )
        out.append("")
    return out[:-1]


def publication_line(p) -> str:
    line = f"{p['authors']}, *{link(p['title'], p.get('url'))}*, {p['venue']}"
    if p.get("date") and p["date"][:4] not in p["venue"]:
        line += f" ({p['date'][:4]})"
    line += "."
    if p.get("note"):
        line += f" {p['note']}"
    return line


def publications(cv, resume):
    pubs = cv.get("publications", {})
    out = [
        f"{i}. {publication_line(p)}"
        for i, p in enumerate(pick(newest_first(pubs.get("selected")), resume), 1)
    ]
    if (c := pubs.get("collaboration")) and (not resume or c.get("resume")):
        out += [
            "",
            (
                link(c["summary"], c.get("url"))
                if resume
                else f"{c['summary']} Full list: {link('INSPIRE-HEP', c.get('url'))}."
            ),
        ]
    if pubs.get("acknowledged") and not resume:
        out += ["", "**Acknowledged in**", ""]
        out += [f"- {publication_line(p)}" for p in pubs["acknowledged"]]
    return out


def talks(cv, resume):
    out = []
    for t in pick(newest_first(cv.get("talks")), resume):
        kind = " (poster)" if t.get("type") == "poster" else ""
        out.append(
            f"- *{link(t['title'], t.get('url'))}*{kind} — "
            f"{t['event']}, {t['location']}, {when(t)}"
        )
    return out


def events(items, resume, show_role=True):
    out = []
    for e in pick(newest_first(items), resume):
        role = f"{e['role']}, " if show_role and e.get("role") else ""
        line = (
            f"- {role}**{link(e['title'], e.get('url'))}** — {e['location']}, {when(e)}"
        )
        if e.get("description") and not resume:
            line += f". {e['description']}"
        out.append(line)
    return out


def teaching_resume(cv):
    """Resume: one condensed bullet group instead of every workshop."""
    teach, outreach = cv.get("teaching") or [], cv.get("outreach") or []
    years = [
        _parts(i.get("start") or i.get("date"))[0]
        for i in teach + outreach
        if i.get("start") or i.get("date")
    ]
    out = [
        f"- Taught, mentored or organized {len(teach) + len(outreach)} software and "
        f"data-analysis workshops and courses ({min(years)}–{max(years)}) for audiences from high school "
        "students and STEM teachers to HEP postdocs, including HSF/IRIS-HEP, "
        "Software Carpentry and the CMS Data Analysis School."
    ]
    out += events(cv.get("mentoring"), True)
    return out


def service(cv, resume):
    out = []
    for s in pick(newest_first(cv.get("service")), resume):
        line = f"- {s['role']}, {link(s['organization'], s.get('url'))} — {s['location']}, {when(s)}"
        if s.get("description") and not resume:
            line += f". {s['description']}"
        out.append(line)
    return out


def leadership(cv, resume):
    out = []
    for l in pick(cv.get("leadership"), resume):
        dates = f" ({when(l)})" if when(l) else ""
        out.append(f"- **{l['role']}**, {link(l['organization'], l.get('url'))}{dates}")
        out += highlights(l, resume)
    return out


def honors(cv, resume):
    out = []
    for a in pick(cv.get("awards"), resume):
        date = f" ({fmt_date(a['date'])})" if a.get("date") else ""
        out.append(
            f"- **{link(a['title'], a.get('url'))}**{date}. {a.get('summary', '')}".rstrip()
        )
    for c in pick(cv.get("certifications"), resume):
        date = f" ({fmt_date(c['date'])})" if c.get("date") else ""
        out.append(f"- **{c['name']}**, {link(c['issuer'], c.get('url'))}{date}")
    return out


def memberships(cv, resume):
    return [
        f"- {link(m['organization'], m.get('url'))}"
        for m in pick(cv.get("memberships"), resume)
    ]


def skills(cv, _resume):
    out = [
        f"- **{s['category']}:** {', '.join(s['items'])}"
        for s in cv.get("skills") or []
    ]
    if langs := cv.get("languages"):
        out.append(
            "- **Languages:** "
            + ", ".join(f"{l['language']} ({l['fluency']})" for l in langs)
        )
    return out


# --------------------------------------------------------------------------- #
# Documents
# --------------------------------------------------------------------------- #
def build_cv(cv) -> str:
    lines = header(cv)
    lines += section("Summary", [cv["basics"]["summary"]["cv"]])
    lines += section("Education", education(cv, False))
    lines += section("Research Experience", research(cv, False))
    lines += section("Publications", publications(cv, False))
    lines += section("Conference Talks and Posters", talks(cv, False))
    lines += section(
        "Software Training: Instructor and Mentor", events(cv.get("teaching"), False)
    )
    lines += section("Student Mentoring", events(cv.get("mentoring"), False))
    lines += section(
        "Education and Outreach Activities Organized",
        events(cv.get("outreach"), False, show_role=False),
    )
    lines += section("Service", service(cv, False))
    lines += section("Leadership", leadership(cv, False))
    lines += section("Honors and Certifications", honors(cv, False))
    lines += section("Memberships", memberships(cv, False))
    lines += section("Skills", skills(cv, False))
    return "\n".join(lines).rstrip() + "\n"


def build_resume(cv) -> str:
    lines = header(cv)
    lines += section("Summary", [cv["basics"]["summary"]["resume"]])
    lines += section("Education", education(cv, True))
    lines += section("Research Experience", research(cv, True))
    lines += section("Teaching and Mentoring", teaching_resume(cv) + service(cv, True))
    lines += section("Selected Publications", publications(cv, True))
    lines += section("Selected Talks", talks(cv, True))
    lines += section("Leadership", leadership(cv, True))
    lines += section("Honors and Certifications", honors(cv, True))
    lines += section("Skills", skills(cv, True))
    return "\n".join(lines).rstrip() + "\n"


def build_json_resume(cv) -> dict:
    """Map onto https://jsonresume.org/schema (v1.0.0). Includes everything."""
    b = cv["basics"]
    loc = b.get("location", {})

    def h(item):
        return [
            x if isinstance(x, str) else x["text"] for x in item.get("highlights") or []
        ]

    def event_summary(e):
        role = f"{e['role']}. " if e.get("role") else ""
        return (
            f"{role}{e.get('location', '')}. {e.get('description', '')}".strip(" .")
            or None
        )

    data = {
        "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
        "basics": {
            "name": b["name"],
            "label": b["label"],
            "email": b["email"],
            "url": b["url"],
            "summary": b["summary"]["resume"],
            "location": {
                "city": loc.get("city"),
                "region": loc.get("region"),
                "countryCode": (
                    "US" if loc.get("country") == "USA" else loc.get("country")
                ),
            },
            "profiles": b.get("profiles", []),
        },
        "work": [
            {
                "name": r["organization"],
                "position": r["position"],
                "location": r.get("location"),
                "startDate": iso(r.get("start")),
                "endDate": iso(r.get("end")),
                "summary": (
                    f"Supervisor: {r['supervisor']}" if r.get("supervisor") else None
                ),
                "highlights": h(r),
                "url": (r.get("links") or [{}])[0].get("url"),
            }
            for r in newest_first(cv.get("research"))
        ],
        "volunteer": [
            {
                "organization": l["organization"],
                "position": l["role"],
                "url": l.get("url"),
                "startDate": iso(l.get("start")),
                "endDate": iso(l.get("end")),
                "highlights": h(l),
            }
            for l in cv.get("leadership") or []
        ]
        + [
            {
                "organization": e["title"],
                "position": e.get("role", "Organizer"),
                "url": e.get("url"),
                "startDate": iso(e.get("start") or e.get("date")),
                "endDate": iso(e.get("end") or e.get("date")),
                "summary": event_summary(e),
            }
            for e in newest_first(
                (cv.get("teaching") or [])
                + (cv.get("mentoring") or [])
                + (cv.get("outreach") or [])
            )
        ]
        + [
            {
                "organization": s["organization"],
                "position": s["role"],
                "url": s.get("url"),
                "startDate": iso(s.get("date")),
                "endDate": iso(s.get("date")),
                "summary": s.get("description"),
            }
            for s in cv.get("service") or []
        ],
        "education": [
            {
                "institution": e["institution"],
                "area": e["area"],
                "studyType": e["degree"],
                "startDate": iso(e.get("start")),
                "endDate": iso(e.get("end")),
                "courses": [f"Minor: {e['minor']}"] if e.get("minor") else [],
            }
            for e in cv.get("education") or []
        ],
        "awards": [
            {
                "title": a["title"],
                "date": iso(a.get("date")),
                "awarder": a.get("awarder"),
                "summary": a.get("summary"),
            }
            for a in cv.get("awards") or []
        ],
        "certificates": [
            {
                "name": c["name"],
                "issuer": c["issuer"],
                "date": iso(c.get("date")),
                "url": c.get("url"),
            }
            for c in cv.get("certifications") or []
        ],
        "publications": [
            {
                "name": p["title"],
                "publisher": p["venue"],
                "releaseDate": iso(p.get("date")),
                "url": p.get("url"),
                "summary": p["authors"],
            }
            for p in newest_first(cv.get("publications", {}).get("selected"))
        ],
        "skills": [
            {"name": s["category"], "keywords": s["items"]}
            for s in cv.get("skills") or []
        ],
        "languages": cv.get("languages", []),
        "interests": [{"name": i} for i in cv.get("interests") or []],
        # Not in the JSON Resume schema; kept under a custom key so nothing is lost.
        "x-talks": [
            {**t, "date": iso(t.get("date")), "end": iso(t.get("end"))}
            for t in newest_first(cv.get("talks"))
        ],
        "meta": {"lastModified": dt.date.today().isoformat(), "source": "_data/cv.yml"},
    }
    return _drop_empty(data)


def _drop_empty(obj):
    if isinstance(obj, dict):
        return {
            k: absolute(v) if k == "url" else _drop_empty(v)
            for k, v in obj.items()
            if v not in (None, "", [], {})
        }
    if isinstance(obj, list):
        return [_drop_empty(v) for v in obj]
    return obj


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--only", choices=["cv", "resume", "json"], help="build a single output"
    )
    ap.add_argument(
        "--source", type=Path, default=SOURCE, help=f"YAML source (default: {SOURCE})"
    )
    args = ap.parse_args()

    cv = yaml.safe_load(args.source.read_text(encoding="utf-8"))
    global SITE_URL
    SITE_URL = cv["basics"]["url"]
    outputs = {
        "cv": ("CV.md", lambda: build_cv(cv)),
        "resume": ("resume.md", lambda: build_resume(cv)),
        "json": (
            "resume.json",
            lambda: (
                json.dumps(build_json_resume(cv), indent=2, ensure_ascii=False) + "\n"
            ),
        ),
    }
    for key, (name, render) in outputs.items():
        if args.only in (None, key):
            (HERE / name).write_text(render(), encoding="utf-8")
            print(f"wrote {(HERE / name).relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
