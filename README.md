# University of Northeastern Somalia website

Official static website source for the University of Northeastern Somalia (UNS), Garowe, Puntland, Somalia.

## Current production

- Website: https://uns-website-1.vercel.app
- Pages: Home, About, Academics, Admissions, Learning Options, Research, Career Development, News & Events, and Contact

## Materialize the verified production source

The production deployment is static. To download its exact public source tree into this repository checkout, run:

```bash
python3 sync_from_vercel.py
```

The script downloads all nine HTML routes, shared CSS and JavaScript, the unmodified official logo, campus map, `robots.txt`, and `sitemap.xml`. It verifies every response before replacing files.

## Content policy

Only verified UNS information should be published. Do not add unconfirmed accreditation, rankings, fees, deadlines, facilities, publications, vacancies, statistics, or partnerships. Use “Contact UNS for details” where information is unavailable.
